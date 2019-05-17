from tkinter import *
import json
import socket
import os
import signal


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.all_entries = []  # Maintain a list of all inputs for the ui
        self.all_deletes = []  # Maintain a list of all deletes for the ui
        self.p = None  # When localhost is started, keep track of that process so it can be killed later
        self.pack()
        self.createWidgets()
        self.window = None  # 2nd window for ui editing
        self.inputType = ""
        self.styleWindow = None  # 3rd window for style editing
        self.styleType = ""

        self.rangeWindow = None  # Window for slider range input
        self.rangeMin = 0  # Min value for slider
        self.rangeMax = 100  # Max value for slider
        self.rangeLab = ""  # Label For the Slider

        self.optionsWindow = None  # Window for options input
        self.optionEntries = []  # List of options entry boxes
        self.options = []  # List of options
        self.dropLab = ""

    # When the ui is being edited, show the current state of the ui before editing begins, get state from the data.json file
    def restoreState(self):
        if os.path.getsize(
                "./data.json") > 2:  # If there are no inputs in the file, the file contains an empty array [] which has size 2
            with open('data.json', 'r') as infile:
                json_array = json.load(infile)
                for item in json_array:
                    self.restoreBox(item)

    # Save contents of the database to a csv file
    def databaseDump(self):
        from subprocess import Popen
        Popen([
                  "mongoexport -h ds143143.mlab.com:43143 -d ocean-eyes -c fishdata -u admin -p admin22 -o ./fishdata.csv --type=csv -f 'userId,location,conditions,date,catch_size'"],
              shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    # Add box method to handle restoring state
    def restoreBox(self, item):
        inputName = item['label']
        thisType = item['type']
        options = []
        if thisType == "":
            inputType = ""
            className = ""
            ent = Entry(self.window)
            ent.insert(END, inputName)
        elif thisType == "time":
            inputType = "time"
            className = ""
            ent = Entry(self.window)
            ent.insert(END, "time")
            ent.config(state=DISABLED)
        elif thisType == "date":
            inputType = "date"
            className = ""
            ent = Entry(self.window)
            ent.insert(END, "date")
            ent.config(state=DISABLED)
        elif thisType == "range":
            inputType = "range"
            className = "slider"
            ent = Scale(self.window, orient=HORIZONTAL, from_=item['min'], to=item['max'])
        elif thisType == "select":
            inputType = "select"
            className = ""
            for option in item['options']:
                options.append(option['value'])
            variable = StringVar(self.window)
            variable.set(options[0])  # default value
            ent = OptionMenu(self.window, variable, *options)
        elif thisType == "radio":
            inputType = "radio"
            className = ""
            for option in item['options']:
                options.append(option['value'])
            ent = Radiobutton(self.window, text="Radio Button Group")
        elif thisType == "checkbox":
            inputType = "checkbox"
            className = ""
            for option in item['options']:
                options.append(option['value'])
            ent = Checkbutton(self.window, text="Check Button Group")
        elif thisType == "map":
            inputType = "map"
            className = ""
            ent = Label(self.window, text="Location Select Widget")
        elif thisType == "imageUpload":
            inputType = "imageUpload"
            className = ""
            ent = Label(self.window, text="Image Upload")
        else:
            inputType = ""
            className = ""
            ent = Entry(self.window)
            ent.insert(END, textString)

        index = len(self.all_entries)
        ent.pack(side="top")
        self.all_entries.append((ent, inputType, className, item['min'], item['max'], inputName, options))
        remove = Button(self.window, text='X', fg="Red", command=lambda i=index: self.removeBox(i))
        remove.pack(side="top")
        self.all_deletes.append(remove)

    # Create a new input
    def addBox(self, textString=""):
        inputName = ""
        thisType = self.inputType.get()
        if thisType == "Text Input":
            inputType = ""
            className = ""
            ent = Entry(self.window)
            ent.insert(END, textString)
        elif thisType == "Time Input":
            inputType = "time"
            className = ""
            ent = Entry(self.window)
            ent.insert(END, "Time")
            ent.config(state=DISABLED)
        elif thisType == "Date Input":
            inputType = "date"
            className = ""
            ent = Entry(self.window)
            ent.insert(END, "Date")
            ent.config(state=DISABLED)
        elif thisType == "Slider":
            self.rangeWindow = Toplevel()
            self.setRange()
            root.wait_window(self.rangeWindow)
            inputType = "range"
            className = "slider"
            inputName = self.rangeLab
            ent = Scale(self.window, orient=HORIZONTAL, from_=self.rangeMin, to=self.rangeMax)
        elif thisType == "DropDown":
            self.optionsWindow = Toplevel()
            self.setOptions()
            root.wait_window(self.optionsWindow)
            inputType = "select"
            className = ""
            inputName = self.dropLab
            variable = StringVar(self.window)
            variable.set(self.options[0])  # default value
            ent = OptionMenu(self.window, variable, *self.options)
        elif thisType == "Radio Button":
            self.optionsWindow = Toplevel()
            self.setOptions()
            root.wait_window(self.optionsWindow)
            inputType = "radio"
            className = ""
            ent = Radiobutton(self.window, text="Radio Button Group")
            ent.pack(side="top")
        elif thisType == "Checkbox":
            self.optionsWindow = Toplevel()
            self.setOptions()
            root.wait_window(self.optionsWindow)
            inputType = "checkbox"
            className = ""
            ent = Checkbutton(self.window, text="Check Button Group")
            ent.pack(side="top")
        elif thisType == "Image Upload":
            inputType = "imageUpload"
            className = ""
            ent = Label(self.window, text="Image Upload Widget")
        elif thisType == "Location Input":
            inputType = "map"
            className = ""
            ent = Label(self.window, text="Location Select Widget")
        else:
            inputType = ""
            className = ""
            ent = Entry(self.window)
            ent.insert(END, textString)

        index = len(self.all_entries)
        ent.pack(side="top")
        options = self.options.copy()
        self.all_entries.append((ent, inputType, className, self.rangeMin, self.rangeMax, inputName, options))
        remove = Button(self.window, text='X', fg="Red", command=lambda i=index: self.removeBox(i))
        remove.pack(side="top")
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

    # Edit the ui
    def makeEdits(self):
        self.window = Toplevel(root)
        self.window.protocol("WM_DELETE_WINDOW", self.onWindowClose)
        self.refresh_server = Button(self.window)

        self.refresh_server["text"] = "Refresh localhost"
        self.refresh_server["command"] = self.createInputs
        self.refresh_server.pack(side="top")

        self.inputType = StringVar(self.window)
        self.inputType.set("Text Input")  # default value

        self.inputSelect = OptionMenu(self.window, self.inputType, "Text Input", "Time Input", "Date Input", "Slider",
                                      "DropDown", "Radio Button", "Checkbox", "Image Upload", "Location Input")
        self.inputSelect.pack(side="top")
        self.addInput = Button(self.window)
        self.addInput["text"] = "Add Input"
        self.addInput["command"] = self.addBox
        self.addInput.pack(side="top")

        self.restoreState()

    # Edit the ui
    def pickStyle(self):
        self.styleWindow = Toplevel(root)
        self.applyStyles = Button(self.styleWindow)

        self.applyStyles["text"] = "Refresh localhost"
        self.applyStyles["command"] = self.changeStyle
        self.applyStyles.pack(side="top")

        self.styleType = StringVar(self.styleWindow)
        self.styleType.set("Style 1")  # default value

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

        self.minLabel = Label(self.minframe, text="Minimum Value: ")
        self.minLabel.pack(side="left")
        self.min = Entry(self.minframe)
        self.min.pack(side="right")

        self.maxLabel = Label(self.maxframe, text="Maximum Value: ")
        self.maxLabel.pack(side="left")
        self.max = Entry(self.maxframe)
        self.max.pack(side="right")

        self.QUIT = Button(self.rangeWindow, text="Save",
                           command=self.saveRange)
        self.QUIT.pack(side="bottom")

    def saveRange(self):
        self.rangeMin = int(self.min.get())
        self.rangeMax = int(self.max.get())
        self.rangeLab = self.rangeName.get()
        if (self.rangeMin < self.rangeMax):
            self.rangeWindow.destroy()
        else:
            print("Invalid Range")

    def setOptions(self):
        # Reset range values
        self.options.clear()
        self.optionEntries.clear()
        self.rangeNameFrame = Frame(self.optionsWindow)
        self.rangeNameFrame.pack(side="top")
        self.numOptionsFrame = Frame(self.optionsWindow)
        self.numOptionsFrame.pack(side="top")

        self.dropLab = Label(self.rangeNameFrame, text="DropDown Label: ")
        self.dropLab.pack(side="left")
        self.dropName = Entry(self.rangeNameFrame)
        self.dropName.pack(side="right")

        self.numOpLabel = Label(self.numOptionsFrame, text="Number of Options: ")
        self.numOpLabel.pack(side="left")
        self.numOptions = Entry(self.numOptionsFrame)
        self.numOptions.pack(side="right")

        self.addOptions = Button(self.optionsWindow, text="Add Options",
                                 command=self.addOptionBoxes)
        self.addOptions.pack()

    def addOptionBoxes(self):
        for i in range(int(self.numOptions.get())):
            ent = Entry(self.optionsWindow)
            self.optionEntries.append(ent)
            ent.pack(side="top")
        save = Button(self.optionsWindow, text="Save Options", command=self.saveOptions)
        save.pack(side="bottom")

    def saveOptions(self):
        self.dropLab = self.dropName.get()
        for ent in self.optionEntries:
            self.options.append(ent.get())
        if len(self.options) > 0:
            self.optionsWindow.destroy()

    # Generate all widgets used on the ui
    def createWidgets(self):

        self.upload = Button(self)
        self.upload["text"] = "Upload Files to server"
        self.upload["command"] = self.uploadToServer
        self.upload.pack(side="top")

        # self.dataDump = Button(self)
        # self.dataDump["text"] = "Dump contents of database to csv file"
        # self.dataDump["command"] = self.databaseDump
        # self.dataDump.pack(side="top")

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
root.title("Citizen Science Web Portal")
root.update_idletasks()
width = 400
height = 400
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

app = Application(master=root)
app.mainloop()

