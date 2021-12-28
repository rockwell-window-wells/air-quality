from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior, ThemeManager
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.screen import MDScreen
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.snackbar.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

from kivy.config import Config
from kivy.core.window import Window
from libs.layout import KV
from libs.datamethods import refresh_data

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Window.size = (800, 600)
Window.minimum_width, Window.minimum_height = Window.size


class RootScreen(MDScreen):
    pass


class HomeScreen(MDScreen):
    pass


class SingleDayScreen(MDScreen):

    analysis_date = None
    analysis_starttime = None
    analysis_endtime = None
    snackbar = None
    dialog = None

    # Snackbar for showing status messages (better than allocating space to labels)
    def snackbar_show(self, snackbartext):
        self.snackbar = Snackbar(text = snackbartext)
        self.snackbar.open()

    # Refresh the data from the single day analysis screen
    def refreshdata_single(self, datadirectory):
        refresh_data(datadirectory)
        status_text = "Data is being refreshed"
        self.snackbar_show(status_text)

    ### Functions for choosing the date in single date analysis ###
    def show_single_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_save)
        date_dialog.open()

    def on_date_save(self, instance, value, date_range):
        self.analysis_date = value
        # print("{} selected for analysis".format(self.analysis_date))
        status_text = "{} selected for analysis".format(self.analysis_date)
        self.snackbar_show(status_text)

    ### Functions for choosing analysis times ###
    def show_time_dialog(self, *args):
        theme_cls = ThemeManager()

        theme_cls.theme_style = "Light"
        theme_cls.primary_palette = "Green"
        if not self.dialog:
            self.dialog = MDDialog(
                title="Time Range",
                buttons=[
                    MDRaisedButton(
                        text="Start Time",
                        font_style="Button",
                        on_release=self.show_start_time_picker
                    ),
                    MDRaisedButton(
                        text="End Time",
                        font_style="Button",
                        on_release=self.show_end_time_picker
                    ),
                    MDRaisedButton(
                        text="Set",
                        font_style="Button",
                        md_bg_color=theme_cls.accent_color,
                        on_release=self.set_time_dialog
                    ),
                    MDFlatButton(
                        text="Clear",
                        font_style="Button",
                        theme_text_color="Custom",
                        text_color=theme_cls.primary_color,
                        on_release=self.clear_time_dialog
                    ),
                    MDFlatButton(
                        text="Cancel",
                        font_style="Button",
                        theme_text_color="Custom",
                        text_color=theme_cls.primary_color,
                        on_release=self.cancel_time_dialog
                    ),
                ],
            )
        self.dialog.open()

    def set_time_dialog(self, *args):
        # self.analysis_starttime = None
        # self.analysis_endtime = None
        self.dialog.dismiss(force=True)
        if not self.analysis_starttime or not self.analysis_endtime:
            statustext = "MISSING TIME RANGE. Please choose time range before running analysis."
        else:
            statustext = "TIME RANGE SET: {} to {}".format(self.analysis_starttime, self.analysis_endtime)
        self.snackbar_show(statustext)

    def clear_time_dialog(self, *args):
        self.analysis_starttime = None
        self.analysis_endtime = None
        statustext = "TIME RANGE CLEARED. Please choose time range before running analysis."
        self.snackbar_show(statustext)

    def cancel_time_dialog(self, *args):
        self.dialog.dismiss(force=True)
        if not self.analysis_starttime or not self.analysis_endtime:
            statustext = "MISSING TIME RANGE. Please choose time range before running analysis."
            self.snackbar_show(statustext)

    def show_start_time_picker(self, *args):
        time_dialog = MDTimePicker()
        if self.analysis_starttime:
            time_dialog.set_time(self.analysis_starttime)
        time_dialog.bind(on_save=self.on_start_time_save)
        time_dialog.open()

    def on_start_time_save(self, instance, time):
        self.analysis_starttime = time
        status_text = "{} start time".format(self.analysis_starttime)
        self.snackbar_show(status_text)

    def show_end_time_picker(self, *args):
        time_dialog = MDTimePicker()
        if self.analysis_endtime:
            time_dialog.set_time(self.analysis_endtime)
        time_dialog.bind(on_save=self.on_end_time_save)
        time_dialog.open()

    def on_end_time_save(self, instance, time):
        self.analysis_endtime = time
        status_text = "{} end time".format(self.analysis_endtime)
        self.snackbar_show(status_text)

    ### Functions for running analysis on the chosen date and time range ###
    def calculate_single_date(self):
        if self.analysis_date is None:
            self.snackbar_show("Analysis date not set!")
        else:
            status_text = "Generating analysis for {}.".format(self.analysis_date)
            self.snackbar_show(status_text)
        # print("{} selected for analysis".format(self.analysis_date))




