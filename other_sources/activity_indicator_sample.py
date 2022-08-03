# ---------------------------------------------------------------------------------
# Name:       activity_indicator_sample.py
# Purpose:    DelphiVCL for Python sample
#
# Author:     Lucas Moura Belo - https://github.com/lmbelo?tab=repositories
#
# Created:    28/09/2021
# Copyright:  2020-2022 Embarcadero Technologies, Inc.
# License:    https://github.com/Embarcadero/DelphiVCL4Python/blob/main/LICENSE.md
# Original source code: https://github.com/Embarcadero/DelphiVCL4Python/tree/main/samples/ActivityIndicator
# ---------------------------------------------------------------------------------

# --- Third Party libraries ---
# delphivcl: Delphi's VCL library as a Python module for building native Windows GUI Applications
from delphivcl import ActivityIndicator, Application, caFree, CheckBox, ColorBox,  ComboBox, FileOpenDialog, Form,\
    FreeConsole, Label, MainMenu, RadioGroup, StyleManager, StyleServices, TrackBar

# --- Python modules ---
# os: module which allows access to OperatingSystem-dependent functionalities.
import os
# sys: module which provides access to some variables used or maintained by the interpreter and to functions that
#      interact strongly with the interpreter.
import sys


class ActivityIndicatorForm(Form):
    def __init__(self, owner):
        self.__create_comps()
        self.__config_comps()

    def __create_comps(self):
        self.od_styles = FileOpenDialog(self)
        self.mm_menu = MainMenu(self)
        self.mi_file = self.mm_menu.CreateMenuItem()
        self.mi_load_style = self.mm_menu.CreateMenuItem()
        self.mi_exit = self.mm_menu.CreateMenuItem()
        self.chk_animate = CheckBox(self)
        self.trk_frame_delay = TrackBar(self)
        self.lbl_frame_delay = Label(self)
        self.grp_indicator_type = RadioGroup(self)
        self.grp_indicator_size = RadioGroup(self)
        self.grp_indicator_color = RadioGroup(self)
        self.cbx_vcl_style = ComboBox(self)
        self.lbl_vcl_style = Label(self)
        self.ai = ActivityIndicator(self)
        self.cbx_form_color = ColorBox(self)
        self.lbl_form_color = Label(self)

    def __config_comps(self):
        self.caption = "Activity Indicator sample"
        self.SetProps(ClientHeight=328, ClientWidth=452, Position="poScreenCenter", OnClose=self.__on_form_close)
        self.SetProps(Menu=self.mm_menu)

        # Configure the menu items
        self.mm_menu.Items.Insert(0, self.mi_file)
        self.mi_file.Insert(0, self.mi_load_style)
        self.mi_file.Insert(1, self.mi_exit)

        # Configure the menu items
        self.mi_file.SetProps(Caption="File")
        self.mi_load_style.SetProps(Caption="Load Styles...", OnClick=self.__on_load_style_click)
        self.mi_exit.SetProps(Caption="Exit", OnClick=(lambda sender: Application.Terminate()))

        # Configure the FileOpenDialog
        self.od_styles.SetProps(Title="Select the Vcl Styles directory",
                                options=["fdoPickFolders", "fdoPathMustExist", "fdoForceFileSystem"],
                                OkButtonLabel="Select")

        # Configure further components
        self.lbl_frame_delay.SetProps(Parent=self, Left=245, Top=55, Width=88, Height=15, Caption='Fame Delay (50)')
        self.lbl_vcl_style.SetProps(Parent=self, Left=20, Top=124, Width=49, Height=15, Alignment="taRightJustify",
                                    Caption='VCL Style')
        self.lbl_form_color.SetProps(Parent=self, Left=245, Top=126, Width=176, Height=15,
                                     Caption='Form Color (Windows Style Only)')
        self.chk_animate.SetProps(Parent=self, Left=254, Top=20, Width=96, Height=17, Caption='Animate', TabOrder=0,
                                  OnClick=self.__chk_animate_click)
        self.trk_frame_delay.SetProps(Parent=self, Left=238, Top=74, Width=203, Height=28, Max=15, Min=3, Position=5,
                                      TabOrder=1, OnChange=self.__trk_frame_delay_change)
        self.ai.SetProps(Parent=self, Left=20, Top=20)
        self.cbx_vcl_style.SetProps(Parent=self, Left=20, Top=145, Width=197, Height=23, Style="csDropDownList",
                                    TabOrder=2, OnChange=self.__cbx_vcl_style_change)
        self.cbx_form_color.SetProps(Parent=self, Left=245, Top=145, Width=188, Height=22, TabOrder=3,
                                     OnChange=self.__cbx_form_color_change)

        self.grp_indicator_type.SetProps(Parent=self, Left=20, Top=193, Width=145, Height=117, Caption='Indicator Type',
                                         TabOrder=4, OnClick=self.__grp_indicator_type_click)
        self.grp_indicator_type.Items.Add('aitMomentumDots')
        self.grp_indicator_type.Items.Add('aitRotatingSector')
        self.grp_indicator_type.Items.Add('aitSectorRing')
        self.grp_indicator_type.SetProps(ItemIndex=0)

        self.grp_indicator_size.SetProps(Parent=self, Left=184, Top=193, Width=125, Height=117,
                                         Caption='Indicator Size', TabOrder=5, OnClick=self.__grp_indicator_size_click)
        self.grp_indicator_size.Items.Add('aisSmall')
        self.grp_indicator_size.Items.Add('aisMedium')
        self.grp_indicator_size.Items.Add('aisLarge')
        self.grp_indicator_size.Items.Add('aisXLarge')
        self.grp_indicator_size.SetProps(ItemIndex=1)

        self.grp_indicator_color.SetProps(Parent=self, Left=328, Top=193, Width=105, Height=117,
                                          Caption='Indicator Color', TabOrder=6,
                                          OnClick=self.__grp_indicator_color_click)
        self.grp_indicator_color.Items.Add('aicBlack')
        self.grp_indicator_color.Items.Add('aicWhite')
        self.grp_indicator_color.SetProps(ItemIndex=0)

        self.__sm = StyleManager()
        for style_name in self.__sm.StyleNames:
            self.cbx_vcl_style.Items.Add(style_name)
        self.cbx_vcl_style.ItemIndex = self.cbx_vcl_style.Items.IndexOf(self.__sm.ActiveStyle.Name)

    @staticmethod
    def __on_form_close(sender, action):
        action.Value = caFree

    def __on_load_style_click(self, sender):
        if self.od_styles.Execute():
            for file in os.listdir(self.od_styles.FileName):
                if file.endswith(".vsf"):
                    style_file_path = os.path.join(self.od_styles.FileName, file)
                    valid_style, style_info = self.__sm.IsValidStyle(style_file_path)
                    if valid_style and not (style_info.Name in self.cbx_vcl_style.Items):
                        self.__sm.LoadFromFile(style_file_path)

            self.cbx_vcl_style.Items.Clear()
            for style_name in self.__sm.StyleNames:
                self.cbx_vcl_style.Items.Add(style_name)

        self.cbx_vcl_style.Sorted = True
        self.cbx_vcl_style.ItemIndex = self.cbx_vcl_style.Items.IndexOf(self.__sm.ActiveStyle.Name)
        self.BringToFront()

    def __chk_animate_click(self, sender):
        self.ai.Animate = self.chk_animate.Checked

    def __trk_frame_delay_change(self, sender):
        self.ai.FrameDelay = self.trk_frame_delay.Position * 10
        self.lbl_frame_delay.Caption = f"Frame Delay ({self.ai.FrameDelay})"

    def __grp_indicator_type_click(self, sender):
        self.ai.IndicatorType = self.grp_indicator_type.Items[self.grp_indicator_type.ItemIndex]

    def __grp_indicator_size_click(self, sender):
        self.ai.IndicatorSize = self.grp_indicator_size.Items[self.grp_indicator_size.ItemIndex]

    def __grp_indicator_color_click(self, sender):
        self.ai.IndicatorColor = self.grp_indicator_color.Items[self.grp_indicator_color.ItemIndex]

    def __cbx_vcl_style_change(self, sender):
        style_ = self.cbx_vcl_style.Text
        self.__sm.SetStyle(style_)
        self.lbl_form_color.Enabled = StyleServices().IsSystemStyle
        self.cbx_form_color.Enabled = StyleServices().IsSystemStyle

    def __cbx_form_color_change(self, sender):
        self.Color = self.cbx_form_color.Selected


def main():
    Application.Initialize()
    Application.Title = "Activity Indicator"
    main_form = ActivityIndicatorForm(Application)
    main_form.Show()
    FreeConsole()
    Application.Run()
    main_form.Destroy()


# Use of __name__ & __main__
# When the Python interpreter reads a code file, it completely executes the code in it.
# For example, in a file my_module.py, when executed as the main program, the __name__ attribute will be '__main__',
# however if it is used importing it from another module: import my_module, the __name__ attribute will be 'my_module'.
if __name__ == '__main__':
    main()

    # Terminate normally
    sys.exit(0)
