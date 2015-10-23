import xml.etree.cElementTree as ET
import tkinter as tk
from tkinter import ttk as ttk
from tkinter import N, W, E, S

class NotesWriter(tk.Frame):
        def __init__(self, master=None):
                #Setup UI Tk Frame
                ttk.Frame.__init__(self, master, padding = "10 5 12 12")
                self.grid(column=0, row=0, sticky=(N, W, E, S))
                self.columnconfigure(0, weight=1)
                self.rowconfigure(0,weight=1)
                
                #Initialize Input Variable Bindings
                self.title = tk.StringVar()
                self.id = tk.StringVar()
                self.body = tk.StringVar()
                self.srcNote = tk.StringVar()
                self.srcLink = tk.StringVar()
                self.tTags = tk.StringVar()
                self.cTags = tk.StringVar()
                self.sTags = tk.StringVar()

                self.createWidgets()


        def createWidgets(self):
                ttk.Label(self, text="Title").grid(column = 1, row=1, sticky=W)
                self.titleEntry = ttk.Entry(self, width = 35, textvariable = self.title)
                self.titleEntry.grid(column = 1, row = 2, columnspan = 3, sticky=(W,E))

                ttk.Label(self, text="ID").grid(column=5, row=1, sticky=W)
                self.idEntry = ttk.Entry(self, width = 35, textvariable = self.id)
                self.idEntry.grid(column = 5, row = 2, sticky=(W,E))

                ttk.Label(self, text="Enter note").grid(column=1, row=3, sticky=W)
                self.bodyText = tk.Text(self)
                self.bodyText.grid(column = 1, row = 4, columnspan = 5, sticky=(N,W,E,S))

                ttk.Label(self, text="Enter Source Link").grid(column=1, row=5, sticky=W)
                self.srcLinkEntry = ttk.Entry(self, width = 35, textvariable = self.srcLink)
                self.srcLinkEntry.grid(column = 1, row = 6, columnspan = 5, sticky=(W,E))

                ttk.Label(self, text="Enter Source Notes").grid(column=1, row=7, sticky=W)
                self.srcNoteEntry = ttk.Entry(self, width = 35, textvariable = self.srcNote)
                self.srcNoteEntry.grid(column = 1, row = 8, columnspan = 5, sticky=(W,E))

                ttk.Label(self, text="Enter Client Tags").grid(column=1, row=9, sticky=W)
                self.cTagsEntry = ttk.Entry(self, width = 35, textvariable = self.cTags)
                self.cTagsEntry.grid(column = 1, row = 10, sticky=(W,E))

                ttk.Label(self, text="Enter Topic Tags").grid(column=3, row=9, sticky=W)
                self.tTagsEntry = ttk.Entry(self, width = 35, textvariable = self.tTags)
                self.tTagsEntry.grid(column = 3, row = 10, sticky=(W,E))

                ttk.Label(self, text="Enter Study Tags").grid(column=5, row=9, sticky=W)
                self.sTagsEntry = ttk.Entry(self, width = 35, textvariable = self.sTags)
                self.sTagsEntry.grid(column = 5, row = 10, sticky=(W,E))

                self.saveButton = tk.Button(self, text='Save', fg = "green", width = 35, command=self.save)
                self.saveButton.grid(column = 5, row=11, sticky=(E))
                
                self.clearButton = tk.Button(self, text='Clear', fg = "blue", width = 35, command=self.clear)
                self.clearButton.grid(column = 3, row=11)
                
                self.quitButton = tk.Button(self, text='Quit', width = 35, command=self.quit)
                self.quitButton["fg"] = "red"
                self.quitButton.grid(column = 1, row=11, sticky=(W))

                for child in self.winfo_children(): child.grid_configure(padx=5, pady=5)


        def save(self):
                print("Body text: %s." % self.bodyText.get("1.0",'end-1c'))

        def quit(self):
                pass

        def clear(self):
                self.title = ""
                self.id = ""
                self.bodyText.delete("1.0",'end')
                self.srcNote = ""
                self.srcLink = ""
                self.tTags = ""
                self.cTags = ""
                self.sTags = ""

class XMLNoteWriter:
        def __init__(self, path = None):
                self.tree = ET.ElementTree()
                if path != None:
                        self.tree.parse(path)
                        self.NoteParent = self.tree.getroot()
                else:
                        self.NoteParent = self.tree.Element("NOTES")
        
        def writeNote(sTitle,sId,sBody,sSrcNote,sSrcLink,sTTags,sCTags,sSTags):
                ET.SubElement(self.NoteParent, 'TOPIC') ID
                ET.SubElement(self.NoteParent, 'BODY')
                ET.SubElement(self.NoteParent, 'XREF')
                ET.SubElement(self.NoteParent, 'T_TAGS')
                ET.SubElement(self.NoteParent, 'C_TAGS')
                ET.SubElement(self.NoteParent, 'S_TAGS')
                ET.SubElement(self.NoteParent, 'DATE')
                
        def saveNote:
                pass
        
        
root = tk.Tk()
root.title("XML Note Taker v0.0")
app = NotesWriter(root)
#app.master.maxsize(800,800)
app.mainloop()
