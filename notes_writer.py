import xml.etree.ElementTree as ET
import tkinter as tk
from datetime import datetime
from tkinter import ttk as ttk
from tkinter import N, W, E, S
import xml.dom.minidom as minidom
import re

CONFIG_REL_PATH = 'ConfigXMLNotes.xml'
 

class NotesWriter(tk.Frame):
        def __init__(self, master=None):
                #Setup UI Tk Frame
                ttk.Frame.__init__(self, master, padding = "10 5 12 12")
                self.grid(column=0, row=0, sticky=(N, W, E, S))
                self.columnconfigure(0, weight=1)
                self.rowconfigure(0,weight=1)
                
                #Initialize Input Variable Bindings
                self.topic = tk.StringVar()
                self.id = tk.StringVar()
                self.body = tk.StringVar()
                self.srcNote = tk.StringVar()
                self.srcLink = tk.StringVar()
                self.tTags = tk.StringVar()
                self.cTags = tk.StringVar()
                self.sTags = tk.StringVar()

                #Empty dict to store key to widget bindings
                self.wigKeyBindings = {}          #key string to widget object reference
                self.uiEntryDescriptions = {}     #input identifier to description string
                self.uiHotKeys = {}             #input identifier to key string

                self.readconfig()
                self.writer = XMLNoteWriter(self.path)
                self.createWidgets()


        def readconfig(self):
                self.configTree = ET.ElementTree()
                self.configTree.parse(CONFIG_REL_PATH)
                self.config = self.configTree.getroot()

                #Initialize configuration settings
                self.version = self.config.find("VERSION").text
                self.path = self.config.find("ACTIVEPATH").text
                for entry in self.config.find("HOTKEYS").findall("KEYBIND"):
                        self.uiEntryDescriptions[entry.get('id')] = entry.text
                        self.uiHotKeys[entry.get('id')] = entry.get('key')


        def activate(self, event):
                self.wigKeyBindings[event.keysym].focus()

        def execute(self, event):
                self.wigKeyBindings[event.keysym].invoke()

        def createWidgets(self):
                
                self.topicEntry = ttk.Entry(self, width = 35, textvariable = self.topic)
                self.topicEntry.grid(column = 1, row = 2, columnspan = 3, sticky=(W,E))
                self.labelAndBind('topic', self.topicEntry, self.activate).grid(column = 1, row=1, sticky=W)

                self.idEntry = ttk.Entry(self, width = 35, textvariable = self.id)
                self.idEntry.grid(column = 5, row = 2, sticky=(W,E))
                self.labelAndBind("id", self.idEntry, self.activate).grid(column=5, row=1, sticky=W)

                self.bodyText = tk.Text(self)
                self.bodyText.grid(column = 1, row = 4, columnspan = 5, sticky=(N,W,E,S))
                self.labelAndBind("body",self.bodyText, self.activate).grid(column=1, row=3, sticky=W)
                
                self.srcLinkEntry = ttk.Entry(self, width = 35, textvariable = self.srcLink)
                self.srcLinkEntry.grid(column = 1, row = 6, columnspan = 5, sticky=(W,E))
                self.labelAndBind('srcLink', self.srcLinkEntry, self.activate).grid(column=1, row=5, sticky=W)

                self.srcNoteEntry = ttk.Entry(self, width = 35, textvariable = self.srcNote)
                self.srcNoteEntry.grid(column = 1, row = 8, columnspan = 5, sticky=(W,E))
                self.labelAndBind('srcNote', self.srcNoteEntry, self.activate).grid(column=1, row=7, sticky=W)

                self.cTagsEntry = ttk.Entry(self, width = 35, textvariable = self.cTags)
                self.cTagsEntry.grid(column = 1, row = 10, sticky=(W,E))
                self.labelAndBind('cTags', self.cTagsEntry, self.activate).grid(column=1, row=9, sticky=W)

                self.tTagsEntry = ttk.Entry(self, width = 35, textvariable = self.tTags)
                self.tTagsEntry.grid(column = 3, row = 10, sticky=(W,E))
                self.labelAndBind('tTags', self.tTagsEntry, self.activate).grid(column=3, row=9, sticky=W)

                self.sTagsEntry = ttk.Entry(self, width = 35, textvariable = self.sTags)
                self.sTagsEntry.grid(column = 5, row = 10, sticky=(W,E))
                self.labelAndBind('sTags', self.sTagsEntry, self.activate).grid(column=5, row=9, sticky=W)

                self.saveButton = tk.Button(self, text='Save <Alt + {0}>'.format(self.uiHotKeys['save']), fg = "green", width = 35, command=self.save)
                self.saveButton.grid(column = 5, row=11, sticky=(E))
                self.bindIdent('save', self.saveButton, self.execute)
                
                self.clearButton = tk.Button(self, text='Clear <Alt + {0}>'.format(self.uiHotKeys['clear']), fg = "blue", width = 35, command=self.clear)
                self.clearButton.grid(column = 3, row=11)
                self.bindIdent('clear', self.clearButton, self.execute)
                
                self.quitButton = tk.Button(self, text='Quit <Alt + {0}>'.format(self.uiHotKeys['quit']), fg = "red", width = 35, command=self.quit)
                self.quitButton.grid(column = 1, row=11, sticky=(W))
                self.bindIdent('quit', self.quitButton, self.execute)

                for child in self.winfo_children(): child.grid_configure(padx=5, pady=5)

        
        def labelAndBind(self, ident, widget, funct):
                key = self.bindIdent(ident, widget, funct)
                label = ttk.Label(self, text='{0} <Alt + {1}>'.format(self.uiEntryDescriptions[ident], key))
                return label

        def bindIdent(self, ident, widget, funct):
                key = self.uiHotKeys[ident]
                self.wigKeyBindings[key] = widget
                self.bind_all('<Alt-' + key + '>',funct)
                return key

        def getVersion(self):
                return self.version

        def save(self):
                #print(self.topic.get())
                #print(self.id.get())
                #print(self.bodyText.get("1.0",'end-1c'))
                #print(self.srcNote.get())
                #print(self.srcLink.get())
                #print(self.tTags.get())
                #print(self.cTags.get())
                #print(self.sTags.get())
                self.writer.writeNote(self.topic.get(), self.id.get(), self.bodyText.get("1.0",'end-1c'),
                    self.srcNote.get(), self.srcLink.get(), self.tTags.get(),
                    self.cTags.get(), self.sTags.get())
                self.writer.saveNote()

        def quit(self):
                import sys; sys.exit() 

        def clear(self):
                self.topic = ""
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
                        self.path = path
                        self.tree.parse(path)
                        self.noteParent = self.tree.getroot()
                else:
                        self.noteParent = self.tree.Element("NOTES")

        
        def writeNote(self, sTopic,sId,sBody,sSrcNote,sSrcLink,sTTags,sCTags,sSTags):
                #TODO after simple prototype, restructure to take generic dictionary of tags, values, attributes.  should be able to recycle some of this for updating config file.
                note = ET.SubElement(self.noteParent, 'NOTE') 
                note.set('id',sId)
                elem = ET.SubElement(note, 'TOPIC')
                elem.text = sTopic
                elem = ET.SubElement(note, 'BODY')
                elem.text = sBody
                #elem = ET.SubElement(note, 'XREF')
                #elem.text = sXRef
                elem = ET.SubElement(note, 'T_TAGS')
                elem.text = sTTags
                elem = ET.SubElement(note, 'C_TAGS')
                elem.text = sCTags
                elem = ET.SubElement(note, 'S_TAGS')
                elem.text = sSTags
                elem = ET.SubElement(note, 'DATE')
                elem.text = datetime.today().strftime('%m/%d/%Y')
                
                
        def saveNote(self):
                rough_xml = ET.tostring(self.noteParent, 'utf-8')
                reparsed_xml = minidom.parseString(rough_xml).toprettyxml(indent="\t")
                reparsed_xml = re.sub(r'\n[ |\t|\n]*\n',r'\n',reparsed_xml)  #remove blank rows
                with open(self.path, "w") as text_file:
                        print(reparsed_xml, file=text_file)

root = tk.Tk()

app = NotesWriter(root)
root.title("XML Note Taker " + app.getVersion())
app.mainloop()
