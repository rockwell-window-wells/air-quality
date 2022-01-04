# Built with:
# Python 3.9.8
# kivy 2.0.0
# kivymd 1.0.0.dev0
# pandas 1.3.4
# numpy 1.19.5
# csv 1.0
# matplotlib 3.4.3
# pyfpdf (imported as fpdf) 1.7.2

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


class RootScreen(MDScreen):
    pass


class HomeScreen(MDScreen):
    def translate_en(self):
        app.english = True
        app.home_title = app.home_title_en
        app.analysis_title = app.analysis_title_en
        app.settings_title = app.settings_title_en
        app.navigation_title = app.navigation_title_en
        app.refresh_data_label = app.refresh_data_en
        app.single_day_label = app.single_day_en
        app.multi_day_label = app.multi_day_en
        app.time_range_label = app.time_range_en
        app.calculate_label = app.calculate_en
        app.export_label = app.export_en
        app.annotate_vals_label = app.annotate_vals_en
        app.annotate_lines_label = app.annotate_lines_en
        app.employee_hint_label = app.employee_hint_en
        app.refresh_dialog_title_label = app.refresh_dialog_title_en
        app.refresh_dialog_text_label = app.refresh_dialog_text_en
        app.time_range_dialog_title_label = app.time_range_dialog_title_en
        app.time_range_dialog_start_label = app.time_range_dialog_start_en
        app.time_range_dialog_end_label = app.time_range_dialog_end_en
        app.clear_btn_label = app.clear_btn_en
        app.cancel_btn_label = app.cancel_btn_en
        app.export_dialog_title_label = app.export_dialog_title_en


        app.settings_title = app.settings_title_en
        app.set_btn_label = app.set_btn_en
        app.reset_btn_label = app.reset_btn_en
        app.data_folder_label = app.data_folder_en
        app.export_folder_label = app.export_folder_en

        self.snackbar_show("Language changed to English")

    def translate_esp(self):
        app.english = False
        app.home_title = app.home_title_esp
        app.analysis_title = app.analysis_title_esp
        app.settings_title = app.settings_title_esp
        app.navigation_title = app.navigation_title_esp
        app.refresh_data_label = app.refresh_data_esp
        app.single_day_label = app.single_day_esp
        app.multi_day_label = app.multi_day_esp
        app.time_range_label = app.time_range_esp
        app.calculate_label = app.calculate_esp
        app.export_label = app.export_esp
        app.annotate_vals_label = app.annotate_vals_esp
        app.annotate_lines_label = app.annotate_lines_esp
        app.employee_hint_label = app.employee_hint_esp
        app.refresh_dialog_title_label = app.refresh_dialog_title_esp
        app.refresh_dialog_text_label = app.refresh_dialog_text_esp
        app.time_range_dialog_title_label = app.time_range_dialog_title_esp
        app.time_range_dialog_start_label = app.time_range_dialog_start_esp
        app.time_range_dialog_end_label = app.time_range_dialog_end_esp
        app.clear_btn_label = app.clear_btn_esp
        app.cancel_btn_label = app.cancel_btn_esp
        app.export_dialog_title_label = app.export_dialog_title_esp


        app.settings_title = app.settings_title_esp
        app.set_btn_label = app.set_btn_esp
        app.reset_btn_label = app.reset_btn_esp
        app.data_folder_label = app.data_folder_esp
        app.export_folder_label = app.export_folder_esp

        self.snackbar_show("Idioma cambiado a Espa\u00F1ol")


    # Snackbar for showing status messages (better than allocating space to labels)
    def snackbar_show(self, snackbartext):
        self.snackbar = Snackbar(text = snackbartext)
        self.snackbar.open()


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
                title= app.refresh_dialog_title_label,
                text= app.refresh_dialog_text_label,
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
                title=app.time_range_dialog_title_label,
                buttons=[
                    MDRaisedButton(
                        text=app.time_range_dialog_start_label,
                        font_style="Button",
                        on_release=self.show_start_time_picker
                    ),
                    MDRaisedButton(
                        text=app.time_range_dialog_end_label,
                        font_style="Button",
                        on_release=self.show_end_time_picker
                    ),
                    MDRaisedButton(
                        text=app.set_btn_label,
                        font_style="Button",
                        md_bg_color=theme_cls.accent_color,
                        on_release=self.set_time_dialog
                    ),
                    MDFlatButton(
                        text=app.clear_btn_label,
                        font_style="Button",
                        theme_text_color="Custom",
                        text_color=theme_cls.primary_color,
                        on_release=self.clear_time_dialog
                    ),
                    MDFlatButton(
                        text=app.cancel_btn_label,
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
            if app.english is True:
                statustext = "MISSING TIME RANGE. Please choose time range before running analysis."
            else:
                statustext = "FALTA RANGO DE TIEMPO. Elija un intervalo de tiempo antes de ejecutar el an\u00E1lisis."
        else:
            if app.english is True:
                statustext = "TIME RANGE SET: {} to {}".format(self.t_start, self.t_end)
            else:
                statustext = "SE HA FIJADO EL RANGO DE TIEMPO: {} to {}".format(self.t_start, self.t_end)
        if self.date and (self.t_start >= self.t_end):
            if app.english is True:
                statustext = "ERROR: Start time is later than end time."
            else:
                statustext = "ERROR: La hora de inicio es posterior a la hora de finalizaci\u00F3n."

        self.snackbar_show(statustext)

    def clear_time_dialog(self, *args):
        self.t_start = None
        self.t_end = None
        if app.english is True:
            statustext = "TIME RANGE CLEARED. Please choose time range before running analysis."
        else:
            statustext = "RANGO DE TIEMPO BORRADO. Elija un intervalo de tiempo antes de ejecutar el an\u00E1lisis."
        self.snackbar_show(statustext)

    def cancel_time_dialog(self, *args):
        self.time_range_dialog.dismiss(force=True)
        if not self.t_start or not self.t_end:
            if app.english is True:
                statustext = "MISSING TIME RANGE. Please choose time range before running analysis."
            else:
                statustext = "FALTA RANGO DE TIEMPO. Elija un intervalo de tiempo antes de ejecutar el an\u00E1lisis."
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
                # print("ERROR: No data for chosen date and times.")
                if app.english is True:
                    self.snackbar_show("ERROR: No data for chosen date and times.")
                else:
                    self.snackbar_show("ERROR: No hay datos para la fecha y hora elegidas.")
            else:
                app.gooddata = True
                self.twa, self.peak, self.ste, self.img_src = plot_data(measdata_window, self.dt_start, self.dt_end, valueannotations, lineannotations, directory)
                app.plotready = True
                print(app.plotready)

                # print("TWA: {} ppm".format(self.twa))
                # print("Peak: {} ppm".format(self.peak))

        # If the data is from multiple dates and the time range is chosen:
        elif self.dates and self.t_start and self.t_end:
            measdata_window, self.dt_start, self.dt_end = prepare_data(min(self.dates), max(self.dates), self.t_start, self.t_end, directory)
            if measdata_window.empty:
                app.gooddata = False
                # print('ERROR: No data for chosen date range and times.')
                if app.english is True:
                    self.snackbar_show("ERROR: No data for chosen dates and times.")
                else:
                    self.snackbar_show("ERROR: No hay datos para las fechas y horas elegidas.")
            else:
                app.gooddata = True
                self.twa, self.peak, self.ste, self.img_src = plot_data(measdata_window, self.dt_start, self.dt_end, valueannotations, lineannotations, directory)
                app.plotready = True
                print(app.plotready)

                # print("TWA: {} ppm".format(self.twa))
                # print("Peak: {} ppm".format(self.peak))

        elif not self.date and not self.dates:
            if app.english is True:
                self.snackbar_show("Missing date(s). Unable to generate plot.")
            else:
                self.snackbar_show("Falta la (s) fecha (s). No se pudo generar la trama.")
        else:
            if app.english is True:
                self.snackbar_show("Missing times. Unable to generate plot.")
            else:
                self.snackbar_show("Tiempos perdidos. No se pudo generar la trama.")

    ### Functions for exporting the analysis to a PDF ###
    def export(self, exportdirectory, plot, employee):
        if app.gooddata is True and app.plotready is True:
            print("All data is there for a good export.")

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
                if app.english is True:
                    self.snackbar_show("Missing date(s). Unable to generate plot.")
                else:
                    self.snackbar_show("Falta la (s) fecha (s). No se pudo generar la trama.")
            else:
                if app.english is True:
                    self.snackbar_show("Missing times. Unable to generate plot.")
                else:
                    self.snackbar_show("Tiempos perdidos. No se pudo generar la trama.")

        elif app.gooddata is True and app.plotready is False:
            if app.english is True:
                self.snackbar_show("ERROR: Data has not been plotted.")
            else:
                self.snackbar_show("ERROR: Los datos no se han representado gr\u00E1ficamente.")

        else:
            print("gooddata: {}\nplotready: {}".format(app.gooddata, app.plotready))
            if app.english is True:
                self.snackbar_show("ERROR: No data for chosen dates and times.")
            else:
                self.snackbar_show("ERROR: No hay datos para las fechas y horas elegidas.")

    def show_export_dialog(self, *args):
        theme_cls = ThemeManager()
        theme_cls.theme_style = "Light"
        theme_cls.primary_palette = "LightGreen"
        theme_cls.primary_hue = "400"

        if not self.export_dialog:
            self.export_dialog = MDDialog(
                title=app.export_dialog_title_label,
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
        if os.path.isdir(newfolder):
            app.datafolder = newfolder
            if app.english is True:
                statustext = "Data folder changed to {}".format(app.datafolder)
            else:
                statustext = "La carpeta de datos cambi\u00F3 a {}".format(app.datafolder)
            self.snackbar_show(statustext)
        else:
            if app.english is True:
                statustext = "Not a valid folder path."
            else:
                statustext = "No es una ruta de carpeta v\u00E1lida"
            self.snackbar_show(statustext)


    def reset_datafolder(self):
        app.datafolder = app.directory
        if app.english is True:
            statustext = "Data folder reset to {}".format(app.datafolder)
        else:
            statustext = "Carpeta de datos restablecida a {}".format(app.datafolder)
        self.snackbar_show(statustext)


    def set_exportfolder(self, newfolder):
        # Add a check here to verify that newfolder is a valid folder path string
        if os.path.isdir(newfolder):
            app.exportfolder = newfolder
            if app.english is True:
                statustext = "Export folder changed to {}".format(app.exportfolder)
            else:
                statustext = "La carpeta de exportaci\u00F3n cambi\u00F3 a {}".format(app.exportfolder)
            self.snackbar_show(statustext)
        else:
            if app.english is True:
                statustext = "Not a valid folder path."
            else:
                statustext = "No es una ruta de carpeta v\u00E1lida"
            self.snackbar_show(statustext)

    def reset_exportfolder(self, defaultfolder):
        app.exportfolder = app.export_directory
        if app.english is True:
            statustext = "Export folder reset to {}".format(app.exportfolder)
        else:
            statustext = "Exportar carpeta restablecida a {}".format(app.exportfolder)
        self.snackbar_show(statustext)


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
    # globalstring = StringProperty('testing, testing.....')
    directory = "Z:/Safety/Inspections & Assessments/Air Samplings/PAC 8000 Data Logs"
    export_directory = "Z:/Safety/Inspections & Assessments/Air Samplings/PAC 8000 Reports"
    datafolder_default = StringProperty(directory)
    exportfolder_default = StringProperty(export_directory)
    datafolder = datafolder_default
    exportfolder = exportfolder_default
    logfilestr = directory + "/LOGGED.csv"
    logfile = StringProperty(logfilestr)
    lognamepatternstr = "*PAC 8000*.txt"
    lognamepattern = StringProperty(lognamepatternstr)
    logfilepatternstr = directory + "/" + lognamepatternstr
    logfilepattern = StringProperty(logfilepatternstr)
    processedfilestr = directory + "/PROCESSED.csv"
    processedfile = StringProperty(processedfilestr)
    pnamepatternstr = "*PAC 8000*.pkl"
    pnamepattern = StringProperty(pnamepatternstr)
    pfilepatternstr = directory + "/" + pnamepatternstr
    pfilepattern = StringProperty(pfilepatternstr)

    ### Labels in English ###
    home_title_en = "Home"
    analysis_title_en = "Analysis"
    navigation_title_en = "Navigation"
    refresh_data_en = "Refresh Data"
    single_day_en = "Single Day"
    multi_day_en = "Multiple Dates"
    time_range_en = "Time Range"
    calculate_en = "Calculate"
    export_en = "Export"
    annotate_vals_en = "Annotate Values"
    annotate_lines_en = "Annotate Lines"
    employee_hint_en = "Employee wearing PAC 8000"
    refresh_dialog_title_en = "Data Refresh Complete"
    refresh_dialog_text_en = "All raw data has been prepared for use."
    time_range_dialog_title_en = "Set Time Range"
    time_range_dialog_start_en = "Start Time"
    time_range_dialog_end_en = "End Time"
    clear_btn_en = "Clear"
    cancel_btn_en = "Cancel"
    export_dialog_title_en = "Data Export Complete"

    settings_title_en = "Settings"
    set_btn_en = "Set"
    reset_btn_en = "Reset"
    data_folder_en = "Data folder path"
    export_folder_en = "Export folder path"

    ### Labels in Spanish ###
    home_title_esp = "Inicio"
    analysis_title_esp = "An\u00E1lisis"
    navigation_title_esp = "Navegaci\u00F3n"
    refresh_data_esp = "Actualizar datos"
    single_day_esp = "Fecha \u00FAnica"
    multi_day_esp = "Fechas multiples"
    time_range_esp = "Intervalo de tiempo"
    calculate_esp = "Calcular"
    export_esp = "Exportar"
    annotate_vals_esp = "Anotar Valores"
    annotate_lines_esp = "Anotar L\u00EDneas"
    employee_hint_esp = "Empleado que lleva el PAC 8000"
    refresh_dialog_title_esp = "Actualizaci\u00F3n de Datos Completa"
    refresh_dialog_text_esp = "Todos los datos brutos se han preparado para su uso."
    time_range_dialog_title_esp = "Establecer Rango de Tiempo"
    time_range_dialog_start_esp = "Inicio"
    time_range_dialog_end_esp = "Finalizaci\u00F3n"
    clear_btn_esp = "Limpiar"
    cancel_btn_esp = "Cancelar"
    export_dialog_title_esp = "Exportaci\u00F3n de datos completa"


    settings_title_esp  = "Ajustes"
    set_btn_esp = "Establecer"
    reset_btn_esp = "Reiniciar"
    data_folder_esp = "Ruta de la carpeta de datos"
    export_folder_esp = "Ruta de la carpeta de exportaci\u00F3n"

    ### Reference variables for text labels ###
    home_title = StringProperty(home_title_en)
    analysis_title = StringProperty(analysis_title_en)
    navigation_title = StringProperty(navigation_title_en)
    refresh_data_label = StringProperty(refresh_data_en)
    single_day_label = StringProperty(single_day_en)
    multi_day_label = StringProperty(multi_day_en)
    time_range_label = StringProperty(time_range_en)
    calculate_label = StringProperty(calculate_en)
    export_label = StringProperty(export_en)
    annotate_vals_label = StringProperty(annotate_vals_en)
    annotate_lines_label = StringProperty(annotate_lines_en)
    employee_hint_label = StringProperty(employee_hint_en)
    refresh_dialog_title_label = StringProperty(refresh_dialog_title_en)
    refresh_dialog_text_label = StringProperty(refresh_dialog_text_en)
    time_range_dialog_title_label = StringProperty(time_range_dialog_title_en)
    time_range_dialog_start_label = StringProperty(time_range_dialog_start_en)
    time_range_dialog_end_label = StringProperty(time_range_dialog_end_en)
    clear_btn_label = StringProperty(clear_btn_en)
    cancel_btn_label = StringProperty(cancel_btn_en)
    export_dialog_title_label = StringProperty(export_dialog_title_en)


    settings_title = StringProperty(settings_title_en)
    set_btn_label = StringProperty(set_btn_en)
    reset_btn_label = StringProperty(reset_btn_en)
    data_folder_label = StringProperty(data_folder_en)
    export_folder_label = StringProperty(export_folder_en)

    english = True
    gooddata = False
    plotready = False


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
