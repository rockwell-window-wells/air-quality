from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.screen import MDScreen
from kivymd.font_definitions import theme_font_styles

from kivy.config import Config
from kivy.core.window import Window
from libs.layout import KV

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Window.size = (800, 600)
Window.minimum_width, Window.minimum_height = Window.size


class RootScreen(MDScreen):
    pass


class HomeScreen(MDScreen):
    pass


class SingleDayScreen(MDScreen):
    pass


class MultiDayScreen(MDScreen):
    pass


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
        self.title = "Rockwell Styrene Analysis Tool"
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
