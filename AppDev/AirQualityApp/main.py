from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.screen import MDScreen

from kivy.config import Config
from kivy.core.window import Window
from libs.layout import KV

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Window.size = (800, 600)
Window.minimum_width, Window.minimum_height = Window.size

class RootScreen(MDScreen):
    pass

class SettingsScreen(MDScreen):
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

    def reset_datafolder(self):
        # defaultval = self.datafolder_default
        self.datafolder = "Z:/Safety/Inspections & Assessments/Air Samplings/PAC 8000 Data Logs"
        self.folderlabel.text = self.datafolder + " is the new folder path!"
        print(self.datafolder)

    def set_datafolder(self, newfolder):
        self.datafolder = newfolder
        self.folderlabel.text = newfolder + " is the new folder path"
        print(self.datafolder)


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

# class Settings():
#     def __init__(self):
#         self.datafolder = "Z:/Safety/Inspections & Assessments/Air Samplings/PAC 8000 Data Logs"
#
#     def change_datafolder(new_datafolder):
#         self.datafolder = new_datafolder


class AirQualityApp(MDApp):
    # Global settings
    globalstring = StringProperty('testing, testing.....')



    def build(self):
        # App settings
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.title = "Rockwell Styrene Analysis Tool"
        # self.icon = "assets/RockwellSmallLogo.png"
        screen = Builder.load_string(KV)

        # Internal variables (not sure if these should be in the build function, init, or on_start)
        # self.datafolder_default = "Z:/Safety/Inspections & Assessments/Air Samplings/PAC 8000 Data Logs"
        # self.exportfolder_default = "Z:/Safety/Inspections & Assessments/Air Samplings/PAC 8000 Reports"
        # self.datafolder = self.datafolder_default
        # self.exportfolder = self.exportfolder_default
        # self.logfile = self.datafolder + "/LOGGED.csv"

        return screen

    # def on_start(self):
    #     icons_item = {
    #         "calendar-check": "Single Day Styrene",
    #         "calendar-multiple-check": "Multi-Day Styrene",
    #         "database": "Data Settings",
    #         "export": "Export Settings",
    #     }
    #     for icon_name in icons_item.keys():
    #         self.root.ids.content_drawer.ids.md_list.add_widget(
    #             ItemDrawer(icon=icon_name, text=icons_item[icon_name])
    #         )


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
