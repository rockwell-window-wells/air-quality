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
from kivy.uix.checkbox import CheckBox
from kivy.uix.recycleview import RecycleView

from kivy.config import Config
from kivy.core.window import Window
from libs.layout import KV
from libs.datamethods import refresh_data, prepare_data, plot_data
from libs.exportmethods import generatesinglePDF, generatemultiPDF
import os, sys
from kivy.resources import resource_add_path, resource_find
from os.path import exists
# from libs.datamethods import prepare_data
# from libs.datamethods import plot_data

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Window.size = (1000, 750)
Window.minimum_width, Window.minimum_height = Window.size

# colors = {
#     "Green": {
#         "50": "b8d87a",
#         "100": "b8d87a",
#         "200": "b8d87a",
#         "300": "b8d87a",
#         "400": "b8d87a",
#         "500": "b8d87a",
#         "600": "b8d87a",
#         "700": "b8d87a",
#         "800": "b8d87a",
#         "900": "b8d87a",
#         "A100": "b8d87a",
#         "A200": "b8d87a",
#         "A400": "b8d87a",
#         "A700": "b8d87a",
#     },
#     "Light": {
#         "StatusBar": "E0E0E0",
#         "AppBar": "F5F5F5",
#         "Background": "FAFAFA",
#         "CardsDialogs": "FFFFFF",
#         "FlatButtonDown": "cccccc",
#     },
#     "Dark": {
#         "StatusBar": "000000",
#         "AppBar": "212121",
#         "Background": "303030",
#         "CardsDialogs": "424242",
#         "FlatButtonDown": "999999",
#     }
# }


class RootScreen(MDScreen):
    pass


class HomeScreen(MDScreen):
    pass


