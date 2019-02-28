from tkinter import *
import json
import socket

class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

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
		numInputs = input('Number of inputs: ')
		with open('data.json', 'w') as outfile:
			inputs = []
			for i in range(int(numInputs)):
				inputName = input('Enter name of input ' + str(i+1) + ': ')
				data = ({'key': inputName, 'label': inputName, 'name': inputName})
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
			from subprocess import call
			call(["npm", "start"])
			
	def createWidgets(self):
		L1 = Label(self, text="Number of Inputs")
		L1.pack(side="top")
		self.numInputs = Entry(self, bd =5)
		self.numInputs.pack(side="top")
		
		self.upload = Button(self)
		self.upload["text"] = "Upload Files to server"
		self.upload["command"] = self.uploadToServer
		self.upload.pack(side="top")
		
		self.restart_server = Button(self)
		self.restart_server["text"] = "Start localhost"
		self.restart_server["command"] = self.startLocalhost
		self.restart_server.pack(side="top")
		
		self.QUIT = Button(self, text="QUIT", fg="red",
								command=root.destroy)
		self.QUIT.pack(side="bottom")

	def say_hi(self):
		print("hi there, everyone!")

root = Tk()
app = Application(master=root)
app.mainloop()
