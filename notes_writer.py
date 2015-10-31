import xml.etree.ElementTree as ET
import tkinter as tk
from datetime import datetime
from tkinter import ttk as ttk
from tkinter import N, W, E, S
import xml.dom.minidom as minidom
import re

CONFIG_REL_PATH = 'ConfigXMLNotes.xml'


class Text(tk.Text):
    def set(self, val):
        self.delete("1.0",'end')
        self.insert(tk.END,val)

    #override get to always get all text.
    def get(self):
        return super(Text, self).get("1.0",'end-1c')
 
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
                self.idParent = tk.StringVar()
                self.bodyText = Text(self)
                self.srcNote = tk.StringVar()
                self.srcLink = tk.StringVar()
                self.tTags = tk.StringVar()
                self.cTags = tk.StringVar()
                self.sTags = tk.StringVar()
                self.overwriteInd = tk.IntVar()
                self.entries = [self.topic, self.id, self.bodyText,
                            self.srcNote, self.srcLink, self.tTags,
                            self.cTags, self.sTags]

                #Empty dict to store key to widget bindings
                self.wigKeyBindings = {}          #key string to widget object reference
                self.uiEntryDescriptions = {}     #input identifier to description string
                self.uiHotKeys = {}             #input identifier to key string

                self.readconfig()
                self.writer = XMLNoteWriter(self.path)
                self.currentIDList = self.writer.getAllIDs()
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

        def toggle(self, event):
                self.wigKeyBindings[event.keysym].toggle()


        def refreshOptionMenu(self, startEntry):
                # Delete old options
                self.idParentEntry['menu'].delete(0, 'end')

                # Insert list of new options (tk._setit hooks them up to var)
                self.currentIDList = self.writer.getAllIDs()
                for choice in self.currentIDList:
                    self.idParentEntry['menu'].add_command(label=choice, command=tk._setit(self.idParent, choice))
                self.idParent.set(startEntry)

        def updateFieldsToParent(self, *args):
                note = self.writer.readNote(self.idParent.get())
                self.updateFields(note)

        def updateFields(self, loaded_inputs): 
                for i in range(0, len(self.entries)-1):
                        self.entries[i].set(loaded_inputs[i])

        def createWidgets(self):
                #TO DO:  move width, row, type, etc layout info into the configuration file.
                self.topicEntry = ttk.Entry(self, width = 35, textvariable = self.topic)
                self.topicEntry.grid(column = 1, row = 2, columnspan = 1, sticky=(W,E))
                self.labelAndBind('topic', self.topicEntry, self.activate).grid(column = 1, row=1, sticky=W)

                self.idEntry = ttk.Entry(self, width = 35, textvariable = self.id)
                self.idEntry.grid(column = 3, row = 2, sticky=(W,E))
                self.labelAndBind("id", self.idEntry, self.activate).grid(column=3, row=1, sticky=W)

                self.idParentEntry = tk.OptionMenu(self, self.idParent, *self.currentIDList)
                self.idParentEntry.grid(column = 5, row = 2, sticky=(W,E))
                self.labelAndBind("idParent", self.idParentEntry, self.activate).grid(column=5, row=1, sticky=W)
                self.idParent.trace("w",self.updateFieldsToParent)

                self.overwriteIndChkbx = tk.Checkbutton(self, text="Overwrite Note <Alt + {0}>".format(self.uiHotKeys['overwriteInd']), variable=self.overwriteInd)
                self.overwriteIndChkbx.grid(column = 5, row = 3, sticky=(W,E))
                self.bindIdent('overwriteInd', self.overwriteIndChkbx, self.toggle)

                #self.bodyText = Text(self)  => declared in init
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
                toSave = [entry.get() for entry in self.entries]
                self.writer.writeNote(self.overwriteInd.get(), *toSave)
                self.writer.saveNote()
                self.refreshOptionMenu(self.id.get())

        def quit(self):
                import sys; sys.exit() 

        def clear(self):
                self.updateFields(["" for item in range(len(self.entries))])

class XMLNoteWriter:
        def __init__(self, path = None, parent = None):
                self.tree = ET.ElementTree()
                if path != None:
                        self.path = path
                        self.tree.parse(path)
                        self.noteParent = self.tree.getroot()
                else:
                        self.noteParent = self.tree.Element("NOTES")
                self.root = self.tree.getroot()
                if not parent is None:
                        self.noteParent.find()

        def __setNote(self, iOverwrite, noteImmParent, noteTag, noteText):
                if iOverwrite == 0:
                        elem = ET.SubElement(noteImmParent, noteTag)
                else:
                        elem = noteImmParent.find(noteTag)
                elem.text = noteText

        def writeNote(self, iOverwrite, sTopic,sId,sBody,sSrcNote,sSrcLink,sTTags,sCTags,sSTags):
                #TODO after simple prototype, restructure to take generic dictionary of tags, values, attributes.  should be able to recycle some of this for updating config file.
                if iOverwrite == 0:
                    self.noteParent = ET.SubElement(self.noteParent, 'NOTE') 
                self.noteParent.set('id',sId)
                self.__setNote(iOverwrite, self.noteParent, 'TOPIC', sTopic)
                self.__setNote(iOverwrite, self.noteParent, 'BODY', sBody)
                self.__setNote(iOverwrite, self.noteParent, 'SRC_NOTE', sSrcNote)
                self.__setNote(iOverwrite, self.noteParent, 'SRC_LINK', sSrcLink)
                self.__setNote(iOverwrite, self.noteParent, 'T_TAGS', sTTags)
                self.__setNote(iOverwrite, self.noteParent, 'C_TAGS', sCTags)
                self.__setNote(iOverwrite, self.noteParent, 'S_TAGS', sSTags)
                self.__setNote(iOverwrite, self.noteParent, 'DATE', datetime.today().strftime('%m/%d/%Y'))


        def readNote(self, root):
                #TODO improve this [hardcoded range; repetition]
                self.noteParent = self.root.find(".//NOTE[@id='{0}']".format(root))
                if self.noteParent is not None:
                        self.id = root
                        self.topic = self.noteParent.find('TOPIC').text
                        self.body = self.__validateTextVar(self.noteParent.find('BODY').text)
                        self.srcNote = self.noteParent.find('SRC_NOTE').text
                        self.srcLink = self.noteParent.find('SRC_LINK').text
                        self.tTags = self.noteParent.find('T_TAGS').text
                        self.cTags = self.noteParent.find('C_TAGS').text
                        self.sTags = self.noteParent.find('S_TAGS').text
                        self.date = self.noteParent.find('DATE').text
                        return [self.topic, root, self.body, self.srcNote, self.srcLink, self.tTags, self.cTags, self.sTags, self.date]
                else:
                        return ["" for i in range(9)]

        def getAllIDs(self, root=None):
                if root is None: 
                    root = self.root
                ids = []
                for note in root.findall(".//NOTE"):
                        ids.append(note.get("id"))
                return ids
                
        def getAllChildIDs(self):
                pass
                
        def saveNote(self):
                rough_xml = ET.tostring(self.root, 'utf-8')
                reparsed_xml = minidom.parseString(rough_xml).toprettyxml(indent="\t")
                reparsed_xml = re.sub(r'\n[ |\t|\n]*\n',r'\n',reparsed_xml)  #remove blank rows
                with open(self.path, "w") as text_file:
                        print(reparsed_xml, file=text_file)

        def __validateTextVar(self, text):
                if text is None:
                    text = ''
                return text

root = tk.Tk()

app = NotesWriter(root)
root.title("XML Note Taker " + app.getVersion())
app.mainloop()
