from Tkinter import *
from tkSimpleDialog import *
from tkFileDialog   import *
from tkMessageBox import *
class mset(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
root = Tk()
app = mset(master=root)
app.master.title("Mini")
root.geometry("950x600")
root.configure(background="#2A4A6B")
left = Frame(root)
left.pack(side=LEFT)
right = Frame(root)
right.pack(side=RIGHT)
bottom = Frame(root)
bottom.pack(side=BOTTOM)
class QuitMe(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, text='Quit', command=self.quit)
        widget.pack(expand=YES, fill=BOTH, side=LEFT)
    def quit(self):
        ans = askokcancel('Mini', "Sure you want to Quit?")
        if ans: Frame.quit(self)
class ScrolledText(Frame):
    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.configure(background="black")
        self.pack(expand=YES, fill=BOTH)
        self.makewidgets()
        self.settext(text, file)
    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        self.text = text
    def settext(self, text='', file=None):
        if file:
            text = open(file, 'r').read()
        self.text.delete('1.0', END)
        self.text.insert('1.0', text)
        self.text.mark_set(INSERT, '1.0')
        self.text.focus()
    def gettext(self):
        return self.text.get('1.0', END+'-1c')
class mini(ScrolledText):
    def __init__(self, parent=None, file=None):
        frm = Frame(parent)
        frm.pack(fill=X)
        frm.configure(background="black")
        Button(frm, text='Save',  command=self.onSave, height = 0, width = 2, bg='black').pack(side=LEFT)
        Button(frm, text='Cut',   command=self.onCut, height = 0, width = 2, bg='black').pack(side=LEFT)
        Button(frm, text='Paste', command=self.onPaste, height = 0, width = 2, bg='black').pack(side=LEFT)
        Button(frm, text='Find',  command=self.onFind, height = 0, width = 2, bg='black').pack(side=LEFT)
        QuitMe(frm).pack(side=RIGHT)
        ScrolledText.__init__(self, parent, file=file)
        self.text.config(font=('Console', 10, 'normal'))
    def onSave(self):
        filename = asksaveasfilename()
        if filename:
            alltext = self.gettext()
            open(filename, 'w').write(alltext)
    def onCut(self):
        text = self.text.get(SEL_FIRST, SEL_LAST)
        self.text.delete(SEL_FIRST, SEL_LAST)
        self.clipboard_clear()
        self.clipboard_append(text)
    def onPaste(self):
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.text.insert(INSERT, text)
        except TclError:
            pass
    def onFind(self):
        target = askstring('Mini', 'Search String?')
        if target:
            where = self.text.search(target, INSERT, END)
            if where:
                print where
                pastit = where + ('+%dc' % len(target))
                self.text.tag_add(SEL, where, pastit)
                self.text.mark_set(INSERT, pastit)
                self.text.see(INSERT)
                self.text.focus()
if len(sys.argv) > 1:
	mini(file=sys.argv[1]).mainloop()
else:
	mini().mainloop()

