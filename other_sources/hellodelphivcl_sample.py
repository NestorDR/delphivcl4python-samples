# ---------------------------------------------------------------------------------
# Name:       hellodelphivcl_sample.py
# Purpose:    DelphiVCL for Python sample
#
# Author:     Embarcadero Technologies, Inc.
#
# Copyright:  2020-2022 Embarcadero Technologies, Inc.
# License:    https://github.com/Embarcadero/DelphiVCL4Python/blob/main/LICENSE.md
# Original source code: https://github.com/Embarcadero/DelphiVCL4Python/blob/main/samples/HelloWorld/hellodelphivcl.py
# ---------------------------------------------------------------------------------

# --- Third Party libraries ---
# delphivcl: Delphi's VCL library as a Python module for building native Windows GUI Applications
from delphivcl import Application, caFree, Form, FreeConsole, Label

# --- Python modules ---
# sys: module which provides access to some variables used or maintained by the interpreter and to functions that
#      interact strongly with the interpreter.
import sys


class MainForm(Form):
    def __init__(self, owner):
        self.Caption = "A VCL Form..."
        self.SetBounds(10, 10, 500, 400)
        self.Position = "poScreenCenter"

        self.lblHello = Label(self)
        self.lblHello.SetProps(Parent=self, Caption="Hello DelphiVCL for Python")
        self.lblHello.SetBounds(10, 10, 300, 24)

        self.OnClose = self.__on_form_close

    @staticmethod
    def __on_form_close(sender, action):
        action.Value = caFree


def main():
    Application.Initialize()
    Application.Title = "Hello Python"
    main_form_ = MainForm(Application)
    main_form_.Show()
    FreeConsole()
    Application.Run()
    main_form_.Destroy()


# Use of __name__ & __main__
# When the Python interpreter reads a code file, it completely executes the code in it.
# For example, in a file my_module.py, when executed as the main program, the __name__ attribute will be '__main__',
# however if it is used importing it from another module: import my_module, the __name__ attribute will be 'my_module'.
if __name__ == '__main__':
    main()

    # Terminate normally
    sys.exit(0)
