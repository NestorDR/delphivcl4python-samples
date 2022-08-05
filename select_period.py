# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------------------
# Name:       select_period.py
# Purpose:    DelphiVCL for Python sample
#
# Author:     Nestor D R
# Version:    0.0.1
#
# Copyright:  2020-2022 Embarcadero Technologies, Inc.
# License:    https://github.com/Embarcadero/DelphiVCL4Python/blob/main/LICENSE.md
# ---------------------------------------------------------------------------------

# --- Third Party libraries ---
# delphivcl: Delphi's VCL library as a Python module for building native Windows GUI Applications
#            Visit https://docwiki.embarcadero.com/Libraries/Alexandria/en/Vcl.StdCtrls (standard)
#                  https://docwiki.embarcadero.com/Libraries/Alexandria/en/Vcl.ComCtrls (COM)
#                  https://docwiki.embarcadero.com/Libraries/Alexandria/en/Vcl (Visual Component Library)
#                  https://functionx.com/bcb/index.htm
from delphivcl import Abort, Application, Button, caFree, ComboBox, DateTimePicker, Edit, Form, FreeConsole, Label, \
    MB_OK

# --- Python modules ---
# datetime: module which supplies classes to work with date and time.
from datetime import datetime, timedelta
# inspect: module which provides several useful functions to help get information about live objects such as modules,
#          classes, methods, functions, tracebacks, frame objects, and code objects
import inspect
# re: module which provides regular expression matching operations similar to those found in Perl.
import re
# sys: module which provides access to some variables used or maintained by the interpreter and to functions that
#      interact strongly with the interpreter.
import sys

# --- App modules ---
from view import layout


