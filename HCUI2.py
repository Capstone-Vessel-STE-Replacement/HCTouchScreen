from kivymd.app import MDApp  
from kivymd.uix.progressbar import MDProgressBar 

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup  
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from datetime import datetime
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import requests
import subprocess
from pymavlink import mavutil
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDFlatButton
class TouchScreen(FloatLayout):
    def __init__(self, **kwargs): 
        super(TouchScreen, self).__init__(**kwargs)
        # self.info_popup = InfoPopup()
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#1F448C'))
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        #Clock.schedule_interval(self.update_time, 1)  # Schedule time updates

   # def update_time(self, *args):
       # self.ids.time_label.text = datetime.now().strftime('%H:%M')
    
    def on_size(self, *args):
        self.rect.size = self.size
    
    def on_pos(self, *args):
        self.rect.pos = self.pos
    
    def toggle_info_popup(self):
        if self.info_popup.is_open:
            self.info_popup.dismiss()
        else:
            self.info_popup.open()
            self.info_popup.is_open = True

    def activate_active_mode(self):
        print("hello active")

    def activate_passive_mode(self):
        print("helllo passive")


    def activate_standby_mode(self):
        print("helllo standby")

    def update_operational_status(self, mode):
        self.ids.operating_mode_label.text = f"MODE: {mode.upper()}"
    
    def shutdown_system(self):
        try:
            subprocess.call(['sudo', 'shutdown', '-h', 'now'])
        except Exception as e:
            print(f"Error shutting down: {e}")

class HCUIApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        # Create an instance of the TouchScreen class
        screen = TouchScreen()
        # Add the MDFlatButton to the TouchScreen layout
        button = MDFlatButton(text='Hello, KivyMD!', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        screen.add_widget(button)
        return screen

if __name__ == '__main__':
    HCUIApp().run()
