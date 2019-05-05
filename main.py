from tkinter import *
from tkinter import ttk
from idlelib.textview import view_text
from idlelib.colorizer import ColorDelegator, color_config
from idlelib.percolator import Percolator
from subprocess import run
import os
import webbrowser
import shutil
from tkinter import filedialog
from tkinter import messagebox



LABELFONT = ("Fixedsys", 13)
MENUFONT = ("Ebrima", 11)
ENTRYFONT = ("Courier", 10)
BUTTONFONT = ("Dotum", 12)

py2to3pPath = os.path.abspath("utils\\2to3.exe")
python_2_files = []
dest = ""
file_dir = ""
findState = DISABLED


def main():

    def convertFile():

        global new_base_dir

        if len(python_2_files)!=0:
            # if ther is a file selected...
            print("\n")

            # convert the files
            for _file in python_2_files:

                base_dir = "/".join(_file.split("/")[:-1])
                new_base_dir = base_dir +"//ConvertedFiles"
                
                # # create a Converted file and save files there
                # old_dir = os.getcwd()
                # new_dir = old_dir+"//ConvertedFiles"

                if os.path.isdir(new_base_dir)==False:
                    os.makedirs(new_base_dir)
                    print("created the convertedFiles fonder")
                else:
                    pass

                # change the working directory to Converted folder
                os.chdir(new_base_dir)

                # cpoy the file to be conerted to the convertedFiles path
                new__file_path = os.getcwd() + "/" + os.path.basename(_file)
                x = shutil.copy(_file, new__file_path)
                # convert each selected python 2 file
                command = [py2to3pPath,
                    "-w",
                    "-n",
                    x]

                run(command)
                print("done, converting : ", os.path.basename(_file))
                print("command = ", command)
            
            print("Done all operations")

            python3SrcBtn.config(state=NORMAL)
            py3Dest.set(new_base_dir)
                


    def searchFile():

        global python_2_files

        files_list = filedialog.askopenfilenames(filetypes=[("Python Files .py", ".py"),
                                                             ("Python .pyw files", ".pyw"),
                                                            ("All Files", "*")
                                                             ]
                                                )
        # print(files_list)
        
        files = []
        for i in range(len(files_list)):
            x = os.path.basename(files_list[i])
            files.append(x)
        
        python_2_files = files_list
        files = ", ".join(files)
        py2file.set(files)
        print(files)
        print(python_2_files)

        
    def openPy3Destination():

        # dest = os.open(new_base_dir)
        webbrowser.open(new_base_dir)  

        # print(dest)
    
    def convertText():

        py2Txt = python2Text.get(0.1, END)

        with open("utils\\py2.py", "w") as py2TextOb:
            py2TextOb.write(py2Txt)
        
        command = ["utils\\2to3.exe",
                    "-w",
                    "-W",
                    "-n",
                    "utils\\py2.py"
                    ]

        
        run(command)

        # print(command)

        with open("utils\\py2.py", "r") as py3TextOb:
            py2Txt = py3TextOb.read()
            python3Text.delete(0.1, END)
            python3Text.insert(0.1, py2Txt)
    
    root = Tk()
    root.title("Py2-to-Py3-Converter-GUI-tkinter")
    root.geometry("800x550")
    root.resizable(width=0, height=0)
    root.grid_rowconfigure(0, weight=1) # this needed to be added
    root.grid_columnconfigure(0, weight=1) # as did this

    #  TKINTER VARIABLES
    py2file = StringVar()
    py2file.set("")
    py3Dest = StringVar()
    py3Dest.set("")

    # the Notebook
    notebook = ttk.Notebook(root, padding=5)
    notebook.grid(sticky="nsew")
    notebook.grid_rowconfigure(0, weight=1) # this needed to be added
    notebook.grid_columnconfigure(0, weight=1) # as did this

    # file Converter tab
    filesConverterFrame = Frame(root)
    filesConverterFrame.grid(row=0, column=0, sticky="nsew")
    filesConverterFrame.grid_rowconfigure(0, weight=1) # this needed to be added
    filesConverterFrame.grid_columnconfigure(0, weight=1) # as did this
    fileConvCanv = Canvas(filesConverterFrame)
    fileConvCanv.grid(sticky="nsew")
    fileConvCanv.grid_rowconfigure(1, pad=60)
    fileConvCanv.grid_rowconfigure(2, pad=50)
    fileConvCanv.grid_rowconfigure(3, pad=50) # this needed to be added
    fileConvCanv.grid_columnconfigure(1, pad=50) # as did this

    python2Label = Label(fileConvCanv, text="Python2File:", font=LABELFONT)
    python2Label.grid(row=1, column=1)

    python3Label = Label(fileConvCanv, text="Py3FileDirectory:", font=LABELFONT)
    python3Label.grid(row=2, column=1)
    
    python2Entry = Entry(fileConvCanv, font=ENTRYFONT, width=60, textvariable=py2file)
    python2Entry.grid(row=1, column=2, sticky="w")

    python3Entry = Entry(fileConvCanv, font=ENTRYFONT, width=60, textvariable=py3Dest)
    python3Entry.grid(row=2, column=2, sticky="w")

    python2SrcBtn = Button(fileConvCanv, text="Search", font=BUTTONFONT, command=searchFile)
    python2SrcBtn.grid(row=1, column=3, padx=5)

    python3SrcBtn = Button(fileConvCanv, text="Open", font=BUTTONFONT, command=openPy3Destination, state=findState)
    python3SrcBtn.grid(row=2, column=3)

    convertBtn = Button(fileConvCanv, text="CONVERT", font=BUTTONFONT, command=convertFile)
    convertBtn.grid(row=3, column=2)

    # settingsBtn = Button(fileConvCanv, text="SS")
    # settingsBtn.grid(row=50, column=4, sticky="se")


    # raw text converter tab
    rawTextConverterFrame = Frame(bg="green")
    rawTextConverterFrame.grid(row=0, column=0, sticky="nsew")
    rawTextConverterFrame.grid_rowconfigure(0, weight=1) # this needed to be added
    rawTextConverterFrame.grid_columnconfigure(0, weight=1) # as did this
    rawTextConvCanv = Canvas(rawTextConverterFrame)
    rawTextConvCanv.grid(sticky="nsew")

    python2TextLabel = Label(rawTextConvCanv, text="Python 2 Code...")
    python2TextLabel.grid(row=1, column=1, padx=5, pady=5)

    python2Text = Text(rawTextConvCanv, width=43, wrap="none")
    Percolator(python2Text).insertfilter(ColorDelegator())
    color_config(python2Text)
    python2Text.grid(row=2, column=1, padx=5)
    # Python 3 text scrollbar
    hbar = Scrollbar(rawTextConvCanv, name='hbar', orient=HORIZONTAL)
    hbar['command'] = python2Text.xview
    hbar.grid(row=50, column=1, sticky="ew", padx=2)
    python2Text['xscrollcommand'] = hbar.set

    toTextLabel = Label(rawTextConvCanv, text=">>>")
    toTextLabel.grid(row=2, column=2, sticky="nsew")

    python3TextLabel = Label(rawTextConvCanv, text="Python 3 Code")
    python3TextLabel.grid(row=1, column=3)

    python3Text = Text(rawTextConvCanv, width=43, wrap="none")
    python3Text.insert(0.1, "print(\"Hello world\")")
    Percolator(python3Text).insertfilter(ColorDelegator())
    color_config(python3Text)
    python3Text.grid(row=2, column=3)
    # Python 3 text scrollbar
    hbar1 = Scrollbar(rawTextConvCanv, name='hbar1', orient=HORIZONTAL)
    hbar1['command'] = python3Text.xview
    hbar1.grid(row=50, column=3, sticky="ew")
    python3Text['xscrollcommand'] = hbar1.set

    convertBtnText = Button(rawTextConvCanv, text="CONVERT", command=convertText)
    convertBtnText.grid(row=3, column=2, pady=10, padx=5)


    # Notebook Adding of Tabs
    notebook.add(rawTextConverterFrame, text="Convert Raw python code")
    notebook.add(filesConverterFrame, text="Convert Files")

    notebook.select(".!frame")

    # print(notebook.tabs())


    root.mainloop()

if __name__ == "__main__":
    main()