#!/usr/bin/env python
#coding = utf8

# coded by Jaanus Kalde
# http://jaanus.tech-thing.org

# Freeware, you can share and change it. But not sell
# http://creativecommons.org/licenses/by-nc-sa/3.0/


import glob, os
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import *
from manager import *
from tkSimpleDialog import *

f=open('manager/config.txt','r')
conf=f.readlines()
f.close()

#askdirectory()
for i in range(2):
   conf[i]=conf[i].strip()

mod = lib = modNames = libNames = content = selectedContent = []

selectedFile = popup = popupContent = None

def contentUpdate(arg):
   contentListbox.delete(0,END)
   global content, selectedFile

   if selected.get() == 0:
      selectedFile = lib[int(fileListbox.curselection()[0])]
      content = getLibContent(selectedFile)
      content.sort()
      for i in content:
         contentListbox.insert(END,i)
   else:
      selectedFile = mod[int(fileListbox.curselection()[0])]
      content = getModContent(selectedFile)
      content.sort()
      for i in content:
         contentListbox.insert(END,i)
   
   out('Content is updated.', 3)

def update(content):
   fileListbox.delete(0,END)
   for i in content:
      fileListbox.insert(END, i)

def libUpdate():
   contentListbox.delete(0,END)
   global lib, libNames
   lib = glob.glob(conf[0]+'/*.lib')
   lib.sort()
   libNames = []
   for i in lib:
      libNames.append(i[8:-4])
   
   out('Now we are looking libraries',3)
   update(libNames)

def modUpdate():
   contentListbox.delete(0,END)
   global mod, modNames
   mod = glob.glob(conf[1]+'/*.mod')
   mod.sort()
   modNames = []
   for i in mod:
      modNames.append(i[8:-4])

   out('Now we are looking modules',3)
   update(modNames)

def delete():
   if selected.get() == 0:
      if askquestion('Really','Want to delete library '+libNames[int(fileListbox.curselection()[0])]) == 'yes':
         os.remove(lib[int(fileListbox.curselection()[0])])
         out('You deleted library '+libNames[int(fileListbox.curselection()[0])],2)
         libUpdate()
   else:
      if askquestion('Really','Want to delete module '+modNames[int(fileListbox.curselection()[0])]) == 'yes':
         os.remove(mod[int(fileListbox.curselection()[0])])
         out('You deleted module '+modNames[int(fileListbox.curselection()[0])],2)
         modUpdate()
   
#refactor with askstring(...)
def new():
   if selected.get() == 0:
      newLibrary()
      libUpdate()
   else:
      newModule()
      modUpdate()

def check():
   if selected.get() == 0:
      out('TODO',1)
   else:
      checkModule(mod[int(fileListbox.curselection()[0])])

def deleteContent():
   if contentListbox.curselection() != ():
      tmp=[]
      for i in contentListbox.curselection():
         tmp.append(content[int(i)])
      if selected.get() == 0:
         if askquestion('Really','Want to delete part(s) '+','.join(tmp)) == 'yes':
            deleteLibContent(selectedFile, tmp)
      else:
         if askquestion('Really','Want to delete module(s) '+','.join(tmp)) == 'yes':
            deleteModContent(selectedFile, tmp)
      contentListbox.delete(0,END)
      out('TODO: make content box update correctly.',1)

def renameContent():
   if contentListbox.curselection() != ():
      if selected.get() == 0:
         renameLibContent(selectedFile, content[int(contentListbox.curselection()[0])])
      else:
         renameModContent(selectedFile, content[int(contentListbox.curselection()[0])])
      
#there is a bug here, don't try to move to the same file you are moving from
def moveContent():
   if contentListbox.curselection() != ():
      selectFile(__moveCallback)
   
def copyContent():
   if contentListbox.curselection() != ():
      selectFile(__copyCallback)
      
