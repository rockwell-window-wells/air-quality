import kivy
kivy.require('2.0.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label


class TestApp(App):

    def build(self):
        return Label(text='Hello world')


if __name__ == '__main__':
    TestApp().run()
