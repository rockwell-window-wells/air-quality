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

<AnalysisScreen>:
    name: "analysisscreen"
    # singleday_status: singleday_status
    plotsingle: plotsingle
    annotatecheck: annotatecheck
    employeename: employeename

    MDGridLayout:
        cols: 2
        padding: 10
        spacing: 10

        MDGridLayout:
            # orientation: "vertical"
            rows: 8
            spacing: 10
            padding: 10
            # md_bg_color: app.theme_cls.accent_color
            size_hint: (0.25, 1)

            MDFloatLayout:

                MDLabel:
                    id: singledaytitle
                    text: "Analysis"
                    font_style: "H5"
                    pos_hint: {"top": 0.7, "x": 0.01}


            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: refreshdata_single
                    text: "Refresh Data"
                    font_style: "Button"
                    # pos_hint: {"top": 0.5, "right": 0.5}
                    on_release:
                        root.refreshdata_btn(app.datafolder)

            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: choosedate_single
                    text: "Single Day"
                    font_style: "Button"
                    pos_hint: {"top": 0.5, "right": 0.5}
                    elevation: 5
                    on_release: root.show_single_date_picker()

            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: choosedate_single
                    text: "Multiple Dates"
                    font_style: "Button"
                    pos_hint: {"top": 0.5, "right": 0.5}
                    elevation: 5
                    on_release: root.show_multi_date_picker()

            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: timerange_single
                    text: "Time Range"
                    font_style: "Button"
                    pos_hint: {"top": 0.5, "right": 0.5}
                    elevation: 5
                    on_release: root.show_time_dialog()

            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: calculate
                    text: "Calculate"
                    font_style: "Button"
                    md_bg_color: app.theme_cls.accent_color
                    pos_hint: {"top": 0.5, "right": 0.5}
                    elevation: 5
                    on_release:
                        root.calculate(root.annotatecheck.active, app.directory)

            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: export_single
                    text: "Export"
                    font_style: "Button"
                    md_bg_color: app.theme_cls.accent_color
                    pos_hint: {"top": 0.5, "right": 0.5}
                    elevation: 5
                    on_release:
                        root.export(app.export_directory, root.img_src, employeename.text)


            MDBoxLayout:
                orientation: "horizontal"

                CheckBox:
                    id: annotatecheck
                    color: [0.01, 1, 0.01, 1]
                    active: True

                MDLabel:
                    text: "Annotate Chart"

        MDFloatLayout:

            MDBoxLayout:
                pos_hint: {"top": 0.9, "right": 1}
                orientation: "vertical"
                spacing: 0

                MDCard:
                    id: plotsingle
                    size_hint_y: 4.5
                    pos_hint: {"top": 1, "x": 0.0}
                    # md_bg_color: app.theme_cls.accent_color

                    # Put the chart here
                    FitImage:
                        id: graphsingle
                        source: root.img_src

                MDTextField:
                    id: employeename
                    hint_text:"Employee wearing PAC 8000"
                    pos_hint: {"top": 1}

                MDTextField:

# <MultiDayScreen>:
#     name: "multidaystyrene"
#
#     MDGridLayout:
#         cols: 2
#         padding: 10
#         spacing: 10
#
#         MDGridLayout:
#             # orientation: "vertical"
#             rows: 7
#             spacing: 10
#             padding: 10
#             size_hint: (0.25, 1)
#
#             MDFloatLayout:
#
#                 MDLabel:
#                     id: multidaytitle
#                     text: "Multi-Day"
#                     font_style: "H5"
#                     pos_hint: {"top": 0.75, "x": 0.01}
#
#             AnchorLayout:
#                 anchor_x: "left"
#                 anchor_y: "center"
#
#                 MDRaisedButton:
#                     id: refreshdata_single
#                     text: "Refresh Data"
#                     font_style: "Button"
#                     on_release:
#                         root.refreshdata_multi(app.datafolder)
#
#             AnchorLayout:
#                 anchor_x: "left"
#                 anchor_y: "center"
#
#                 MDRaisedButton:
#                     id: choosedate_single
#                     text: "Date Range"
#                     font_style: "Button"
#                     pos_hint: {"top": 0.5, "right": 0.5}
#                     elevation: 5
#
#             AnchorLayout:
#                 anchor_x: "left"
#                 anchor_y: "center"
#
#                 MDRaisedButton:
#                     id: timerange_single
#                     text: "Time Range"
#                     font_style: "Button"
#                     pos_hint: {"top": 0.5, "right": 0.5}
#                     elevation: 5
#
#             AnchorLayout:
#                 anchor_x: "left"
#                 anchor_y: "center"
#
#                 MDRaisedButton:
#                     id: calculate_single
#                     text: "Calculate"
#                     font_style: "Button"
#                     md_bg_color: app.theme_cls.accent_color
#                     pos_hint: {"top": 0.5, "right": 0.5}
#                     elevation: 5
#
#             AnchorLayout:
#                 anchor_x: "left"
#                 anchor_y: "center"
#
#                 MDRaisedButton:
#                     id: export_single
#                     text: "Export"
#                     font_style: "Button"
#                     md_bg_color: app.theme_cls.accent_color
#                     pos_hint: {"top": 0.5, "right": 0.5}
#                     elevation: 5
#
#             AnchorLayout:
#                 anchor_x: "left"
#                 anchor_y: "center"
#
#                 MDBoxLayout:
#                     orientation: "horizontal"
#
#                     CheckBox:
#                         color: [0.01, 1, 0.01, 1]
#                         active: True
#
#                     MDLabel:
#                         text: "Annotate Chart"
#
#
#         MDFloatLayout:
#
#             MDBoxLayout:
#                 pos_hint: {"top": 0.9, "right": 1}
#                 orientation: "vertical"
#                 spacing: 10
#
#                 MDCard:
#                     size_hint_y: 6
#                     # height: "200dp"
#                     pos_hint: {"top": 1, "x": 0.0}
#                     md_bg_color: app.theme_cls.accent_color
#
#                     # Put the chart here
#                     FitImage:
#                         id: plotmulti
#                         source: 'assets/test.png'
#
#                 # MDLabel:
#                 #     id: multi_datalabel
#                 #     text: "TWA: \\nPeak: \\nName: \\nDates: \\nShift: "
#
#                 MDLabel:


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
    # on_release: self.parent.set_color_item(self)

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
                text: "Analysis"
                icon: "chart-line"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "analysisscreen"

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

            AnalysisScreen:

            SettingsScreen:


        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                id: content_drawer
                screen_manager: screen_manager
                nav_drawer: nav_drawer



'''
