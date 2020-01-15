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
height = 500
x2 = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x2, y))
root.resizable(False, False)
root["bg"] = "#607D8B"
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(0, weight=1)

# Initialize all the images used within the UI

img5 = PhotoImage(file="button6.png")
img6 = PhotoImage(file="button7.png")
img = PhotoImage(file="button1.png")
img1 = PhotoImage(file="button2.png")
img2 = PhotoImage(file="button3.png")
img3 = PhotoImage(file="button4.png")
img4 = PhotoImage(file="button5.png")
img7 = PhotoImage(file="button8.png")
img8 = PhotoImage(file="button9.png")
img9 = PhotoImage(file="darkgradient.png")
img10 = PhotoImage(file="button10.png")
img11 = PhotoImage(file="button11.png")
img12 = PhotoImage(file="button12.png")
img13 = PhotoImage(file="button13.png")
img14 = PhotoImage(file="button14.png")
img15 = PhotoImage(file="button15.png")
img16 = PhotoImage(file="button16.png")
img17 = PhotoImage(file="button17.png")





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

        self.nameWindow = None #Window for adding name
        self.rangeWindow = None  # Window for slider range input
        self.rangeMin = 0  # Min value for slider
        self.rangeMax = 100  # Max value for slider
        self.rangeLab = ""  # Label For the Slider
        self.x = 6
        self.optionsWindow = None  # Window for options input
        self.optionEntries = []  # List of options entry boxes
        self.options = []  # List of options
        self.dropLab = ""

    # When the ui is being edited, show the current state of the ui before editing begins, get state from the data.json file
    def restoreState(self, x):
        if os.path.getsize(
                "./data.json") > 2:  # If there are no inputs in the file, the file contains an empty array [] which has size 2
            with open('data.json', 'r') as infile:
                json_array = json.load(infile)
                for item in json_array:
                    self.x = self.x + 1
                    self.restoreBox(item, x)

    # Save contents of the database to a csv file
    def databaseDump(self):
        from subprocess import Popen
        Popen([
                  "mongoexport -h ds143143.mlab.com:43143 -d ocean-eyes -c fishdata -u admin -p admin22 -o ./fishdata.csv --type=csv -f 'userId,location,conditions,date,catch_size'"],
              shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    # Add box method to handle restoring state
    def restoreBox(self, item, x):
        inputName = item['label']
        thisType = item['type']
        options = []
        
        if thisType == "":
            inputType = ""
            className = ""
            ent = Entry(self.window)
            ent.insert(END, inputName)
            ent.config(bg= "white")
        elif thisType == "time":
            inputType = "time"
            className = ""
            ent = Entry(self.window)
            ent.insert(END, "time")
            ent.config(state=DISABLED)
            ent.config(bg= "white")
        elif thisType == "date":
            inputType = "date"
            className = ""
            ent = Entry(self.window)
            ent.insert(END, "date")
            ent.config(state=DISABLED)
            ent.config(bg= "white")
        elif thisType == "range":
            inputType = "range"
            className = "slider"
            ent = Scale(self.window, orient=HORIZONTAL, from_=item['min'], to=item['max'])
            ent.config(bg="#607D8B", highlightthickness=0, length=175, fg="white")
        elif thisType == "select":
            inputType = "select"
            className = ""
            for option in item['options']:
                options.append(option['value'])
            variable = StringVar(self.window)
            variable.set(options[0])  # default value
            ent = OptionMenu(self.window, variable, *options)
            ent.config(bg = "#607D8B", fg="white", highlightthickness=0)
        elif thisType == "radio":
            inputType = "radio"
            className = ""
            for option in item['options']:
                options.append(option['value'])
            ent = Radiobutton(self.window, text="Radio Button Group", bd=2)
            ent.config(bg= "#607D8B", fg="white")
        elif thisType == "checkbox":
            inputType = "checkbox"
            className = ""
            for option in item['options']:
                options.append(option['value'])
            ent = Checkbutton(self.window, text="Check Button Group")
            ent.config(bg= "#607D8B")
        elif thisType == "map":
            inputType = "map"
            className = ""
            ent = Label(self.window, text="Location Select Widget")
            ent.config(bg= "#607D8B")
        elif thisType == "imageUpload":
            inputType = "imageUpload"
            className = ""
            ent = Label(self.window, text="Image Upload")
            ent.config(bg= "#607D8B")
        else:
            inputType = ""
            className = ""
            ent = Entry(self.frame1)
            ent.insert(END, textString)

        index = len(self.all_entries)
        ent.grid(row=self.x, column=1, columnspan=1, sticky="e", padx=3, pady=2)
        self.all_entries.append((ent, inputType, className, item['min'], item['max'], inputName, options))
        remove = Button(self.window, image=img, bd=0, highlightthickness=0, bg="#607D8B", text='x', fg="Red", command=lambda i=index: self.removeBox(i))
        remove.grid(row=self.x, column=2, sticky="w", columnspan=1, padx=3, pady=2)
        self.all_deletes.append(remove)

    # Create a new input
    def addBox(self):
        global x
        textString=""
        inputName = ""
        thisType = self.inputType.get()
        
        if thisType == "Text Input":
            self.nameWindow = Toplevel()
            self.setName()
            self.nameWindow["bg"] = "#607D8B"
            root.wait_window(self.nameWindow)
            inputName = self.nameLab
            inputType = ""
            className = ""
            ent = Entry(self.window)
            ent.insert(END, inputName)
            ent.config(bg= "white")
        elif thisType == "Time Input":
            inputType = "time"
            className = ""
            ent = Entry(self.window)
            ent.insert(END, "Time")
            ent.config(state=DISABLED)
            ent.config(bg= "white")
        elif thisType == "Date Input":
            inputType = "date"
            className = ""
            ent = Entry(self.window)
            ent.insert(END, "Date")
            ent.config(state=DISABLED,bg= "#607D8B")
            ent.config(bg= "white", borderwidth=2)
        elif thisType == "Slider":
            self.rangeWindow = Toplevel()
            self.setRange()
            self.rangeWindow["bg"] = "#607D8B"
            root.wait_window(self.rangeWindow)
            inputType = "range"
            className = "slider"
            inputName = self.rangeLab
            ent = Scale(self.window, orient=HORIZONTAL, from_=self.rangeMin, to=self.rangeMax)
            ent.config(bg="#607D8B", highlightthickness=0, borderwidth=2, length=175)
        elif thisType == "DropDown":
            self.optionsWindow = Toplevel()
            self.setOptions()
            self.optionsWindow["bg"] = "#607D8B"
            root.wait_window(self.optionsWindow)
            inputType = "select"
            className = ""
            inputName = self.dropLab
            variable = StringVar(self.window)
            variable.set(self.options[0])  # default value
            ent = OptionMenu(self.window, variable, *self.options)
            ent.config(bg= "#607D8B", fg="white", highlightthickness=0)
        elif thisType == "Radio Button":
            self.optionsWindow = Toplevel()
            self.setOptions()
            self.optionsWindow["bg"] = "#607D8B"
            root.wait_window(self.optionsWindow)
            inputType = "radio"
            className = ""
            inputName = self.dropLab
            ent = Radiobutton(self.window, text="Radio Button Group")
            ent.config(bg= "#607D8B", fg="black")
        elif thisType == "Checkbox":
            self.optionsWindow = Toplevel()
            self.setOptions()
            self.optionsWindow["bg"] = "#607D8B"
            root.wait_window(self.optionsWindow)
            inputType = "checkbox"
            className = ""
            inputName = self.dropLab
            ent = Checkbutton(self.window, text="Check Button Group")
            ent.config(bg= "#607D8B")
        elif thisType == "Image Upload":
            inputType = "imageUpload"
            className = ""
            ent = Label(self.window, text="Image Upload Widget")
            ent.config(bg= "#607D8B")
        elif thisType == "Location Input":
            inputType = "map"
            className = ""
            ent = Label(self.window, text="Location Select Widget")
            ent.config(bg= "#607D8B")
        else:
            inputType = ""
            className = ""
            ent = Entry(self.window)
            ent.insert(END, textString)
            ent.config(bg= "#607D8B")
            
        index = len(self.all_entries)
        self.x = self.x + 1
        ent.grid(row=self.x, column=1, columnspan=1, sticky="e", padx=3, pady=2)
        options = self.options.copy()
        self.all_entries.append((ent, inputType, className, self.rangeMin, self.rangeMax, inputName, options))
        remove = Button(self.window, image=img, bd=0, bg="#607D8B", text='x', fg="Red", command=lambda i=index: self.removeBox(i))
        remove.grid(row=self.x, column=2, sticky="w", columnspan=1, padx=3, pady=2)
        self.all_deletes.append(remove)

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
                options = []
                if (isinstance(ent[0], Entry)):
                    inputName = ent[0].get()
                else:
                    inputName = ent[5]
                if (isinstance(ent[0], OptionMenu) or isinstance(ent[0], Radiobutton) or isinstance(ent[0],
                                                                                                    Checkbutton)):
                    for key, item in enumerate(ent[6]):
                        options.append({"value": item, "label": item, "key": key})
                data = ({'key': number, 'label': inputName, 'name': inputName, 'type': ent[1], 'className': ent[2],
                         'min': ent[3], 'max': ent[4], 'options': options})
                inputs.append(data)
            json.dump(inputs, outfile)
        with open('title.json', 'w') as outfile:
            title = self.titleEntry.get()
            data = ({'titlename': title})
            json.dump(data, outfile)
            

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

    # Start node project on localhost:8080 if available
    def startLocalhost(self):
        if self.tryPort(8080):
            print("Starting dev server")
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
        
    def prioraddBox(self, x):
        print(self.x)
        self.addBox(x)
        
    # Edit the ui. Create a resizable window with specific colors. 
    def makeEdits(self):
        self.window = Toplevel(root)
        self.window.protocol("WM_DELETE_WINDOW", self.onWindowClose)
        
        ### F5F5F5 vs 607D8B vs #607D8B
        
        self.window["bg"] = "#607D8B"
        
        width = 350
        height = 600
        x1 = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x1, y))
        
        
        self.topFrame = Label(self.window, text="Edit UI", underline=True, font="Helvetica 14", fg="white")
        self.topFrame['bg'] = "#607D8B"
        f = font.Font(self.topFrame, self.topFrame.cget("font"))
        f.configure(underline = True)
        self.topFrame.configure(font=f)

        self.window.grid_rowconfigure(0, weight=0)
        self.window.grid_rowconfigure(1, weight=0)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        self.window.grid_columnconfigure(3, weight=1)
        self.topFrame.grid(row=0, column=1, columnspan=2, pady=6)
        self.refresh_server = Button(self.window)

        # Create the dropdown with input options, labels, frames which hold
        # the items and align them. 

        global x
        self.refresh_server["command"] = self.createInputs
        self.refresh_server.config(image=img5, bd=0)
        self.refresh_server['bg'] = "#607D8B"

        self.refresh_server.grid(row=1, column=1, columnspan=2)

        self.inputType = StringVar(self.window)
        self.inputType.set("Text Input")  # default value

        self.inputSelect = OptionMenu(self.window, self.inputType, "Text Input", "Time Input", "Date Input", "Slider",
                                      "DropDown", "Radio Button", "Checkbox", "Image Upload", "Location Input")
        self.inputSelect.grid(row=2, column=1, columnspan=2)
        self.inputSelect.config(font=('Roboto', 7), indicator=0, bd=0, image=img6, text="Input options", compound=CENTER, bg="#607D8B", activebackground="#97c7f1", highlightthickness=0)
        self.addInput = Button(self.window)
        self.addInput["text"] = "Add Input"
        self.addInput["command"] = self.addBox
        #self.addInput["command"] = self.addBox
        self.addInput.config(image=img1, bg="#607D8B", activebackground="#97c7f1", bd=0)
        self.addInput.grid(row=3, column=1, columnspan=2)
        #self.addInput.pack(side="top", pady=4)

        self.topFrame = Label(self.window, text="Title:", underline=True, font="Helvetica 14", fg="white")
        self.topFrame['bg'] = "#607D8B"
        f = font.Font(self.topFrame, self.topFrame.cget("font"))
        f.configure(underline = True)
        self.topFrame.configure(font=f)
        self.topFrame.grid(row=4, column=1, columnspan=2, pady=6)

        self.titleEntry = Entry(self.window)
        self.titleEntry.config(bg= "white")
        self.titleEntry.insert(END, "Enter a title")
        self.titleEntry.grid(row=5, column=1, columnspan=2, pady=6)

        self.topFrame = Label(self.window, text="Inputs:", underline=True, font="Helvetica 14", fg="white")
        self.topFrame['bg'] = "#607D8B"
        f = font.Font(self.topFrame, self.topFrame.cget("font"))
        f.configure(underline = True)
        self.topFrame.configure(font=f)
        self.topFrame.grid(row=6, column=1, columnspan=2, pady=6)
        
        self.frame1 = Frame(self.window, bg="#607D8B", highlightbackground="black", highlightcolor="black", highlightthickness=1, bd=4)
        
        self.restoreState(self.x)
        


    # Edit the ui
    def pickStyle(self):
        self.styleWindow = Toplevel(root)
        self.applyStyles = Button(self.styleWindow)
        self.styleWindow["bg"] = "#607D8B"
        width = 350
        height = 300
        x = (self.styleWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (self.styleWindow.winfo_screenheight() // 2) - (height // 2)
        self.styleWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        self.topFrame = Label(self.styleWindow, text="Change Style", underline=True, font="Helvetica 14", fg="white")
        self.topFrame['bg'] = self.topFrame.master['bg']
        f = font.Font(self.topFrame, self.topFrame.cget("font"))
        f.configure(underline = True)
        self.topFrame.configure(font=f)
        self.topFrame.pack(side="top", padx=10, pady=10)

        
        self.applyStyles["text"] = "Refresh localhost"
        self.applyStyles["command"] = self.changeStyle
        
        self.applyStyles.config(image=img5, bg="#607D8B", bd=0)

        self.applyStyles.pack(side="top", pady=4)
        self.colorButton = Button(self.styleWindow)
        self.colorButton.config(image=img13, bg="#607D8B", bd=0)
        self.colorButton["command"] = self.chooseColor
        self.colorButton.pack(side="top", pady=4)

        self.fontcolorButton = Button(self.styleWindow)
        self.fontcolorButton.config(image=img14, bg="#607D8B", bd=0)
        self.fontcolorButton["command"] = self.choosefontColor
        self.fontcolorButton.pack(side="top", pady=4)

        self.styleType = StringVar(self.styleWindow)
        self.styleType.set("Georgia")  # default value

        self.styleSelect = OptionMenu(self.styleWindow, self.styleType, "Georgia", "Times New Roman", "Courier New", "Arial", "Candara", "Century Gothic")
        self.styleSelect.config(font=('Roboto', 7), indicator=0, bd=0, image=img6, compound=CENTER, bg="#607D8B", activebackground="#97c7f1", highlightthickness=0)

        self.styleSelect.pack(side="top")

    # Save generated inputs to file
    def changeStyle(self):
        with open('font.json', 'w') as outfile:
            style = self.styleType.get()
            if style == "Georgia":
                font = "Georgia"
            elif style == "Times New Roman":
                font = "Times New Roman"
            elif style == "Arial":
                font = "Arial"
            elif style == "Courier New":
                font = "Courier New"
            elif style == "Candara":
                font = "Candara"
            elif style == "Century Gothic":
                font = "Century Gothic"
            data = ({'font': font})
            json.dump(data, outfile)
                                         
    # Choose a color from an askcolor widget
    def chooseColor(self):
        color = askcolor(parent=self)
        with open('color.json', 'w') as outfile:
            data = ({'color': color[1]})
            json.dump(data, outfile)
                                         
    # Choose a font color from an askcolorwidget
    def choosefontColor(self):
        fontcolor = askcolor(parent=self)
        with open('fontcolor.json', 'w') as outfile:
            data = ({'fontcolor': fontcolor[1]})
            json.dump(data, outfile)

    # Set the slider range
    def setRange(self):
        # Reset range values
        self.rangeMin = 0
        self.rangeMax = 100
        self.rangeLab = ""

        self.rangeLabelFrame = Frame(self.rangeWindow)
        self.rangeLabelFrame.pack(side="top")

        self.minframe = Frame(self.rangeWindow)
        self.minframe.pack(side="top")

        self.maxframe = Frame(self.rangeWindow)
        self.maxframe.pack(side="top")

        self.rangeLabel = Label(self.rangeLabelFrame, text="Range Name: ")
        self.rangeLabel.pack(side="left")
        self.rangeName = Entry(self.rangeLabelFrame)
        self.rangeName.pack(side="right")
        self.rangeLabel.config(bg= "#607D8B")

        self.minLabel = Label(self.minframe, text="Minimum Value: ")
        self.minLabel.pack(side="left")
        self.min = Entry(self.minframe)
        self.min.pack(side="right")
        self.minLabel.config(bg= "#607D8B")

        self.maxLabel = Label(self.maxframe, text="Maximum Value: ")
        self.maxLabel.pack(side="left")
        self.max = Entry(self.maxframe)
        self.max.pack(side="right")
        self.maxLabel.config(bg= "#607D8B")

        self.QUIT = Button(self.rangeWindow, text="Save",
                           command=self.saveRange)
        self.QUIT.config(image=img8, bg="#607D8B", bd=0)
        self.QUIT.pack(side="bottom")

    def saveRange(self):
        self.rangeMin = int(self.min.get())
        self.rangeMax = int(self.max.get())
        self.rangeLab = self.rangeName.get()
        if (self.rangeMin < self.rangeMax):
            self.rangeWindow.destroy()
        else:
            print("Invalid Range")

    def setName(self):
        
        self.nameLab = ""

        self.nameLabelFrame = Frame(self.nameWindow)
        self.nameLabelFrame.pack(side="top")

        self.nameLabel = Label(self.nameLabelFrame, text="Name: ")
        self.nameLabel.pack(side="left")
        self.nameName = Entry(self.nameLabelFrame)
        self.nameName.pack(side="right")
        self.nameLabel.config(bg= "#607D8B")


        self.QUIT = Button(self.nameWindow, text="Save",
                           command=self.saveName)
        self.QUIT.config(image=img8, bg="#607D8B", bd=0)
        self.QUIT.pack(side="bottom")

    def saveName(self):
        self.nameLab = self.nameName.get()
        self.nameWindow.destroy()

    def setOptions(self):
        # Reset range values
        self.options.clear()
        self.optionEntries.clear()
        self.rangeNameFrame = Frame(self.optionsWindow)
        self.rangeNameFrame.pack(side="top")
        self.numOptionsFrame = Frame(self.optionsWindow)
        self.numOptionsFrame.pack(side="top")

        self.dropLab = Label(self.rangeNameFrame, text="Label: ")
        self.dropLab.pack(side="left")
        self.dropName = Entry(self.rangeNameFrame)
        self.dropName.pack(side="right")
        self.dropLab.config(bg= "#607D8B")

        self.numOpLabel = Label(self.numOptionsFrame, text="Number of Options: ")
        self.numOpLabel.pack(side="left")
        self.numOptions = Entry(self.numOptionsFrame)
        self.numOptions.pack(side="right")
        self.numOpLabel.config(bg= "#607D8B")

        self.addOptions = Button(self.optionsWindow, text="Add Options",
                                 command=self.addOptionBoxes)
        self.addOptions.config(image=img7, bg="#607D8B", bd=0)
        self.addOptions.pack()

    def addOptionBoxes(self):
        for i in range(int(self.numOptions.get())):
            ent = Entry(self.optionsWindow)
            self.optionEntries.append(ent)
            ent.pack(side="top")
        save = Button(self.optionsWindow, text="Save Options", command=self.saveOptions)
        save.config(image=img8, bg="#607D8B", bd=0)
        save.pack(side="bottom")

    def saveOptions(self):
        self.dropLab = self.dropName.get()
        for ent in self.optionEntries:
            self.options.append(ent.get())
        if len(self.options) > 0:
            self.optionsWindow.destroy()

    # Create a window to allow the user to change the background on homepage
    # User must include a URL that can link to an image on the internet 
    def changeWindow(self):
        self.bgWindow = Toplevel(root)
        self.bgWindow["bg"] = "#607D8B"
        width = 360
        height = 175
        x = (self.bgWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (self.bgWindow.winfo_screenheight() // 2) - (height // 2)
        self.bgWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.topFrame = Label(self.bgWindow, text="Change Background", underline=True, font="Helvetica 14", fg="white")
        self.topFrame['bg'] = self.topFrame.master['bg']
        f = font.Font(self.topFrame, self.topFrame.cget("font"))
        f.configure(underline = True)
        self.topFrame.configure(font=f)
        self.topFrame.grid(row=0, column=1)

        self.bgWindow.grid_rowconfigure(1, weight=0)
        self.bgWindow.grid_columnconfigure(1, weight=1)

        self.my_label = Label(self.bgWindow, text = "Image URL:", bg= "#607D8B")
        self.my_label.grid(row = 2, column = 0)
        self.my_entry5 = Entry(self.bgWindow, textvariable=1)
        self.my_entry5.grid(row = 2, column = 1, pady=5, ipady=10)
        self.my_button = Button(self.bgWindow, bd=0, bg="#607D8B", image=img5, command = self.changeBackground)
        self.my_button.grid(row = 3, column = 1, pady=5)

    # Method to actually change the json file where the background image is held
    def changeBackground(self):
        
        # Split the filepath to get the directory
        url = str(self.my_entry5.get())
        with open('background.json', 'w') as outfile:
            data = ({'url': url})
            json.dump(data, outfile)
                                         
    # Create a window to allow the user to change the lower text on the homepage
    # Title text must be a max of 50 characters
    def textWindow(self):
        self.bgWindow = Toplevel(root)
        self.bgWindow["bg"] = "#607D8B"
        width = 420
        height = 280
        x = (self.bgWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (self.bgWindow.winfo_screenheight() // 2) - (height // 2)
        self.bgWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.topFrame = Label(self.bgWindow, text="Change Lower Text", underline=True, font="Helvetica 14", fg="white")
        self.topFrame['bg'] = self.topFrame.master['bg']
        f = font.Font(self.topFrame, self.topFrame.cget("font"))
        f.configure(underline = True)
        self.topFrame.configure(font=f)
        self.topFrame.grid(row=0, column=1)

        self.bgWindow.grid_rowconfigure(1, weight=0)
        self.bgWindow.grid_columnconfigure(1, weight=1)

        self.my_label1 = Label(self.bgWindow, text = "Title Text: \n(Max 50 characters)", bg= "#607D8B")
        self.my_label1.grid(row = 2, column = 0)
        self.my_entry3 = Entry(self.bgWindow, textvariable=1)
        self.my_entry3.grid(row = 2, column = 1, pady=5, ipady=10)
        self.my_label = Label(self.bgWindow, text = "Text:", bg= "#607D8B")
        self.my_label.grid(row = 3, column = 0)
        self.my_entry4 = ScrolledText(self.bgWindow, width=50, height=5)
        self.my_entry4.grid(row = 3, column = 1, pady=5)
        self.my_button = Button(self.bgWindow, bg="#607D8B", bd=0, image=img5, command = self.textChange)
        self.my_button.grid(row = 4, column = 1, pady=5)

    #Method to actually change the json file holding the text 
    def textChange(self):
        
        text = str(self.my_entry3.get())
        text1 = str(self.my_entry4.get("1.0", END))
        if text1 == "\n" or text1 == "":
            text1 = "Please enter any information here."
        if text == "\n" or text == "":
            text = "Please enter any information here."
        with open('about.json', 'w') as outfile:
            data = ({'text': text})
            json.dump(data, outfile)
        print (text1)
        with open('about2.json', 'w') as outfile:
            data = ({'text2': text1})
            json.dump(data, outfile)

    def codeWindow(self):
        self.bgWindow = Toplevel(root)
        self.bgWindow["bg"] = "#607D8B"
        width = 330
        height = 170
        x = (self.bgWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (self.bgWindow.winfo_screenheight() // 2) - (height // 2)
        self.bgWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.topFrame = Label(self.bgWindow, text="Change Admin Access Code", underline=True, font="Helvetica 14", fg="white")
        self.topFrame['bg'] = self.topFrame.master['bg']
        f = font.Font(self.topFrame, self.topFrame.cget("font"))
        f.configure(underline = True)
        self.topFrame.configure(font=f)
        self.topFrame.grid(row=0, column=1)

        self.bgWindow.grid_rowconfigure(1, weight=0)
        self.bgWindow.grid_columnconfigure(1, weight=1)

        self.my_label20 = Label(self.bgWindow, text = "Access Code: ", bg= "#607D8B")
        self.my_label20.grid(row = 2, column = 0)
        self.my_entry20 = Entry(self.bgWindow, textvariable=1)
        self.my_entry20.grid(row = 2, column = 1, pady=5, ipady=10)
        self.my_button = Button(self.bgWindow, bg="#607D8B", bd=0, image=img5, command = self.textChange)
        self.my_button.grid(row = 4, column = 1, pady=5)

    #Method to actually change the json file holding the text 
    def codeChange(self):
        
        adminCode = str(self.my_entry20.get())
        
        if adminCode == "\n" or adminCode == "":
            adminCode = "admin1234"
        
        with open('access.json', 'w') as outfile:
            data = ({'adminAcc': adminCode})
            json.dump(data, outfile)

    def apiWindow(self):
        self.bgWindow = Toplevel(root)
        self.bgWindow["bg"] = "#607D8B"
        width = 330
        height = 170
        x = (self.bgWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (self.bgWindow.winfo_screenheight() // 2) - (height // 2)
        self.bgWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.topFrame = Label(self.bgWindow, text="Add apiURL link", underline=True, font="Helvetica 14", fg="white")
        self.topFrame['bg'] = self.topFrame.master['bg']
        f = font.Font(self.topFrame, self.topFrame.cget("font"))
        f.configure(underline = True)
        self.topFrame.configure(font=f)
        self.topFrame.grid(row=0, column=1)

        self.bgWindow.grid_rowconfigure(1, weight=0)
        self.bgWindow.grid_columnconfigure(1, weight=1)

        self.my_label21 = Label(self.bgWindow, text = "Paste apiURL: ", bg= "#607D8B")
        self.my_label21.grid(row = 2, column = 0)
        self.my_entry21 = Entry(self.bgWindow, textvariable=1)
        self.my_entry21.grid(row = 2, column = 1, pady=5, ipady=10)
        self.my_button = Button(self.bgWindow, bg="#607D8B", bd=0, image=img5, command = self.textChange)
        self.my_button.grid(row = 4, column = 1, pady=5)

    #Method to actually change the json file holding the text 
    def apiChange(self):
        
        apiCode = str(self.my_entry21.get())
        
        if apiCode == "\n" or apiCode == "":
            apiCode = "http://localhost:4000"
        
        with open('apiurl.json', 'w') as outfile:
            data = ({'apiLink': apiCode})
            json.dump(data, outfile)

    # Create a window to allow the user to change the lower image on homepage
    # User must include a URL that can link to an image on the internet
    # Image title must be a maximum of 50 characters
    def imageWindow(self):
        self.bgWindow = Toplevel(root)
        self.bgWindow["bg"] = "#607D8B"
        width = 450
        height = 260
        x = (self.bgWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (self.bgWindow.winfo_screenheight() // 2) - (height // 2)
        self.bgWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.topFrame = Label(self.bgWindow, text="Change Lower Image", underline=True, font="Helvetica 14", fg="white")
        self.topFrame['bg'] = self.topFrame.master['bg']
        f = font.Font(self.topFrame, self.topFrame.cget("font"))
        f.configure(underline = True)
        self.topFrame.configure(font=f)
        self.topFrame.grid(row=0, column=1)

        self.bgWindow.grid_rowconfigure(1, weight=0)
        self.bgWindow.grid_columnconfigure(1, weight=1)

        
        self.my_label1 = Label(self.bgWindow, text = "Image title: \n(Max 50 characters)", bg= "#607D8B")
        self.my_label1.grid(row = 2, column = 0)
        self.my_entry1 = Entry(self.bgWindow)
        self.my_entry1.grid(row = 2, column = 1, pady=5, ipady=10)
        self.my_label = Label(self.bgWindow, text = "Image URL:", bg= "#607D8B")
        self.my_label.grid(row = 3, column = 0)
        self.my_entry = Entry(self.bgWindow)
        self.my_entry.grid(row = 3, column = 1, pady=5)
        self.my_label7 = Label(self.bgWindow, text = "Or", bg= "#607D8B", fg="white")
        self.my_label7.grid(row = 4, column = 1)
        self.my_label9 = Label(self.bgWindow, text = "Text:", bg= "#607D8B")
        self.my_label9.grid(row = 5, column = 0)
        self.my_entry8 = Entry(self.bgWindow)
        self.my_entry8.grid(row = 5, column = 1, pady=5)
        self.my_button = Button(self.bgWindow, bg="#607D8B", bd=0, image=img5, command = self.imageChange)
        self.my_button.grid(row = 6, column = 1, pady=5)

    #Method to actually change the json file of the lower image
    def imageChange(self):
        text1 = str(self.my_entry1.get())
        text3 = str(self.my_entry8.get())
        if text1 == "\n" or text1 == "":
            text1 = "Please enter any information here."
        image = str(self.my_entry.get())
        with open('about1.json', 'w') as outfile:
            data = ({'text1': text1})
            json.dump(data, outfile)
        #if (text3 == "\n" or text3 == "") and (image != "\n" or image != ""):
            with open('image.json', 'w') as outfile:
                data = ({'image': image})
                json.dump(data, outfile)
        #if (text3 != "\n" or text3 != "") and (image == "\n" or image == ""):
            with open('about4.json', 'w') as outfile:
                data = ({'text4': text3})
                json.dump(data, outfile)
    # Generate all widgets used on the ui
    def createWidgets(self):
    

        self.editUI = Button(self)
        self.editUI.config(image=img3, text="Edit Interface", bd=0, bg="#607D8B", activebackground="#97c7f1")
        #self.editUI["text"] = "Edit UI"
        self.editUI["command"] = self.makeEdits
        self.editUI.grid(row =5, column=0,sticky="NSEW")

        self.chooseStyles = Button(self)
        self.chooseStyles.config(image=img2, bd=0, bg="#607D8B", activebackground="#97c7f1")
        #self.chooseStyles["text"] = "Change Style"
        self.chooseStyles["command"] = self.pickStyle
        self.chooseStyles.grid(row =6, column=0,sticky="NSEW")

        self.codeText = Button(self)
        self.codeText.config(image=img15, bd=0, bg="#607D8B")
        self.codeText["command"] = self.codeWindow
        self.codeText.grid(row=7, column=0, sticky="NSEW")

        self.apiText = Button(self)
        self.apiText.config(image=img17, bd=0, bg="#607D8B")
        self.apiText["command"] = self.apiWindow
        self.apiText.grid(row=8, column=0, sticky="NSEW")

        self.QUIT = Button(self)
        self.QUIT["command"] = self.quit
        self.QUIT.config(image=img4, bd=0, bg="#607D8B", activebackground="#97c7f1")
        self.QUIT.grid(row =9, column=0,sticky="NSEW")

        self.changeBG = Button(self)
        self.changeBG.config(image=img10, bd=0, bg="#607D8B")
        self.changeBG["command"] = self.changeWindow
        self.changeBG.grid(row=4, column=0, sticky="NSEW")

        self.changeText = Button(self)
        self.changeText.config(image=img11, bd=0, bg="#607D8B")
        self.changeText["command"] = self.textWindow
        self.changeText.grid(row=3, column=0, sticky="NSEW")

        self.changeImage = Button(self)
        self.changeImage.config(image=img12, bd=0, bg="#607D8B")
        self.changeImage["command"] = self.imageWindow
        self.changeImage.grid(row=2, column=0, sticky="NSEW")
        
app = Application(master=root)
app.mainloop()
