from tkinter import *
import json
import socket
import os
import signal

class Application(Frame):
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.all_entries = []			# Maintain a list of all inputs for the ui
		self.all_deletes = []			# Maintain a list of all deletes for the ui
		self.p = None					# When localhost is started, keep track of that process so it can be killed later
		self.pack()
		self.createWidgets()
		self.window = None				# 2nd window for ui editing
		self.inputType = ""				
		self.styleWindow = None			# 3rd window for style editing
		self.styleType = ""				
	
	# When the ui is being edited, show the current state of the ui before editing begins, get state from the data.json file
	def restoreState(self):
		if os.path.getsize("./data.json") > 2:			# If there are no inputs in the file, the file contains an empty array [] which has size 2
			with open('data.json', 'r') as infile:
				json_array = json.load(infile)
				for item in json_array:
					self.addBox(item['name'])
	
	# Save contents of the database to a csv file
	def databaseDump(self):
		from subprocess import Popen
		Popen(["mongoexport -h ds143143.mlab.com:43143 -d ocean-eyes -c fishdata -u admin -p admin22 -o ./fishdata.csv --type=csv -f 'userId,location,conditions,date,catch_size'"], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
		
	# Create a new input 
	def addBox(self, textString=""):
		thisType = self.inputType.get()
		if thisType == "Text Input":
			inputType = ""
			className = ""
			ent = Entry(self.window)
			ent.insert(END, textString)
		elif thisType == "Slider":
			inputType = "range"
			className = "slider"
			ent = Scale(self.window, orient=HORIZONTAL)
		elif thisType == "Radio Button":
			inputType = "radio"
			className = ""
			ent = Radiobutton(self.window)
		elif thisType == "Checkbox":
			inputType = "checkbox"
			className = ""
			ent = Checkbutton(self.window)
		elif thisType == "Image Upload":
			inputType = ""
			className = ""
			ent = Label(self.window, text="Image Upload Widget")
		elif thisType == "Location Input":
			inputType = ""
			className = ""
			ent = Label(self.window, text="Location Select Widget")
		else:
			inputType = ""
			className = ""
			ent = Entry(self.window)
			ent.insert(END, textString)
			
		index = len(self.all_entries)
		ent.pack(side="top")
		self.all_entries.append( (ent, inputType, className) )
		remove = Button(self.window, text='X', fg="Red", command=lambda i=index: self.removeBox(i))
		remove.pack(side="top")
		self.all_deletes.append( remove )
	
	# Remove input box at index i in the list of inputs	
	def removeBox(self, i):
		item = self.all_entries[i][0]
		item.destroy()
		del self.all_entries[i]
		
		item = self.all_deletes[i]
		item.destroy()
		del self.all_deletes[i]
		
		for index in range(len(self.all_deletes)):
			self.all_deletes[index].configure(command=lambda x=index: self.removeBox(x))
			
	
	# Test if localhost port is in use
	def tryPort(self, port):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = False
		try:
			sock.bind(("127.0.0.1", port))
			result = True
		except:
			print("Server refreshed")
		sock.close()
		return result
    
    # Save generated inputs to file
	def createInputs(self):
		with open('data.json', 'w') as outfile:
			inputs = []
			for number, ent in enumerate(self.all_entries):
				inputName = ent[0].get()
				data = ({'key': number, 'label': inputName, 'name': inputName, 'type': ent[1], 'className': ent[2]})
				inputs.append(data)
			json.dump(inputs, outfile)
	
	# Upload all files in path to a remote server
	def uploadToServer(self):
		username = "nfallowf"
		password = "h7Y65thUp0"
		host = "compute.gaul.csd.uwo.ca"
		port = 22 

		import pysftp
		remotepath = '/'
		localpath = './'
		cnopts = pysftp.CnOpts()
		cnopts.hostkeys = None

		with pysftp.Connection(host=host,username=username,password=password,cnopts=cnopts, port=22) as sftp:

			sftp.put_r('../../src/', "/student/nfallowf/thesis/my-app")
			print('Upload finished')
	
	# Start node project on localhost:8080 if available
	def startLocalhost(self):
		if self.tryPort(8080):
			print ("Starting dev server")
			from subprocess import Popen
			self.p = Popen(["npm start"], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
			
	# Close program, kill anything running on localhost
	def quit(self):
		if self.p is not None:
			os.killpg(os.getpgid(self.p.pid), signal.SIGTERM)
		root.destroy()
	
	# Remove the list of entries when editting window closed, so there aren't duplicates when re opened
	def onWindowClose(self):
		del self.all_entries[:]
		del self.all_deletes[:]
		self.window.destroy()
		
	# Edit the ui
	def makeEdits(self):
		self.window = Toplevel(root)
		self.window.protocol("WM_DELETE_WINDOW", self.onWindowClose)
		self.refresh_server = Button(self.window)
		
		self.refresh_server["text"] = "Refresh localhost"
		self.refresh_server["command"] = self.createInputs
		self.refresh_server.pack(side="top")
		
		
		self.inputType = StringVar(self.window)
		self.inputType.set("Text Input") # default value

		self.inputSelect = OptionMenu(self.window, self.inputType, "Text Input", "Slider", "Radio Button", "Checkbox", "Image Upload", "Location Input")
		self.inputSelect.pack(side="top")
		self.addInput = Button(self.window)
		self.addInput["text"] = "Add Input"
		self.addInput["command"] = self.addBox
		self.addInput.pack(side="top")
		
		self.restoreState()
	
	# Edit the ui
	def pickStyle(self):
		print('test')
		self.styleWindow = Toplevel(root)
		self.applyStyles = Button(self.styleWindow)
		
		self.applyStyles["text"] = "Refresh localhost"
		self.applyStyles["command"] = self.changeStyle
		self.applyStyles.pack(side="top")
		
		
		self.styleType = StringVar(self.styleWindow)
		self.styleType.set("Style 1") # default value

		self.styleSelect = OptionMenu(self.styleWindow, self.styleType, "Style 1", "Style 2")
		self.styleSelect.pack(side="top")

	
	# Save generated inputs to file
	def changeStyle(self):
		with open('styles.json', 'w') as outfile:
			style = self.styleType.get()
			if style == "Style 1":
				style = "form-style-5"
			elif style == "Style 2":
				style = "form-style-4"
			data = ({'style': style})
			json.dump(data, outfile)
			
	# Generate all widgets used on the ui
	def createWidgets(self):
		
		self.upload = Button(self)
		self.upload["text"] = "Upload Files to server"
		self.upload["command"] = self.uploadToServer
		self.upload.pack(side="top")
		
		#self.dataDump = Button(self)
		#self.dataDump["text"] = "Dump contents of database to csv file"
		#self.dataDump["command"] = self.databaseDump
		#self.dataDump.pack(side="top")
		
		self.restart_server = Button(self)
		self.restart_server["text"] = "Start localhost"
		self.restart_server["command"] = self.startLocalhost
		self.restart_server.pack(side="top")
		
		self.editUI = Button(self)
		self.editUI["text"] = "Edit UI"
		self.editUI["command"] = self.makeEdits
		self.editUI.pack(side="top")
		
		self.chooseStyles = Button(self)
		self.chooseStyles["text"] = "Change Style"
		self.chooseStyles["command"] = self.pickStyle
		self.chooseStyles.pack(side="top")
		
		self.QUIT = Button(self, text="QUIT", fg="red",
								command=self.quit)
		self.QUIT.pack(side="bottom")

root = Tk()
app = Application(master=root)
app.mainloop()