class AnalysisScreen(MDScreen):
    date = None         # Analysis date (single calendar day)
    dates = None        # Analysis dates (multiple day analysis)
    t_start = None      # Analysis start time
    t_end = None        # Analysis end time
    dt_start = None     # Datetime version of t_start
    dt_end = None       # Datetime version of t_end
    snackbar = None     # Holding variable for status snackbar
    time_range_dialog = None       # Holding variable for time dialog
    refresh_dialog = None   # Holding variable for refresh data dialog
    export_dialog = None    # Holding variable for export dialog
    twa = None          # Time-weighted average over the time chosen (doesn't assume 8 hours)
    peak = None         # Maximum styrene value recorded during time range of interest
    ste = None          # Maximum short term exposure in a 15 minute window
    img_src = StringProperty('assets/Styrene-3D-balls.png')

    # Snackbar for showing status messages (better than allocating space to labels)
    def snackbar_show(self, snackbartext):
        self.snackbar = Snackbar(text = snackbartext)
        self.snackbar.open()

     # Refresh the data from the single day analysis screen
    def refreshdata_btn(self, datadirectory):
        # NOTE: THIS COULD BE UPDATED LATER TO GIVE THE DETAILS OF THE REFRESH
        # IN A DIALOG BOX SO THE USER KNOWS HOW LONG TO WAIT. OR FIGURE OUT HOW
        # TO ADD A PROGRESS BAR HERE.
        refresh_data(datadirectory)
        # status_text = "Data has been refreshed"
        # self.snackbar_show(status_text)
        self.show_refresh_dialog()

    def show_refresh_dialog(self, *args):
        theme_cls = ThemeManager()
        theme_cls.theme_style = "Light"
        theme_cls.primary_palette = "LightGreen"
        theme_cls.primary_hue = "400"

        if not self.refresh_dialog:
            self.refresh_dialog = MDDialog(
                title="Data Refresh Complete",
                text="All raw data has been prepared for use.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        font_style="Button",
                        on_release=self.close_refresh_dialog
                    ),
                ],
            )
        self.refresh_dialog.open()

    def close_refresh_dialog(self, *args):
        self.refresh_dialog.dismiss(force=True)

    ### Functions for choosing the date in single date analysis ###
    def show_single_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_single_date_save)
        date_dialog.open()

    def on_single_date_save(self, instance, value, date_range):
        self.date = value
        self.dates = None
        print("self.date = {}\nself.dates = {}".format(self.date, self.dates))
        # print(instance, value, date_range)

    ### Functions for choosing the date in single date analysis ###
    def show_multi_date_picker(self):
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_save=self.on_multi_date_save)
        date_dialog.open()

    def on_multi_date_save(self, instance, value, date_range):
        self.dates = date_range
        self.date = None
        print("self.date = {}\nself.dates = {}".format(self.date, self.dates))

    ### Functions for choosing analysis times ###
    def show_time_dialog(self, *args):
        theme_cls = ThemeManager()
        theme_cls.theme_style = "Light"
        theme_cls.primary_palette = "LightGreen"
        theme_cls.primary_hue = "400"

        if not self.time_range_dialog:
            self.time_range_dialog = MDDialog(
                title="Set Time Range",
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
        self.time_range_dialog.open()

    def set_time_dialog(self, *args):
        self.time_range_dialog.dismiss(force=True)
        if not self.t_start or not self.t_end:
            statustext = "MISSING TIME RANGE. Please choose time range before running analysis."
        else:
            statustext = "TIME RANGE SET: {} to {}".format(self.t_start, self.t_end)
        self.snackbar_show(statustext)

    def clear_time_dialog(self, *args):
        self.t_start = None
        self.t_end = None
        statustext = "TIME RANGE CLEARED. Please choose time range before running analysis."
        self.snackbar_show(statustext)

    def cancel_time_dialog(self, *args):
        self.time_range_dialog.dismiss(force=True)
        if not self.t_start or not self.t_end:
            statustext = "MISSING TIME RANGE. Please choose time range before running analysis."
            self.snackbar_show(statustext)

    def show_start_time_picker(self, *args):
        time_dialog = MDTimePicker()
        if self.t_start:
            time_dialog.set_time(self.t_start)
        time_dialog.bind(on_save=self.on_start_time_save)
        time_dialog.open()

    def on_start_time_save(self, instance, time):
        self.t_start = time

    def show_end_time_picker(self, *args):
        time_dialog = MDTimePicker()
        if self.t_end:
            time_dialog.set_time(self.t_end)
        time_dialog.bind(on_save=self.on_end_time_save)
        time_dialog.open()

    def on_end_time_save(self, instance, time):
        self.t_end = time

    ### Functions for running analysis on the chosen date and time range ###
    def calculate(self, valueannotations, lineannotations, directory):
        # If the data is from a single day and the time range is chosen:
        if self.date and self.t_start and self.t_end:
            measdata_window, self.dt_start, self.dt_end = prepare_data(self.date, self.date, self.t_start, self.t_end, directory)
            if measdata_window.empty:
                print('ERROR: No data for chosen date and times.')
            else:
                self.twa, self.peak, self.ste, self.img_src = plot_data(measdata_window, self.dt_start, self.dt_end, valueannotations, lineannotations, directory)

                print("TWA: {} ppm".format(self.twa))
                print("Peak: {} ppm".format(self.peak))

        # If the data is from multiple dates and the time range is chosen:
        elif self.dates and self.t_start and self.t_end:
            measdata_window, self.dt_start, self.dt_end = prepare_data(min(self.dates), max(self.dates), self.t_start, self.t_end, directory)
            if measdata_window.empty:
                print('ERROR: No data for chosen date range and times.')
            else:
                self.twa, self.peak, self.ste, self.img_src = plot_data(measdata_window, self.dt_start, self.dt_end, valueannotations, lineannotations, directory)

                print("TWA: {} ppm".format(self.twa))
                print("Peak: {} ppm".format(self.peak))

        elif not self.date and not self.dates:
            self.snackbar_show("Missing date(s). Unable to generate plot.")
        else:
            self.snackbar_show("Missing times. Unable to generate plot.")

    ### Functions for exporting the analysis to a PDF ###
    def export(self, exportdirectory, plot, employee):
        # If the data is for a single day:
        if self.date and not self.dates and self.t_start and self.t_end:
            tstartstr = str(self.t_start)
            tstartstr = tstartstr[0:-3]
            tstartstr = tstartstr.replace(":", "")
            tendstr = str(self.t_end)
            tendstr = tendstr[0:-3]
            tendstr = tendstr.replace(":", "")
            pdfname = str(self.date) + "_{}-{}_Styrene_Report.pdf".format(tstartstr,tendstr)
            generatesinglePDF(self.date, self.t_start, self.t_end, plot, self.twa, self.peak, self.ste, employee, pdfname, exportdirectory)
            # print("PDF report generated for single day")
            # print("Look for {} in {}".format(pdfname, exportdirectory))
            self.show_export_dialog()


        elif self.dates and not self.date and self.t_start and self.t_end:
            tstartstr = str(self.t_start)
            tstartstr = tstartstr[0:-3]
            tstartstr = tstartstr.replace(":", "")
            tendstr = str(self.t_end)
            tendstr = tendstr[0:-3]
            tendstr = tendstr.replace(":", "")
            pdfname = "{}_{}_{}-{}_Styrene_Report.pdf".format(str(min(self.dates)), str(max(self.dates)), tstartstr, tendstr)
            generatemultiPDF(min(self.dates), max(self.dates), self.t_start, self.t_end, plot, self.twa, self.peak, self.ste, employee, pdfname, exportdirectory)
            # print("PDF report generated for multiple dates")
            # print("Look for {} in {}".format(pdfname, exportdirectory))
            self.show_export_dialog()
        elif not self.date and not self.dates:
            self.snackbar_show("Missing date(s). Unable to export data.")
        else:
            self.snackbar_show("Missing time range. Unable to export data.")

    def show_export_dialog(self, *args):
        theme_cls = ThemeManager()
        theme_cls.theme_style = "Light"
        theme_cls.primary_palette = "LightGreen"
        theme_cls.primary_hue = "400"

        if not self.export_dialog:
            self.export_dialog = MDDialog(
                title="Data Export Complete",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        font_style="Button",
                        on_release=self.close_export_dialog
                    ),
                ],
            )
        self.export_dialog.open()

    def close_export_dialog(self, *args):
        self.export_dialog.dismiss(force=True)


