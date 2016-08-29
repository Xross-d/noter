#!/usr/bin/python
import Tkinter as tk
import tkMessageBox
import pickle
import sched, time

version = "1.0.0"
notes_file = "notes.tnt"

about_text = "Version: "+version+"\nXross."

usage_text = "todo..."

class MyApp(object):
	def __init__(self,master):
		self.master = master
		self.master.title("MyApp")
		self.master.geometry("600x400")
		self.editor = Editor(self.master)
		self.menubar = MenuBar(self.master)
		self.editor.autoSave()
		self.master.mainloop()

class MenuBar(object):
	def __init__(self,master):
		self.master = master
		self.menubar = tk.Menu(self.master)
		self.filemenu = tk.Menu(self.menubar,tearoff=0)
		self.filemenu.add_command(label="Exit",command=self.ExitCommand)
		self.menubar.add_cascade(label="MyApp",menu=self.filemenu)

		#edit menu
		self.editmenu = tk.Menu(self.menubar,tearoff=0)
		self.editmenu.add_command(label="Date/Time",command=self.DateTime)
		self.menubar.add_cascade(label="Edit",menu=self.editmenu)

		#display menu
		self.master.config(menu=self.menubar)


	def DateTime(self):
		self.localtime = time.asctime( time.localtime( time.time() )  )
		self.strtime = str(self.localtime)
		self.label = tkMessageBox.showinfo("Date/Time",self.strtime)
		return None

	def ExitCommand(self):
		if tkMessageBox.askyesno("Quit","Are you sure?"):
			self.master.destroy()

class Editor(object):
	def __init__(self,master):
		self.master = master
		self.editor = tk.Frame(self.master)
		self.notelistframe = tk.Frame(self.master)

		self.text = tk.Text(self.editor,height=8, width=4)
		self.text.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=1)

		self.scroll1v = tk.Scrollbar(self.notelistframe,orient=tk.VERTICAL)
		self.scroll2h = tk.Scrollbar(self.notelistframe,orient=tk.HORIZONTAL)
		self.notelist = tk.Listbox(self.notelistframe,yscrollcommand=self.scroll1v.set,selectmode=tk.EXTENDED)
		self.notelist = tk.Listbox(self.notelistframe,xscrollcommand=self.scroll2h.set,selectmode=tk.EXTENDED)
		self.scroll1v.configure(command=self.notelist.yview)
		self.scroll2h.configure(command=self.notelist.xview)
		self.scroll2h.pack(side=tk.BOTTOM,fill=tk.X)
		self.notelist.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)
		self.scroll1v.pack(side=tk.RIGHT,fill=tk.Y)

		self.editor.pack(fill=tk.BOTH,side=tk.LEFT)
		self.notelistframe.pack(fill=tk.BOTH,expand=1,side=tk.RIGHT)
		self.buttons = Buttons(self.editor,self.text,self.notelist)
		self.getNotes()

	def autoSave(self):
		self.buttons.save()
		self.master.after(60000 * 1, self.autoSave)

	def getNotes(self):
		try:
			f = file(notes_file, "rb")
			self.notes = pickle.load(f)
			for item in self.notes:
				self.notelist.insert(tk.END,item)
			f.close()
		except:
			pass


class Buttons(object):
	def __init__(self,master,text,notes):
		self.master = master
		self.text = text
		self.notelist = notes
		self.enterButton = tk.Button(self.master,text="Enter",command=self.enter)
		self.removeButton = tk.Button(self.master,text="Remove",command=self.remove)
		self.saveButton = tk.Button(self.master,text="Save",command=self.save)
		self.showButtons()

	def enter(self):
		self.text_contents = self.text.get(1.0, tk.END)
		self.notelist.insert(tk.END, self.text_contents)
		self.text.delete(1.0,tk.END)

	def remove(self):
		self.notelist.delete(tk.ANCHOR)

	def save(self):
		f = file(notes_file, "wb")
		self.notes = self.notelist.get(0, tk.END)
		pickle.dump(self.notes, f)

	def showButtons(self):
		self.enterButton.pack(side=tk.LEFT)
		self.removeButton.pack(side=tk.LEFT)
		self.saveButton.pack(side=tk.LEFT)

if __name__ == '__main__':
	root = tk.Tk()
	myapp = MyApp(root)
