from tkinter import *
import json
import socket
import os
import signal

class Application(Frame):
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.all_entries = []
		self.p = None
		self.pack()
		self.createWidgets()
		self.window = None
		
	def restoreState(self):
		if os.path.getsize("./data.json") > 0:
			with open('data.json', 'r') as infile:
				json_array = json.load(infile)
				for item in json_array:
					self.addBox(item['name'])
		
	def databaseDump(self):
		from subprocess import Popen
		Popen(["mongoexport -h ds143143.mlab.com:43143 -d ocean-eyes -c fishdata -u admin -p admin22 -o ./fishdata.csv --type=csv -f 'userId,location,conditions,date,catch_size'"], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
		
	def addBox(self, text=""):
		print ("Added Input")
		index = len(self.all_entries)
		entryName = "entry"+str(index)
		deleteName = "del"+str(index)
		ent = Entry(self.window, name=entryName)
		ent.pack(side="top")
		self.all_entries.append( ent )
		remove = Button(self.window, text='X', name=deleteName, fg="Red", command=lambda i=index: self.removeBox(i))
		remove.pack(side="top")
		
	def removeBox(self, i):
		print ("Removed Input")
		ent = self.all_entries[i]
		item = root.nametowidget(ent)
		print(item)
		item.destroy
		del self.all_entries[i-1]
		
		item = root.nametowidget("del"+str(i))
		item.destroy
	
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
    
	def createInputs(self):
		with open('data.json', 'w') as outfile:
			inputs = []
			for number, ent in enumerate(self.all_entries):
				inputName = ent.get()
				data = ({'key': number, 'label': inputName, 'name': inputName})
				inputs.append(data)
			json.dump(inputs, outfile)
	
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
			
	def startLocalhost(self):
		if self.tryPort(8080):
			print ("Starting dev server")
			from subprocess import Popen
			self.p = Popen(["npm start"], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
			
	def quit(self):
		if self.p is not None:
			os.killpg(os.getpgid(self.p.pid), signal.SIGTERM)
		root.destroy()
	
	def makeEdits(self):
		self.window = Toplevel(root)
		self.refresh_server = Button(self.window)
		
		self.refresh_server["text"] = "Refresh localhost"
		self.refresh_server["command"] = self.createInputs
		self.refresh_server.pack(side="top")
		self.addInput = Button(self.window)
		self.addInput["text"] = "Add Input"
		self.addInput["command"] = self.addBox
		self.addInput.pack(side="top")
		
		self.restoreState()
		
		
	def createWidgets(self):
		
		self.upload = Button(self)
		self.upload["text"] = "Upload Files to server"
		self.upload["command"] = self.uploadToServer
		self.upload.pack(side="top")
		
		self.dataDump = Button(self)
		self.dataDump["text"] = "Dump contents of database to csv file"
		self.dataDump["command"] = self.databaseDump
		self.dataDump.pack(side="top")
		
		self.restart_server = Button(self)
		self.restart_server["text"] = "Start localhost"
		self.restart_server["command"] = self.startLocalhost
		self.restart_server.pack(side="top")
		
		self.editUI = Button(self)
		self.editUI["text"] = "Edit UI"
		self.editUI["command"] = self.makeEdits
		self.editUI.pack(side="top")
		
		self.QUIT = Button(self, text="QUIT", fg="red",
								command=self.quit)
		self.QUIT.pack(side="bottom")

root = Tk()
app = Application(master=root)
app.mainloop()
