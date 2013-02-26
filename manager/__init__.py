#coding=utf8

# module input-output file. usest tkinter to display popups
#
# coded by Jaanus Kalde
# http://jaanus.tech-thing.org

# Freeware, you can share and change it. But not sell
# http://creativecommons.org/licenses/by-nc-sa/3.0/


popup = None
popupContent = None

from Tkinter import *
from time import strftime

__filename = __name = None

verbosity = 3
# 0 - ninja mode
# 1 - errors etc
# 2 - file manipulations only
# 3 - debug mode

#function to output thing with given verbosity.
def out(text, v):
   if v <= verbosity:
      if v == 0:
         print '##########',text,'##########'
      elif v == 1:
         print '#####',text,'#####'
      elif v == 2:
         print '##',text,'##'
      else:
         print text
      
def __find__(what, where):
   for i in range(len(where)):
      if what.lower() == where[i].strip().lower():
         return i
   out('Error in file reading', 2)
   return False

def __findStrict__(what, where):
   for i in range(len(where)):
      if what == where[i].strip():
         return i
   out('Error in file reading', 2)
   return False

def getModContent(filename):
   f = open(filename, 'r')
   content = f.readlines()
   f.close()

   #searches for index and gets its contents
   a = __find__('$INDEX',content)
   if a == False:
      out('No index in file', 1)
      return False
   b = __find__('$EndINDEX',content)
   if b == False:
      out('No end of index in file', 1)
      return False
      
   #gets all the content in
   fileIndex = content[a+1:b]

   #get rid of whitespace
   for i in range(len(fileIndex)):
      fileIndex[i] = fileIndex[i].strip()

   return fileIndex

def checkModule(filename):
   f = open(filename, 'r')
   content = f.readlines()
   f.close()

   #searches for index and gets its contents
   a = __find__('$INDEX',content)
   if a == False:
      out('No index in file', 1)
      return False
   b = __find__('$EndINDEX',content)
   if b == False:
      out('No end of index in file', 1)
      return False
      
   #gets all the content in
   fileIndex = content[a+1:b]

   #does error checking to check if all the modules have body
   for i in range(len(fileIndex)):
      fileIndex[i] = fileIndex[i].strip()
      a = __findStrict__('$MODULE '+fileIndex[i],content)
      if a == False:
         out('The module "'+fileIndex[i]+'" has no body.',1)

def getLibContent(filename):
   f = open(filename, 'r')
   content = f.readlines()
   f.close()

   list = []

   #find all DEF tags
   for i in range(len(content)):
      if content[i][0:4] == 'DEF ':
         list.append(content[i].split()[1])
         #find all aliases and display them in the same place
         for e in range(5):
            if content[i+e][0:6] == 'ALIAS ':
               a = content[i+e].split()
               a[0] = list[len(list)-1]
               list[len(list)-1] = '/'.join(a)
   return list

def newModule():
   global popup, popupContent
   popup = Toplevel()
   popup.title('Create new module')
   Message(popup, text='Name').pack(side=LEFT)
   popupContent = StringVar()
   box=Entry(popup, textvariable = popupContent)
   box.bind('<Return>',__newModule2)
   box.pack(side=LEFT)
   Button(popup, text='OK', command=__newModule).pack(side=LEFT)

def __newModule2(arg): __newModule()
   
def __newModule():
   f=open('modules/'+popupContent.get()+'.mod','w')
   f.write('PCBNEW-LibModule-V1  '+ strftime("%d/%m/%Y %H:%M:%S")+'\n#encoding utf-8\n$INDEX\n$EndINDEX\n$EndLIBRARY');
   f.close()

   out('Made new module named: '+popupContent.get(),1)
   popup.destroy()


def newLibrary():
   global popup, popupContent
   popup = Toplevel()
   popup.title('Create new library')
   Message(popup, text='Name').pack(side=LEFT)
   popupContent = StringVar()
   box=Entry(popup, textvariable = popupContent)
   box.bind('<Return>',__newLibrary2)
   box.pack(side=LEFT)
   Button(popup, text='OK', command=__newLibrary).pack(side=LEFT)

def __newLibrary2(arg): __newLibrary()
def __newLibrary():
   f=open('library/'+popupContent.get()+'.lib','w')
   f.write('EESchema-LIBRARY Version 2.3  Date: '+strftime("%d/%m/%Y %H:%M:%S")+'\n#\n#End Library');
   f.close()

   out('Made new module named: '+popupContent.get(),1)
   popup.destroy()

def renameModContent(filename, modname):
   global popup, popupContent, __filename, __name
   __filename = filename
   __name = modname
   popup = Toplevel()
   popup.title('Rename mod content')
   popupContent = StringVar(value=modname)
   box=Entry(popup, textvariable = popupContent)
   box.bind('<Return>',__renameModContent2)
   box.pack(side=LEFT)
   Button(popup, text='OK', command=__renameModContent).pack(side=LEFT)

def __renameModContent2(arg): __renameModContent()
def __renameModContent():
#   global __filename, __name
   f=open(__filename, 'r')
   content = f.readlines()
   f.close()
   
   for i in range(len(content)):
      if content[i].strip()==__name.strip():
         content[i]=popupContent.get()+'\n'
         out('Renamed in index.',3)
      elif content[i].strip()=='$MODULE '+__name.strip():
         content[i]='$MODULE '+popupContent.get()+'\n'
         out('Renamed in content.',3)
      elif content[i].strip()=='Li '+__name.strip():
         content[i]='Li '+popupContent.get()+'\n'
         out('Renamed in Li.',3)
      elif content[i].strip()=='$EndMODULE '+__name.strip():
         content[i]='$EndMODULE '+popupContent.get()+'\n'
         out('Renamed in end of content.',3)
         break;

   f=open(__filename, 'w')
   content = f.write(''.join(content))
   f.close()
   out('Renamed the module.',2)   
   popup.destroy()
   