class MultiDayScreen(MDScreen):

    def refreshdata_multi(self, datadirectory):
        refresh_data(datadirectory)


class SettingsScreen(MDScreen):

    def set_datafolder(self, newfolder):
        # Add a check here to verify that newfolder is a valid folder path string
        self.datafolder = newfolder
        self.datafolderlabel.text = "Data folder changed to: " + self.datafolder
        print(self.datafolder)

    def reset_datafolder(self, defaultfolder):
        self.datafolder = defaultfolder
        self.datafolderlabel.text = "Data folder reset to: " + self.datafolder
        print(self.datafolder)

    def set_exportfolder(self, newfolder):
        # Add a check here to verify that newfolder is a valid folder path string
        self.exportfolder = newfolder
        self.exportfolderlabel.text = "Export folder changed to: " + self.exportfolder
        print(self.exportfolder)

    def reset_exportfolder(self, defaultfolder):
        self.exportfolder = defaultfolder
        self.exportfolderlabel.text = "Export folder reset to: " + self.exportfolder
        print(self.exportfolder)


class ContentNavigationDrawer(MDBoxLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class AirQualityApp(MDApp):
    # Global settings
    globalstring = StringProperty('testing, testing.....')
    directory = "Z:/Safety/Inspections & Assessments/Air Samplings/PAC 8000 Data Logs"
    export_directory = "Z:/Safety/Inspections & Assessments/Air Samplings/PAC 8000 Reports"
    datafolder_default = StringProperty(directory)
    exportfolder_default = StringProperty(export_directory)
    datafolder = datafolder_default
    exportfolder = exportfolder_default
    logfilestr = directory + "/LOGGED.csv"
    logfile = StringProperty(logfilestr)
    lognamepatternstr = "ARPL-1307_PAC 8000*.txt"
    lognamepattern = StringProperty(lognamepatternstr)
    logfilepatternstr = directory + "/" + lognamepatternstr
    logfilepattern = StringProperty(logfilepatternstr)
    processedfilestr = directory + "/PROCESSED.csv"
    processedfile = StringProperty(processedfilestr)
    pnamepatternstr = "ARPL-1307_PAC 8000*.pkl"
    pnamepattern = StringProperty(pnamepatternstr)
    pfilepatternstr = directory + "/" + pnamepatternstr
    pfilepattern = StringProperty(pfilepatternstr)

    def build(self):
        # App settings
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        # self.theme_cls.accent_palette = "Green"
        self.title = "Styrene Analysis Tool"
        # self.icon = "assets/RockwellSmallLogo.png"
        screen = Builder.load_string(KV)

        return screen


    # These date picker methods should be under the appropriate screen classes
    # # Click OK in date picker
    # def on_save(self, instance, value, date_range):
    #     # print(instance, value, date_range)
    #     # self.root.ids.date_label.text = str(value)
    #     # self.root.ids.range_label.text = str(date_range)
    #     self.root.ids.date_label.text = str(date_range[0])
    #
    # # Click Cancel in date picker
    # def on_cancel(self, instance, value):
    #     self.root.ids.date_label.text = "You Clicked Cancel"
    #
    # def show_date_picker(self):
    #     date_dialog = MDDatePicker(mode="range")
    #     date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
    #     date_dialog.open()


if __name__ == '__main__':
    AirQualityApp().run()
