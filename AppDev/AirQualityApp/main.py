from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList

from kivy.config import Config
from kivy.core.window import Window
# from libs.navigation_drawer import navigation_helper

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Window.size = (800, 600)
Window.minimum_width, Window.minimum_height = Window.size

KV = '''
# Menu item in the DrawerList list.
<ItemDrawer>:
    theme_text_color: "Custom"
    on_release: self.parent.set_color_item(self)

    IconLeftWidget:
        id: icon
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color


<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None
        height: avatar.height

        Image:
            id: avatar
            size_hint: None, None
            size: 200, 50
            source: "assets/RockwellFullLogo.png"

    ScrollView:

        DrawerList:
            id: md_list

            ItemDrawer:
                text: "Home"
                icon: "home"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "homescreen"

            ItemDrawer:
                text: "Single Day Styrene"
                icon: "calendar-check"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "singledaystyrene"

            ItemDrawer:
                text: "Multi-Day Styrene"
                icon: "calendar-multiple-check"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "multidaystyrene"

            ItemDrawer:
                text: "Settings"
                icon: "application-settings-outline"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "settings"





MDScreen:

    MDToolbar:
        id: toolbar
        pos_hint: {"top": 1}
        elevation: 10
        title: "Navigation"
        left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]


    MDNavigationLayout:

        ScreenManager:
            id: screen_manager

            MDScreen:
                name: "homescreen"

                AnchorLayout:
                    anchor_x: "center"
                    anchor_y: "center"

                    Image:
                        id: titlelogo
                        size_hint: None, None
                        size: 500, 500
                        source: "assets/RockwellTitleLogo.png"



            MDScreen:
                name: "singledaystyrene"

                MDLabel:
                    text: "You have found the Single Day Styrene Screen!"
                    halign: "center"

            MDScreen:
                name: "multidaystyrene"

                MDLabel:
                    text: "Multi-day Styrene Screen!"
                    halign: "center"

            MDScreen:
                name: "settings"

                MDLabel:
                    text: "Settings Screen"
                    halign: "center"



        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                id: content_drawer
                screen_manager: screen_manager
                nav_drawer: nav_drawer

'''
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

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        # self.icon = "assets/RockwellSmallLogo.png"
        self.title = "Rockwell Styrene Analysis Tool"
        screen = Builder.load_string(KV)
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