class SettingsScreen(MDScreen):

    # Snackbar for showing status messages (better than allocating space to labels)
    def snackbar_show(self, snackbartext):
        self.snackbar = Snackbar(text = snackbartext)
        self.snackbar.open()

    def set_datafolder(self, newfolder):
        # Add a check here to verify that newfolder is a valid folder path string
        self.datafolder = newfolder
        statustext = "Data folder changed to {}".format(self.datafolder)
        self.snackbar_show(statustext)
        # self.datafolderlabel.text = "Data folder changed to: " + self.datafolder
        print(self.datafolder)

    def reset_datafolder(self, defaultfolder):
        self.datafolder = defaultfolder
        statustext = "Data folder reset to {}".format(self.datafolder)
        self.snackbar_show(statustext)
        # self.datafolderlabel.text = "Data folder reset to: " + self.datafolder
        print(self.datafolder)

    def set_exportfolder(self, newfolder):
        # Add a check here to verify that newfolder is a valid folder path string
        self.exportfolder = newfolder
        statustext = "Export folder changed to {}".format(self.datafolder)
        self.snackbar_show(statustext)
        # self.exportfolderlabel.text = "Export folder changed to: " + self.exportfolder
        # print(self.exportfolder)

    def reset_exportfolder(self, defaultfolder):
        self.exportfolder = defaultfolder
        statustext = "Export folder reset to {}".format(self.datafolder)
        self.snackbar_show(statustext)
        # self.exportfolderlabel.text = "Export folder reset to: " + self.exportfolder
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
        # self.theme_cls.colors = colors
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "LightGreen"
        self.theme_cls.primary_hue = "400"
        self.theme_cls.accent_palette = "Amber"
        self.title = "Styrene Analysis Tool"
        self.icon = "assets/RWLettermark.png"

        screen = Builder.load_string(KV)

        return screen


if __name__ == '__main__':
    try:
        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))
        app = AirQualityApp()
        app.run()
        # On close, delete the generated plot images
        i = 0
        while os.path.exists(AirQualityApp.directory + f"/plot{i}.png"):
            os.remove(AirQualityApp.directory + f"/plot{i}.png")
            i += 1

    except Exception as e:
        print(e)
        input("Press enter.")
