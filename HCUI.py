from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.popup import Popup 
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, RoundedRectangle

class RoundedButton(ButtonBehavior, Label):
    background_normal_color = get_color_from_hex('#1F448C')
    background_down_color = get_color_from_hex('#3F668C')  # A slightly different color for the pressed state
    border_color = get_color_from_hex('#FFFFFF')  # Set the border color here

    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self._trigger = None
        with self.canvas.before:
            Color(rgba=self.background_normal_color)
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[15])
        with self.canvas.after:
            Color(rgba=self.border_color)
            self.border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 15), width=1.5)

    def on_size(self, *args):
        self.bg_rect.size = self.size
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 15)

    def on_pos(self, *args):
        self.bg_rect.pos = self.pos
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 15)

    def on_press(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.background_down_color)
            RoundedRectangle(size=self.size, pos=self.pos, radius=[15])

    def on_release(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.background_normal_color)
            RoundedRectangle(size=self.size, pos=self.pos, radius=[15])
        self.cancel_activation()

    def activate_button(self, dt):
        # Add the code here that should be executed after the button is held for 4 seconds
        print("Button activated")  # Example action

    def cancel_activation(self):
        if self._trigger:
            Clock.unschedule(self._trigger)
            self._trigger = None


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
