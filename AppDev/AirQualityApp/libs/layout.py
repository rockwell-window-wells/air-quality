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

                MDBoxLayout:
                    orientation: "vertical"
                    padding: [10]
                    spacing: 10

                    MDBoxLayout:
                        orientation: "horizontal"
                        padding: [10]
                        spacing: 10

                        MDTextField:
                            id: newdatafolderpath
                            hint_text:"Data folder path"
                            pos_hint: {"bottom": 0.3}

                        MDRaisedButton:
                            text: "Set"
                            pos_hint: {"bottom": 0.35}

                        MDRectangleFlatButton:
                            text: "Reset"
                            pos_hint: {"bottom": 0.35}

                    MDBoxLayout:
                        orientation: "horizontal"
                        padding: [10]
                        spacing: 10

                        MDTextField:
                            id: exportfolderpath
                            hint_text:"Export folder path"
                            pos_hint: {"top": 0.75}

                        MDRaisedButton:
                            text: "Set"
                            pos_hint: {"top": 0.75}

                        MDRectangleFlatButton:
                            text: "Reset"
                            pos_hint: {"top": 0.75}


        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                id: content_drawer
                screen_manager: screen_manager
                nav_drawer: nav_drawer

'''
