from tkinter import *
from tkinter import font
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter.colorchooser import *
import json
import socket
import os
import signal

# Create the root window, set the size, color and
# make it go in the middle of the screen

root = Tk()
root.title("Citizen Science Web Portal")
root.update_idletasks()
width = 350
height = 300
x2 = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x2, y))
root.resizable(False, False)
root["bg"] = "#607D8B"
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(0, weight=1)


img8 = PhotoImage(file="button9.png")

# Create the application class with a constructor initializing variables used
# within the UI

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.all_entries = []  # Maintain a list of all inputs for the ui
        self.all_deletes = []  # Maintain a list of all deletes for the ui
        self.p = None  # When localhost is started, keep track of that process so it can be killed later
        self.grid()
        self.createWidgets()
        self.window = None  # 2nd window for ui editing
        self.inputType = ""
        self.styleWindow = None  # 3rd window for style editing
        self.styleType = ""

        self.rangeWindow = None  # Window for slider range input
        self.rangeMin = 0  # Min value for slider
        self.rangeMax = 100  # Max value for slider
        self.rangeLab = ""  # Label For the Slider
        self.x = 6
        self.optionsWindow = None  # Window for options input
        self.optionEntries = []  # List of options entry boxes
        self.options = []  # List of options
        self.dropLab = ""
        
            

    # Upload all files in path to a remote server
    def uploadToServer(self):
        username = input()
        password = input()
        host = input()
        port = input()

        import pysftp
        remotepath = '/'
        localpath = './'
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        with pysftp.Connection(host=host, username=username, password=password, cnopts=cnopts, port=22) as sftp:
            sftp.put_r(localpath, remotepath)
            print('Upload finished')

       # Close program, kill anything running on localhost
    def quit(self):
        if self.p is not None:
            os.killpg(os.getpgid(self.p.pid), signal.SIGTERM)
        root.destroy()
    
    def createWidgets(self):

        self['bg'] = "#607D8B"
        
        self.my_label1 = Label(self, text = "Username:", bg= "#607D8B", fg="white", font="Helvetica 14")
        self.my_label1.grid(row = 2, column = 0)
        self.my_entry3 = Entry(self, textvariable=1)
        self.my_entry3.grid(row = 2, column = 1, pady=5)
        self.my_label = Label(self, text = "Password:", bg= "#607D8B", fg="white", font="Helvetica 14")
        self.my_label.grid(row = 3, column = 0)
        self.my_entry4 = Entry(self, textvariable=2)
        self.my_entry4.grid(row = 3, column = 1, pady=5)

        self.my_label2 = Label(self, text = "Host:", bg= "#607D8B", fg="white", font="Helvetica 14")
        self.my_label2.grid(row = 4, column = 0)
        self.my_entry6 = Entry(self, textvariable=3)
        self.my_entry6.grid(row = 4, column = 1, pady=5)
        self.my_label3 = Label(self, text = "Port:", bg= "#607D8B", fg="white", font="Helvetica 14")
        self.my_label3.grid(row = 5, column = 0)
        self.my_entry5 = Entry(self, textvariable=4)
        self.my_entry5.grid(row = 5, column = 1, pady=5)

        
        
        self.my_button = Button(self, bg="#607D8B", bd=0, image=img8, command = self.uploadToServer)
        
        self.my_button.grid(row = 6, column = 1, pady=5)
        
        
app = Application(master=root)
app.mainloop()
