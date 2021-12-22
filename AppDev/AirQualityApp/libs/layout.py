KV = '''
<HomeScreen>:
    name: "homescreen"

    MDBoxLayout:
        # md_bg_color: app.theme_cls.primary_color
        orientation: "vertical"

        AnchorLayout:
            anchor_x: "center"
            anchor_y: "top"

            Image:
                id: titlelogo
                size_hint: None, None
                size: 500, 500
                source: "assets/RockwellTitleLogo.png"

        AnchorLayout:
            anchor_x: "center"
            anchor_y: "top"

            MDGridLayout:
                cols:2
                size_hint: (0.35, 0.35)

                AnchorLayout:
                    anchor_x: "center"
                    anchor_y: "center"

                    MDRaisedButton:
                        text: "English"
                        font_style: "Button"
                        elevation: 5
                        # pos_hint: {"top": 1, "right": 1.0}

                AnchorLayout:
                    anchor_x: "center"
                    anchor_y: "center"

                    MDRaisedButton:
                        text: "Espa\u00F1ol"
                        font_style: "Button"
                        elevation: 5
                        pos_hint: {"top": 1, "right": 1.0}

<SingleDayScreen>:
    name: "singledaystyrene"

    MDGridLayout:
        cols: 2
        padding: 10
        spacing: 10

        MDGridLayout:
            # orientation: "vertical"
            rows: 5
            spacing: 10
            padding: 10
            # md_bg_color: app.theme_cls.accent_color
            size_hint: (0.35, 1)

            MDFloatLayout:

                MDLabel:
                    id: singledaytitle
                    text: "Single Day"
                    font_style: "H5"
                    pos_hint: {"top": 0.75, "x": 0.01}


            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: refreshdata_single
                    text: "Refresh Data"
                    font_style: "Button"
                    # pos_hint: {"top": 0.5, "right": 0.5}

            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: choosedate_single
                    text: "Date"
                    font_style: "Button"
                    pos_hint: {"top": 0.5, "right": 0.5}
                    elevation: 5

            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: timerange_single
                    text: "Time Range"
                    font_style: "Button"
                    pos_hint: {"top": 0.5, "right": 0.5}
                    elevation: 5

            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: calculate_single
                    text: "Calculate"
                    font_style: "Button"
                    md_bg_color: app.theme_cls.accent_color
                    pos_hint: {"top": 0.5, "right": 0.5}
                    elevation: 5

        MDGridLayout:
            # Put the chart here

            # Relevant data below the chart (TWA level, peak levels, name, date, shift, etc.)


<MultiDayScreen>:
    name: "multidaystyrene"

    MDGridLayout:
        cols: 2
        padding: 10
        spacing: 10

        MDGridLayout:
            # orientation: "vertical"
            rows: 5
            spacing: 10
            padding: 10
            # md_bg_color: app.theme_cls.accent_color
            size_hint: (0.35, 1)

            MDFloatLayout:

                MDLabel:
                    id: singledaytitle
                    text: "Multi-Day"
                    font_style: "H5"
                    pos_hint: {"top": 0.75, "x": 0.01}


            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: refreshdata_single
                    text: "Refresh Data"
                    font_style: "Button"
                    # pos_hint: {"top": 0.5, "right": 0.5}

            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: choosedate_single
                    text: "Date Range"
                    font_style: "Button"
                    pos_hint: {"top": 0.5, "right": 0.5}
                    elevation: 5

            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: timerange_single
                    text: "Time Range"
                    font_style: "Button"
                    pos_hint: {"top": 0.5, "right": 0.5}
                    elevation: 5

            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: calculate_single
                    text: "Calculate"
                    font_style: "Button"
                    md_bg_color: app.theme_cls.accent_color
                    pos_hint: {"top": 0.5, "right": 0.5}
                    elevation: 5

        MDGridLayout:
            # Put the chart here

            # Relevant data below the chart (TWA level, peak levels, name, date, shift, etc.)

<SettingsScreen>:
    name: "settings"
    datafolderlabel: datafolderlabel
    exportfolderlabel: exportfolderlabel

    MDBoxLayout:
        orientation: "vertical"
        padding: 10
        spacing: 10

        MDFloatLayout:

            MDLabel:
                id: settingstitle
                text: "Settings"
                font_style: "H5"
                pos_hint: {"top": 0.75, "x": 0.01}

        MDBoxLayout:
            orientation: "horizontal"
            padding: [10]
            spacing: 10

            MDTextField:
                id: datafolderpath
                hint_text:"Data folder path"
                pos_hint: {"bottom": 0.35}

            MDRaisedButton:
                text: "Set"
                font_style: "Button"
                elevation: 5
                pos_hint: {"bottom": 0.35}
                on_press:
                    root.set_datafolder(datafolderpath.text) if datafolderpath.text != "" else None
                    datafolderpath.text = ""

            MDRectangleFlatButton:
                text: "Reset"
                font_style: "Button"
                elevation: 5
                pos_hint: {"bottom": 0.35}
                on_press: root.reset_datafolder(app.datafolder_default)
                # on_press: folderlabel.text = app.globalstring

        MDLabel:
            id: datafolderlabel
            text: ""
            halign: "center"

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
                font_style: "Button"
                elevation: 5
                pos_hint: {"top": 0.75}
                on_press:
                    root.set_exportfolder(exportfolderpath.text) if exportfolderpath.text != "" else None
                    exportfolderpath.text = ""

            MDRectangleFlatButton:
                text: "Reset"
                font_style: "Button"
                elevation: 5
                pos_hint: {"top": 0.75}
                on_press: root.reset_exportfolder(app.exportfolder_default)

        MDLabel:
            id: exportfolderlabel
            text: ""
            halign: "center"


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
                icon: "cog"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "settings"


RootScreen:

    MDToolbar:
        id: toolbar
        pos_hint: {"top": 1}
        elevation: 10
        title: "Navigation"
        left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]


    MDNavigationLayout:

        ScreenManager:
            id: screen_manager

            HomeScreen:

            SingleDayScreen:

            MultiDayScreen:

            SettingsScreen:


        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                id: content_drawer
                screen_manager: screen_manager
                nav_drawer: nav_drawer



'''