class PeriodForm(Form):
    """
    Create a Class to build a basic Form
    """

    REST_OF_TODAY: int = 0
    TOMORROW: int = 1
    REST_OF_THE_WEEK: int = 2
    NEXT_WEEK: int = 3
    REST_OF_THE_MONTH: int = 4
    NEXT_MONTH: int = 5

    def __init__(self, owner):
        self.container_width = layout.DEFAULT_CONTAINER_WIDTH
        self.container_height = layout.DEFAULT_CONTAINER_HEIGHT

        self.Caption = "Select period..."
        self.SetBounds(0, 0, self.container_width, self.container_height)
        self.Position = "poScreenCenter"
        self.Color = layout.BACKGROUND_COLOR

        # Create fake grid layout fake-grid mimicked by GRID_ROWS_HEIGHT and GRID_COLUMNS_WIDTH, in order to place
        #   each control based on Place layout manager
        self.fake_grid = layout.FakeGridLayout(layout.DEFAULT_GRID_ROWS_HEIGHT,
                                               layout.DEFAULT_GRID_COLUMNS_WIDTH)
        # Create controls in the GUI
        self.__create_controls()

        # Flag to cancel execution thread
        self.cancel_execution_ = False

    def __create_controls(self):
        """
        Create and add the controls to the container thought as a grid, but positioning them after translation to Place
          positioning.
        """

        # Get fake grid to var to made easier its referenced
        fk = self.fake_grid

        # Row Nº 1 - Legend
        row_number_ = 1
        x_, y_ = fk.get_place(row_number_, 1)  # get absolute (x, y) Place for control in fake row, col =  1, 1
        label_ = self.__create_label("Select a default date range or set your own (weeks starting on Sunday).",
                                     x_, y_)
        self.lblLegend = label_

        # Row Nº 2 - Default date ranges
        row_number_ += 1
        x_, y_ = fk.get_place(row_number_, 1)  # get absolute (x, y) Place for control in fake row, col =  2, 1
        self.lblDefaultRanges = self.__create_label("Date range", x_, y_)
        x_, y_ = fk.get_place(2, 2)  # get absolute (x, y) Place for control in fake row, col =  2, 2
        items_ = ["Rest of Today", "Tomorrow", "Rest of the week", "Next week", "Rest of the month", "Next month"]
        self.cboDefaultRanges = \
            self.__create_combobox(items_, x_=x_, y_=y_,
                                   width_=(layout.DEFAULT_INPUT_CONTROL_WIDTH + layout.DEFAULT_LEFT_MARGIN) * 2
                                          + layout.DEFAULT_LABEL_WIDTH)
        self.cboDefaultRanges.OnSelect = self.__cbo_default_ranges_select

        # Row Nº 3 - From Date and From Hour
        row_number_ += 1
        x_, y_ = fk.get_place(row_number_, 1)  # get absolute (x, y) Place for control in fake row, col =  3, 1
        self.lblFromDate = self.__create_label("From date", x_, y_)
        x_, y_ = fk.get_place(row_number_, 2)  # get absolute (x, y) Place for control in fake row, col =  3, 2
        self.dtpFromDate = self.__create_datepicker(x_=x_, y_=y_)
        self.dtpFromDate.OnChange = self.__dtp_from_date_change
        x_, y_ = fk.get_place(row_number_, 3)  # get absolute (x, y) Place for control in fake row, col =  3, 3
        hour_width_ = int(layout.DEFAULT_INPUT_CONTROL_WIDTH / 2)
        self.lblFromHour = self.__create_label("From hour", x_ + hour_width_, y_)
        x_, y_ = fk.get_place(row_number_, 4)  # get absolute (x, y) Place for control in fake row, col =  3, 4
        self.edtFromHour = self.__create_edit(alignment_="taCenter", x_=x_+hour_width_, y_=y_, width_=hour_width_)
        self.edtFromHour.OnExit = self.__edt_hour_exit

        # Row Nº 4 - To Date and To Hour
        row_number_ += 1
        x_, y_ = fk.get_place(row_number_, 1)  # get absolute (x, y) Place for control in fake row, col =  4, 1
        self.lblToDate = self.__create_label("To date", x_, y_)
        x_, y_ = fk.get_place(row_number_, 2)  # get absolute (x, y) Place for control in fake row, col =  3, 4
        self.dtpToDate = self.__create_datepicker(x_=x_, y_=y_)
        x_, y_ = fk.get_place(row_number_, 3)  # get absolute (x, y) Place for control in fake row, col =  4, 3
        self.lblToHour = self.__create_label("To hour", x_ + hour_width_, y_)
        x_, y_ = fk.get_place(row_number_, 4)  # get absolute (x, y) Place for control in fake row, col =  4, 4
        self.edtToHour = self.__create_edit(alignment_="taCenter", x_=x_+hour_width_, y_=y_, width_=hour_width_)
        self.edtToHour.OnExit = self.__edt_hour_exit

        # Setting the default value
        self.cboDefaultRanges.ItemIndex = PeriodForm.NEXT_WEEK
        self.__cbo_default_ranges_select(self.cboDefaultRanges)

        # Row Nº 5 - Empty
        row_number_ += 1

        # Row Nº 6 - Buttons
        row_number_ += 1
        total_width = (layout.DEFAULT_BUTTON_LEFT_MARGIN + layout.DEFAULT_BUTTON_WIDTH)
        x_, y_ = fk.get_place(row_number_, 4)  # get absolute x Place for 1º button in fake row 4
        self.btnCancel = self.__create_button('Cancel', self.btn_cancel_click, x_=x_ - total_width, y_=y_)
        self.btnOk = self.__create_button('Ready', self.btn_ok_click, x_=x_, y_=y_)

        # Close action
        self.OnClose = self.__on_form_close

    def __create_label(self,
                       caption_: str = 'New Label',
                       x_: int = 0, y_: int = 0) -> Label:
        """
        Add a new Label to the GUI
        :param caption_: string of text to show in the control
        :param x_: horizontal offset in pixels for displaying control
        :param y_:  vertical offset in pixels for displaying control

        :return: a new Label
        """
        # Create new label
        new_label_ = Label(self)
        new_label_.SetProps(Parent=self, Caption=caption_,
                            Left=x_, Top=y_ + layout.DEFAULT_LABEL_TOP_OFFSET)

        return new_label_

    def __create_edit(self,
                      text_: str = "",
                      enabled_: bool = True,
                      alignment_: str = "taLeftJustify",
                      x_: int = 0, y_: int = 0,
                      width_: int = layout.DEFAULT_INPUT_CONTROL_WIDTH,
                      height_: int = layout.DEFAULT_ROW_HEIGHT) -> Edit:
        """
        Add a new Edit to the GUI
        :param text_: string of text to show in the control
        :param enabled_: flag to indicate whether the control is displayed enabled or disabled
        :param alignment_: determines how the text is aligned within the text edit control,
                           allowed values: taLeftJustify, taCenter, taRightJustify
        :param x_: horizontal offset in pixels for displaying control
        :param y_:  vertical offset in pixels for displaying control
        :param width_: width of the control in pixels
        :param height_: height of the control in pixels

        :return: a new Edit
        """
        edit_ = Edit(self)
        edit_.SetProps(Parent=self,
                       Text=text_,
                       Enabled=enabled_,
                       Alignment=alignment_,
                       Left=x_, Top=y_,
                       Width=width_, Height=height_)

        return edit_

    def __create_combobox(self,
                          items_: [],
                          enabled_: bool = True,
                          x_: int = 0, y_: int = 0,
                          width_: int = layout.DEFAULT_INPUT_CONTROL_WIDTH,
                          height_: int = layout.DEFAULT_ROW_HEIGHT) -> ComboBox:
        """
        Add a new ComboBox to the GUI
        :param items_: list with all the items to show
        :param enabled_: flag to indicate whether the control is displayed enabled or disabled
        :param x_: horizontal offset in pixels for displaying control
        :param y_:  vertical offset in pixels for displaying control
        :param width_: width of the control in pixels
        :param height_: height of the control in pixels

        :return: a new ComboBox
        """
        combobox_ = ComboBox(self)
        # Visit: https://www.delphipower.xyz/guide_8/the_combobox_component.html
        #        https://www.delphipower.xyz/guide_6/combo_boxes.html
        combobox_.SetProps(Parent=self,
                           Style="csDropDownList",
                           Enabled=enabled_,
                           Left=x_, Top=y_,
                           Width=width_, Height=height_)

        # Adding items to the new_combobox_
        for item_ in items_:
            combobox_.AddItem(item_, None)
        return combobox_

    def __create_datepicker(self,
                            datetime_: datetime = datetime.today(),
                            enabled_: bool = True,
                            x_: int = 0, y_: int = 0,
                            width_: int = layout.DEFAULT_INPUT_CONTROL_WIDTH,
                            height_: int = layout.DEFAULT_ROW_HEIGHT) -> DateTimePicker:
        """
        Add a new DateTimePicker to the GUI
        :param datetime_: the control value
        :param enabled_: flag to indicate whether the control is displayed enabled or disabled
        :param x_: horizontal offset in pixels for displaying control
        :param y_:  vertical offset in pixels for displaying control
        :param width_: width of the control in pixels
        :param height_: height of the control in pixels

        :return: a new DateTimePicker
        """
        dt_picker_ = DateTimePicker(self)
        dt_picker_.SetProps(Parent=self,
                            Datetime=datetime_,
                            Format="dd/MM/yyyy",
                            Enabled=enabled_,
                            Left=x_, Top=y_,
                            Width=width_, Height=height_)

        return dt_picker_

    def __create_button(self,
                        caption_: str = 'New button',
                        command_=None,
                        enabled_: bool = True,
                        x_: int = 0, y_: int = 0,
                        width_: int = layout.DEFAULT_BUTTON_WIDTH, height_: int = layout.DEFAULT_BUTTON_HEIGHT) \
            -> Button:
        """
        Add a new button to the GUI using Place layout manager
        :param caption_: string of text to show in the widget
        :param command_: a callback to be invoked when the button is pressed
        :param enabled_: flag to indicate whether the widget is displayed enabled or disabled
        :param x_: horizontal offset in pixels for displaying widget
        :param y_:  vertical offset in pixels for displaying widget
        :param width_: width for displaying widget
        :param height_: height of the widget in pixels

        :return: a new button
        """
        button_ = Button(self)
        button_.SetProps(Parent=self, Caption=caption_, OnClick=command_,
                         Left=x_, Top=y_,
                         Width=width_, Height=height_)
        return button_

    @staticmethod
    def __on_form_close(sender, action):
        """
        The form is closed and all allocated memory for the form is freed
        Visit: https://docwiki.embarcadero.com/Libraries/Alexandria/en/Vcl.Forms.TCloseAction
        :param sender: parent form
        :param action: close action describes how a form should respond when it is closed
        """
        action.Value = caFree

    def __cbo_default_ranges_select(self, sender):
        """
        Occurs when the user selects a string in the drop-down list
        Identifies and sets date range based on default options
        :param sender: parent combobox component
        """
        def __current_or_next_saturday(date_):
            # Week finishes on Saturday. If today is Saturday, today ends the week, else find next Saturday.
            # Visit: http://stackoverflow.com/questions/8801084/ddg#8801540
            return date_ if date_.weekday() == 5 else date_ + timedelta(days=(4 - date_.weekday()) % 7 + 1)

        def __last_day_of_month(date_):
            # The day 28 exists in every month. 4 days later, it's always next month
            next_month = date_.replace(day=28) + timedelta(days=4)
            # Subtracting the number of the current day brings us back one month
            return next_month - timedelta(days=next_month.day)

        today_ = datetime.today()
        if sender.ItemIndex == PeriodForm.REST_OF_TODAY:
            from_date_ = today_
            to_date_ = today_

        elif sender.ItemIndex == PeriodForm.TOMORROW:
            tomorrow_ = today_ + timedelta(days=1)
            from_date_ = tomorrow_.replace(hour=0, minute=0, second=0, microsecond=0)
            to_date_ = tomorrow_

        elif sender.ItemIndex == PeriodForm.REST_OF_THE_WEEK:
            saturday_ = __current_or_next_saturday(today_)
            from_date_ = today_
            to_date_ = saturday_

        elif sender.ItemIndex == PeriodForm.NEXT_WEEK:
            saturday_ = __current_or_next_saturday(today_)
            from_date_ = (saturday_ + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)     # Sunday
            to_date_ = (saturday_ + timedelta(days=7))

        elif sender.ItemIndex == PeriodForm.REST_OF_THE_MONTH:
            from_date_ = today_      # Sunday
            to_date_ = __last_day_of_month(today_)

        elif sender.ItemIndex == PeriodForm.NEXT_MONTH:
            from_date_ = \
                (__last_day_of_month(today_) + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            to_date_ = __last_day_of_month(from_date_)

        else:
            # Force PeriodForm.REST_OF_TODAY:
            from_date_ = today_
            to_date_ = today_

        # Set date time range in datetimepickers and edits
        self.dtpFromDate.DateTime = from_date_.strftime("%Y-%m-%d %H:%M:%S")
        self.dtpToDate.MinDate = from_date_.strftime("%Y-%m-%d")
        self.dtpToDate.DateTime = to_date_.replace(hour=23, minute=59, second=59, microsecond=999999)\
            .strftime("%Y-%m-%d %H:%M:%S")

        time_tuple_ = self.dtpFromDate.Time
        self.edtFromHour.Text = f"{time_tuple_[3]:0>2}:{time_tuple_[4]:0>2}"
        time_tuple_ = self.dtpToDate.Time
        self.edtToHour.Text = f"{time_tuple_[3]:0>2}:{time_tuple_[4]:0>2}"

    def __dtp_from_date_change(self, sender):
        """
        Occurs when the entered date in the component changes
        Reset the minimum date allowed in the ToDate component
        :param sender: parent datetimepicker component
        """
        if self.dtpToDate.DateTime < sender.DateTime:
            year_ = sender.DateTime[0]
            month_ = sender.DateTime[1]
            day_ = sender.DateTime[2]
            self.dtpToDate.MinDate = datetime(year_, month_, day_)

    def __edt_hour_exit(self, sender):
        """
        Occurs when the input focus shifts away from one control to another
        Validates the entered time, if it is incorrect then aborts/cancels the exit
        :param sender: parent edit component
        """
        # Check valid hour
        hour_minute_ = sender.Text

        # Try to normalize to HH:MM format
        hh_mm_ = hour_minute_.split(":")
        if len(hh_mm_) == 2:
            # Fill to the left up to 2 zeros
            hh_mm_[0] = hh_mm_[0].rjust(2, '0')
            hh_mm_[1] = hh_mm_[1].rjust(2, '0')
            hour_minute_ = ':'.join(hh_mm_)
        else:
            # Fill to the right up to 4 zeros
            hour_minute_ = hour_minute_.ljust(4, '0')
            if len(hour_minute_) == 4:
                hh_mm_ = [hour_minute_[0:2], hour_minute_[2:4]]
                hour_minute_ = ':'.join(hh_mm_)

        # Regex to check valid time in 24-hour format
        if self.is_hh24_mm_(hour_minute_):
            sender.Text = hour_minute_
        else:
            Abort()

    @staticmethod
    def is_hh24_mm_(s) -> bool:
        """
        Validates that the string is in the format HH:MM. 0 to 24 hours in HH, and 0 to 59 minutes in MM
        :param s: string to evaluate

        :return: true if is right, otherwise false
        """
        regex_pattern_hh24_mm_ = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
        return not regex_pattern_hh24_mm_.match(s) is None

    def btn_cancel_click(self, sender):
        """
        Exit application
        """
        self.cancel_execution_ = True
        self.Close()

    def btn_ok_click(self, sender):
        """
        Shows a message informing the selected date range
        :param sender: parent button component
        """
        try:
            from_hour_ = self.edtFromHour.Text
            if not self.is_hh24_mm_(from_hour_):
                self.edtFromHour.SetFocus()
                self.Owner.MessageBox('From hour is not valid.', self.Owner.Title, MB_OK)
                return

            to_hour_ = self.edtToHour.Text
            if not self.is_hh24_mm_(to_hour_):
                self.edtToHour.SetFocus()
                self.Owner.MessageBox('To hour is not valid.', self.Owner.Title, MB_OK)
                return

            from_date_ = datetime(*self.dtpFromDate.DateTime[0:3], ).strftime(f'%Y-%m-%d {from_hour_}:00:000')
            to_date_ = datetime(*self.dtpToDate.DateTime[0:3]).strftime(f'%Y-%m-%d {to_hour_}:59:999')

            format_ = "%Y-%m-%d %H:%M:%S:%f"
            if datetime.strptime(to_date_, format_) < datetime.strptime(from_date_, format_):
                self.dtpToDate.SetFocus()
                self.Owner.MessageBox('End date and time is less than start date.', self.Owner.Title, MB_OK)
                return

            template_ = 'Date range selected is "@FromDate" to "@ToDate".'
            message_ = template_.replace('@FromDate', from_date_).replace('@ToDate', to_date_)
            self.Owner.MessageBox(message_, self.Owner.Title, MB_OK)
        except Exception as e:
            print(f'Ops, something is wrong.\nMethod: {inspect.stack()[0][0].f_code.co_name}.',
                  {sys.exc_info()[0]}, e)
            raise e


def main():
    Application.Initialize()
    Application.Title = "Select Period"
    main_form_ = PeriodForm(Application)
    main_form_.Show()
    FreeConsole()
    Application.Run()
    main_form_.Destroy()
    Application.Terminate()
    if main_form_.cancel_execution_:
        sys.exit('Canceled by user.')
    del main_form_


# Use of __name__ & __main__
# When the Python interpreter reads a code file, it completely executes the code in it.
# For example, in a file my_module.py, when executed as the main program, the __name__ attribute will be '__main__',
# however if it is used importing it from another module: import my_module, the __name__ attribute will be 'my_module'.
if __name__ == '__main__':
    main()

    # Terminate normally
    sys.exit(0)