def renameLibContent(filename, libname):
   global popup, popupContent, __filename, __name
   __filename = filename
   __name = libname.split('/')[0]
   popup = Toplevel()
   popup.title('Rename lib content')
   popupContent = StringVar(value=libname)
   box=Entry(popup, textvariable = popupContent)
   box.bind('<Return>',__renameLibContent2)
   box.pack(side=LEFT)
   Button(popup, text='OK', command=__renameLibContent).pack(side=LEFT)

def __renameLibContent2(arg): __renameLibContent()
def __renameLibContent():
   #think new names and aliases from the format
   if popupContent.get().find('/') == -1:
      newName=popupContent.get()
      newAlias=''
   else:#user entered name with aliases
      newName=popupContent.get().split('/')[0]
      newAlias='ALIAS '+' '.join(popupContent.get().split('/')[1:])+'\n'

   #get file content
   f=open(__filename, 'r')
   content = f.readlines()
   f.close()
   
   for i in range(len(content)):
      if content[i][0:(4+len(__name))]=='DEF '+__name:
         content[i]='DEF '+newName+content[i][(4+len(__name)):]
         content[i+2]='F1 "'+newName+'"'+content[i+2][(5+len(__name)):]
         if content[i+3][0:6] == 'ALIAS ':
            content[i+3] = newAlias
         else:
            content[i+2]+=newAlias
         break;

   f=open(__filename, 'w')
   f.write(''.join(content))
   f.close()
   out('Renamed the library.',2)   
   popup.destroy()
   
   
def deleteModContent(filename, modnames):
   #get file content
   f=open(filename, 'r')
   content = f.readlines()
   f.close()

   #find the bastard(s)
   for wanted in modnames:
      for i in range(len(content)):
         if content[i].strip()==wanted.strip():
            content[i]=''
            out('Deleted '+wanted+' in index.',3)
         elif content[i].strip()=='$MODULE '+wanted.strip():
            for e in range(i, len(content)):
               if content[e].strip()[0:11]=='$EndMODULE ': break
            del content[i:(e+1)]
            out('Deleted '+wanted+' in content.',3)
            break
   #save changes
   f=open(filename, 'w')
   f.write(''.join(content))
   f.close()
   out('Deleted the module(s).',2)   
   

#there is a minor bug in here, we leave stray comments(ghosts)
def deleteLibContent(filename, libnames):
   #get file content
   f=open(filename, 'r')
   content = f.readlines()
   f.close()

   #find the bastard(s)
   for wanted in libnames:
      #lets get these aliases out of the way
      if wanted.find('/') != -1:
         wanted=wanted.split('/')[0]
         
      for i in range(len(content)):
         if content[i][0:(4+len(wanted))]=='DEF '+wanted:
            for e in range(i, len(content)):
               if content[e].strip()[0:6]=='ENDDEF': break
            del content[i:(e+1)]
            out('Deleted '+wanted+'.',3)
            break

   #save changes
   f=open(filename, 'w')
   f.write(''.join(content))
   f.close()
   out('Deleted the part(s).',2)   


def copyLibContent(filename, libnames, dest):
   #get file content
   f=open(filename, 'r')
   content = f.readlines()
   f.close()

   #copy buffer
   f=open(dest, 'r')
   copy = f.readlines()
   f.close()

   #find the bastard(s)
   for wanted in libnames:
      #lets get these aliases out of the way
      if wanted.find('/') != -1:
         wanted=wanted.split('/')[0]
      #if you copy to the same place you copy from
      if filename == dest:
         wanted = 'CopyOf'+wanted
         
      for i in range(len(content)):
         if content[i][0:(4+len(wanted))]=='DEF '+wanted:
            for e in range(i, len(content)):
               if content[e].strip()[0:6]=='ENDDEF':
                  break
            for a in content[i:(e+1)]:
               copy.append(a)
            out('Copied '+wanted+'.',3)
            break

   #save changes
   f=open(dest, 'w')
   f.write(''.join(copy))
   f.close()
   out('Copied the part(s).',2)   
   
def copyModContent(filename, modnames, dest):
   #get file content
   f=open(filename, 'r')
   content = f.readlines()
   f.close()

   #copy buffer
   f=open(dest, 'r')
   copy = f.readlines()
   f.close()

   #pop the $endlibrary thing from bottom
   for i in range(len(copy)-1,0,-1):
      if copy[i].strip().lower()=='$endlibrary':
         del copy[i:]
         break

   #if you copy to the same place you copy from
   if filename == dest:
      for i in range(len(modnames)):
         modnames[i]='CopyOf'+modnames[i]

   #add everithing to index
   for i in range(len(copy)):
      if copy[i].strip().lower()=='$endindex':
         copy[i-1]+='\n'.join(modnames)+'\n'
         break
         
   #find the bastard(s)
   for wanted in modnames:
      for i in range(len(content)):
         if content[i].strip()=='$MODULE '+wanted.strip():
            for e in range(i, len(content)):
               if content[e].strip()[0:11]=='$EndMODULE ': break
            for a in content[i:(e+1)]:
               copy.append(a)
            out('Copied '+wanted+'.',3)
            break

   #save changes
   f=open(dest, 'w')
   f.write(''.join(copy)+'$EndLIBRARY')
   f.close()
   out('Copied the module(s).',2)
