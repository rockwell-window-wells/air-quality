KV = '''
<HomeScreen>:
    name: "homescreen"
    id: home_screen

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
                        on_release: root.translate_en()

                AnchorLayout:
                    anchor_x: "center"
                    anchor_y: "center"

                    MDRaisedButton:
                        text: "Espa\u00F1ol"
                        font_style: "Button"
                        elevation: 5
                        pos_hint: {"top": 1, "right": 1.0}
                        on_release: root.translate_esp()


<AnalysisScreen>:
    name: "analysisscreen"
    id: analysis_screen
    # singleday_status: singleday_status
    plotsingle: plotsingle
    annotatevalues: annotatevalues
    annotatelines: annotatelines
    employeename: employeename
    analysistitle: analysistitle

    MDGridLayout:
        cols: 2
        padding: 10
        spacing: 10

        MDGridLayout:
            # orientation: "vertical"
            rows: 9
            spacing: 10
            padding: 10
            # md_bg_color: app.theme_cls.accent_color
            size_hint: (0.25, 1)

            MDFloatLayout:

                MDLabel:
                    id: analysistitle
                    text: app.analysis_title
                    font_style: "H5"
                    pos_hint: {"top": 0.6, "x": 0.01}


            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: refreshdata_single
                    text: app.refresh_data_label
                    font_style: "Button"
                    # pos_hint: {"top": 0.5, "right": 0.5}
                    on_release:
                        root.refreshdata_btn(app.datafolder)

            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: choosedate_single
                    text: app.single_day_label
                    font_style: "Button"
                    pos_hint: {"top": 0.5, "right": 0.5}
                    elevation: 5
                    on_release: root.show_single_date_picker()

            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: choosedate_single
                    text: app.multi_day_label
                    font_style: "Button"
                    pos_hint: {"top": 0.5, "right": 0.5}
                    elevation: 5
                    on_release: root.show_multi_date_picker()

            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: timerange_single
                    text: app.time_range_label
                    font_style: "Button"
                    pos_hint: {"top": 0.5, "right": 0.5}
                    elevation: 5
                    on_release: root.show_time_dialog()

            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: calculate
                    text: app.calculate_label
                    font_style: "Button"
                    md_bg_color: app.theme_cls.accent_color
                    pos_hint: {"top": 0.5, "right": 0.5}
                    elevation: 5
                    on_release:
                        root.calculate(root.annotatevalues.active, root.annotatelines.active, app.datafolder)

            AnchorLayout:
                anchor_x: "left"
                anchor_y: "center"

                MDRaisedButton:
                    id: export_single
                    text: app.export_label
                    font_style: "Button"
                    md_bg_color: app.theme_cls.accent_color
                    pos_hint: {"top": 0.5, "right": 0.5}
                    elevation: 5
                    on_release:
                        root.export(app.exportfolder, root.img_src, employeename.text)


            MDBoxLayout:
                orientation: "horizontal"

                CheckBox:
                    id: annotatevalues
                    color: [0.01, 1, 0.01, 1]
                    active: True

                MDLabel:
                    text: app.annotate_vals_label

            MDBoxLayout:
                orientation: "horizontal"

                CheckBox:
                    id: annotatelines
                    color: [0.01, 1, 0.01, 1]
                    active: True

                MDLabel:
                    text: app.annotate_lines_label

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
                    hint_text: app.employee_hint_label
                    pos_hint: {"top": 1}

                MDTextField:


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
                text: app.settings_title
                font_style: "H5"
                pos_hint: {"top": 0.75, "x": 0.01}

        MDBoxLayout:
            orientation: "horizontal"
            padding: [10]
            spacing: 10

            MDTextField:
                id: datafolderpath
                hint_text: app.data_folder_label
                pos_hint: {"bottom": 0.35}

            MDRaisedButton:
                text: app.set_btn_label
                font_style: "Button"
                elevation: 5
                pos_hint: {"bottom": 0.35}
                on_press:
                    root.set_datafolder(datafolderpath.text) if datafolderpath.text != "" else None
                    datafolderpath.text = ""

            MDRectangleFlatButton:
                text: app.reset_btn_label
                font_style: "Button"
                elevation: 5
                pos_hint: {"bottom": 0.35}
                on_press: root.reset_datafolder()
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
                hint_text: app.export_folder_label
                pos_hint: {"top": 0.75}

            MDRaisedButton:
                text: app.set_btn_label
                font_style: "Button"
                elevation: 5
                pos_hint: {"top": 0.75}
                on_press:
                    root.set_exportfolder(exportfolderpath.text) if exportfolderpath.text != "" else None
                    exportfolderpath.text = ""

            MDRectangleFlatButton:
                text: app.reset_btn_label
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
                text: app.home_title
                icon: "home"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "homescreen"

            ItemDrawer:
                text: app.analysis_title
                icon: "chart-line"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "analysisscreen"

            ItemDrawer:
                text: app.settings_title
                icon: "cog"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "settings"


RootScreen:
    id: root_screen

    MDToolbar:
        id: toolbar
        pos_hint: {"top": 1}
        elevation: 10
        title: app.navigation_title
        left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]


    MDNavigationLayout:
        id: navigation_layout

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
