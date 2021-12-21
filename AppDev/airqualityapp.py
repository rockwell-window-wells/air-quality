from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.core.window import Window

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Window.size = (800, 600)
Window.minimum_width, Window.minimum_height = Window.size

# class ContentNavigationDrawer(BoxLayout):
#     pass

# class ItemDrawer(OneLineIconListItem):
#     icon = StringProperty()

class AirQualityApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_file('airquality.kv')

    # Click OK in date picker
    def on_save(self, instance, value, date_range):
        # print(instance, value, date_range)
        # self.root.ids.date_label.text = str(value)
        # self.root.ids.range_label.text = str(date_range)
        self.root.ids.date_label.text = str(date_range[0])

    # Click Cancel in date picker
    def on_cancel(self, instance, value):
        self.root.ids.date_label.text = "You Clicked Cancel"

    def show_date_picker(self):
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()


if __name__ == '__main__':
    AirQualityApp().run()