#generates popup to choose target file
#needs callback function as a argument
def selectFile(call):
   if contentListbox.curselection() != ():
      global popup, popupContent, selectedContent
      #store selected thingies
      selectedContent=[]
      for i in contentListbox.curselection():
         selectedContent.append(content[int(i)])
      
      #generate the popup
      popup = Toplevel()
      popup.title('Select target file')
      popupScrollbar = Scrollbar(popup)
      popupScrollbar.grid(row=0, column=1, sticky=N+S)
      popupContent = Listbox(popup, yscrollcommand=popupScrollbar.set, height=30, width=30)
      popupScrollbar.config(command=popupContent.yview)
      popupContent.grid(row=0, column=0, sticky=N+S+E+W)
      popupContent.bind('<<ListboxSelect>>',call)

      if selected.get() == 0:
         for i in libNames:
            popupContent.insert(END, i)
      else:
         for i in modNames:
            popupContent.insert(END, i)

def __copyCallback(arg):
   #destination from popup
   #source from selectedFile and selectedContent

   #copies
   if selected.get() == 0:
      copyLibContent(selectedFile, selectedContent, lib[int(popupContent.curselection()[0])])
   else:
      copyModContent(selectedFile, selectedContent, mod[int(popupContent.curselection()[0])])

   popup.destroy()

def __moveCallback(arg):
   #destination from popup
   #source from selectedFile and selectedContent

   #copies and deletes
   if selected.get() == 0:
      copyLibContent(selectedFile, selectedContent, lib[int(popupContent.curselection()[0])])
      deleteLibContent(selectedFile, selectedContent)
   else:
      copyModContent(selectedFile, selectedContent, mod[int(popupContent.curselection()[0])])
      deleteModContent(selectedFile, selectedContent)
                     
   contentListbox.delete(0,END)
   out('TODO: make content box update correctly.',1)
   popup.destroy()

root = Tk()
root.title('Tech-thing KiCad library manager')
out('KiCad library manager. http://jaanus.tech-thing.org',2)
#root.geometry("%dx%d%+d%+d" % (600, 400, 0, 0))

selected = IntVar() #are we looking libs or mods   


selectFrame = Frame(root)
libButton = Radiobutton(selectFrame, text='libraries', variable=selected, value=0, command=libUpdate).pack(side=LEFT)
modButton = Radiobutton(selectFrame, text='modules', variable=selected, value=1, command=modUpdate).pack(side=LEFT)
selectFrame.grid(row=0, column=0, columnspan=2)

commandFrame = Frame(root)
Button(commandFrame, text='New', command=new).pack(side=LEFT, fill=X)
Button(commandFrame, text='Delete', command=delete).pack(side=LEFT, fill=X)
Button(commandFrame, text='Check', command=check).pack(side=LEFT, fill=X)
commandFrame.grid(row=1, column=0, columnspan=2)

fileListScrollbar = Scrollbar(root)
fileListScrollbar.grid(row=2, column=1, sticky=N+S)
fileListbox = Listbox(root, yscrollcommand=fileListScrollbar.set, height=30, width=30)
fileListScrollbar.config(command=fileListbox.yview)
fileListbox.grid(row=2, column=0, sticky=N+S+E+W)

fileListbox.bind('<<ListboxSelect>>',contentUpdate)

contentCommandFrame = Frame(root)
Button(contentCommandFrame, text='Copy', command=copyContent).pack(side=LEFT, fill=X)
Button(contentCommandFrame, text='Move', command=moveContent).pack(side=LEFT, fill=X)
Button(contentCommandFrame, text='Rename', command=renameContent).pack(side=LEFT, fill=X)
Button(contentCommandFrame, text='Delete', command=deleteContent).pack(side=LEFT, fill=X)
contentCommandFrame.grid(row=1, column=2, columnspan=2)

contentListScrollbar = Scrollbar(root)
contentListScrollbar.grid(row=2, column=3, sticky=N+S)
contentListbox = Listbox(root, yscrollcommand=contentListScrollbar.set, height=30, selectmode=EXTENDED, width=30)
contentListScrollbar.config(command=contentListbox.yview)
contentListbox.grid(row=2, column=2, sticky=N+S+E+W)

libUpdate()
root.mainloop()
