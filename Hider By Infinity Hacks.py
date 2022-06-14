# Note: This Software is made by Ravikant Asoliya

from tkinter import DISABLED, END, FLAT, LEFT, NE, NW, RIGHT, Button, Frame, Listbox, LabelFrame
import os
import sys
import re
from tkinter.filedialog import askdirectory
from tkinter.font import NORMAL
from subprocess import call
from tkinterdnd2 import Tk


class HiderByInfinityHacks(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x207")
        self.resizable(False, False)
        self.title("Hider By Infinity Hacks")
        image_path = self.resource_path("InfinityHacksLogo.ico")
        self.iconbitmap(image_path)
        self.createListbox()
        self.createButton()

    def createListbox(self):
        self.listboxFrame = LabelFrame(
            self, text="Drag and Drop & Select Files and Folders", labelanchor="n", relief=FLAT)
        self.listbox = Listbox(self.listboxFrame, selectmode="extended", font=(
            "arial", "10"), state=DISABLED)
        self.listbox.pack(side=LEFT, ipadx=150, padx=15, pady=(0, 10))
        self.listboxFrame.pack(side=LEFT, anchor=NW)

        self.listbox.drop_target_register("*")
        self.listbox.dnd_bind("<<Drop>>", self.dropFilesInsideListbox)
        self.listbox.bind("<Button-1>", self.selectDirectory)

    def createButton(self):
        self.buttonFrame = Frame(self)
        self.buttonHide = Button(self.buttonFrame, text="Hide",
                                 font=("arial", "10"), command=self.hide)
        self.buttonHide.pack(padx=(0, 20), ipadx=50, pady=(65, 0))

        self.buttonShow = Button(self.buttonFrame, text="Show",
                                 font=("arial", "10"), command=self.show)
        self.buttonShow.pack(padx=(0, 20), ipadx=50, pady=(25, 0))
        self.buttonFrame.pack(side=RIGHT, anchor=NE)

    def dropFilesInsideListbox(self, event, *args):
        self.listbox.configure(state=NORMAL)
        data = event.data
        data = data.replace(" {", "\n")
        data = data.replace("} ", "\n")
        data = data.replace("{", "")
        data = data.replace("}", "")
        data = data.split("\n")
        for files in data:
            if 1 == files.count(":") < 2:
                self.listbox.insert("end", files)
            else:
                files = files.split(" ")
                for file in files:
                    self.listbox.insert("end", file)
        self.listbox.configure(state=DISABLED)

    def selectDirectory(self, event):
        directory = askdirectory()
        self.listbox.configure(state=NORMAL)
        if directory != "":
            self.listbox.insert("end", directory)
        self.listbox.configure(state=DISABLED)

    def hide(self):
        data = self.listbox.size()
        for i in range(0, data):
            call(f"attrib +h +s \"{self.listbox.get(i)}\"", shell=True)
        for i in range(0, data):
            self.listbox.configure(state=NORMAL)
            self.listbox.delete(0, END)
            self.listbox.configure(state=DISABLED)

    def show(self):
        data = self.listbox.size()
        for i in range(0, data):
            if os.path.isfile(self.listbox.get(i)):
                call(f"attrib -s -h \"{self.listbox.get(i)}\"")
                pass
            elif os.path.isdir(self.listbox.get(i)):
                call(f"attrib -s -h \"{self.listbox.get(i)}\"")
                for file in os.listdir(self.listbox.get(i)):
                    call(
                        f"attrib -s -h \"{self.listbox.get(i)}\{file}\"")
            else:
                pass
        for i in range(0, data):
            self.listbox.configure(state=NORMAL)
            self.listbox.delete(0, END)
            self.listbox.configure(state=DISABLED)

    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)


def MakeTkDPIAware(TKGUI):
    TKGUI.DPI_X, TKGUI.DPI_Y, TKGUI.DPI_scaling = Get_HWND_DPI(
        TKGUI.winfo_id())
    TKGUI.TkScale = lambda v: int(float(v) * TKGUI.DPI_scaling)
    TKGUI.TkGeometryScale = lambda s: TkGeometryScale(s, TKGUI.TkScale)


def Get_HWND_DPI(window_handle):
    import os
    if os.name == "nt":
        from ctypes import windll, pointer, wintypes
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
        DPI100pc = 96
        DPI_type = 0
        winH = wintypes.HWND(window_handle)
        monitorhandle = windll.user32.MonitorFromWindow(
            winH, wintypes.DWORD(2))
        X = wintypes.UINT()
        Y = wintypes.UINT()
        try:
            windll.shcore.GetDpiForMonitor(
                monitorhandle, DPI_type, pointer(X), pointer(Y))
            return X.value, Y.value, (X.value + Y.value) / (2 * DPI100pc)
        except Exception:
            return 96, 96, 1
    else:
        return None, None, 1


def TkGeometryScale(s, cvtfunc):
    # format "WxH+X+Y"
    patt = r"(?P<W>\d+)x(?P<H>\d+)\+(?P<X>\d+)\+(?P<Y>\d+)"
    R = re.compile(patt).search(s)
    G = str(cvtfunc(R.group("W"))) + "x"
    G += str(cvtfunc(R.group("H"))) + "+"
    G += str(cvtfunc(R.group("X"))) + "+"
    G += str(cvtfunc(R.group("Y")))
    return G


if __name__ == "__main__":
    hider = HiderByInfinityHacks()
    # MakeTkDPIAware(hider)
    hider.mainloop()
