from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.popup import Popup 
from kivy.uix.label import Label
#imports

class InfoPopup(Popup):
    pass

class TouchScreen(BoxLayout):
    def __init__(self, **kwargs): 
        super(TouchScreen, self).__init__(**kwargs)
        self.info_popup = InfoPopup()

    def toggle_info_popup(self):
        if self.info_popup.parent:
            self.info_popup.dismiss()
        else:
            self.info_popup.open()

class HCUIApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#1F448C')
        return TouchScreen()

if __name__ == '__main__':
    HCUIApp().run()
