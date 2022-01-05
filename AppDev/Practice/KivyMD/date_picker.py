from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_file('date.kv')

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.open()

MainApp().run()
