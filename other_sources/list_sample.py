# ---------------------------------------------------------------------------------
# Name:       list_sample.py
# Purpose:    DelphiVCL for Python sample
#
# Author:     Muhammad Azizul Hakim
#
# Copyright:  2020-2022 Embarcadero Technologies, Inc.
# License:    https://github.com/Embarcadero/DelphiVCL4Python/blob/main/LICENSE.md
# Original source code: https://pythongui.org/an-introduction-to-delphivcl-a-python-gui-builder-for-windows/
# ---------------------------------------------------------------------------------

# --- Third Party libraries ---
# delphivcl: Delphi's VCL library as a Python module for building native Windows GUI Applications
from delphivcl import Application, Button, caFree, Edit, Form, FreeConsole, Label, ListBox

# --- Python modules ---
# sys: module which provides access to some variables used or maintained by the interpreter and to functions that
#      interact strongly with the interpreter.
import sys


class MainForm(Form):
    def __init__(self, owner):
        self.Caption = "A VCL Form..."
        self.SetBounds(10, 10, 340, 410)
        self.lblHello = Label(self)
        self.lblHello.SetProps(Parent=self, Caption="Please Input Your Lists")
        self.lblHello.SetBounds(10, 10, 120, 24)
        self.edit1 = Edit(self)
        self.edit1.SetProps(Parent=self, Top=30, Left=10, Width=200, Height=24)
        self.button1 = Button(self)
        self.button1.SetProps(Parent=self, Caption="Add", OnClick=self.button_click)
        self.button1.SetBounds(220, 29, 90, 24)
        self.lb1 = ListBox(self)
        self.lb1.SetProps(Parent=self)
        self.lb1.SetBounds(10, 60, 300, 300)

    def button_click(self, sender):
        self.lb1.Items.Add(self.edit1.Text)

    @staticmethod
    def __on_form_close(sender, action):
        action.Value = caFree


def main():
    Application.Initialize()
    Application.Title = "Embarcadero DelphiVCL App"
    f = MainForm(Application)
    f.Show()
    FreeConsole()
    Application.Run()
    Application.Destroy()


# Use of __name__ & __main__
# When the Python interpreter reads a code file, it completely executes the code in it.
# For example, in a file my_module.py, when executed as the main program, the __name__ attribute will be '__main__',
# however if it is used importing it from another module: import my_module, the __name__ attribute will be 'my_module'.
if __name__ == '__main__':
    main()

    # Terminate normally
    sys.exit(0)

