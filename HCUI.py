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

class ActivationProgressBar(BoxLayout): # progress bar uses kivymd for styling
    def __init__(self, **kwargs): #setup the progress bar and the label
        super(ActivationProgressBar, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = '1000dp'  

        self.progress_bar = MDProgressBar(max=3, value=0, size_hint_x=.5) #initialize the progress bar
        self.progress_bar.size_hint_y = None
        self.progress_bar.height = dp(36)  # Set the height here

        self.add_widget(self.progress_bar) #seconds to activate label
        self.timer_label = Label(text='3', size_hint_x=0.1)
        self.timer_label.size_hint_y = None
        self.add_widget(self.timer_label)

    def start_countdown(self): # Start the countdown
        self.progress_bar.value = 0
        self.timer_label.text = '3'
        Clock.schedule_interval(self.update_progress, 0.1)

    def update_progress(self, dt): #Update the progress bar and the label
        if self.progress_bar.value >= self.progress_bar.max:
            Clock.unschedule(self.update_progress)
            return False
        self.progress_bar.value += dt
        remaining_time = 3 - int(self.progress_bar.value)
        self.timer_label.text = str(max(0, remaining_time))
        if remaining_time <= 0:
            self.timer_label.text = 'Button Activated'

    def reset_progress(self): #When the button is released, reset the progress bar
        Clock.unschedule(self.update_progress)
        self.progress_bar.value = 0
        self.timer_label.text = '3' 

        
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

    def on_size(self, *args): # Update the background rectangle and border when the size changes
        self.bg_rect.size = self.size
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 15)

    def on_pos(self, *args): # Update the background rectangle and border when the position changes
        self.bg_rect.pos = self.pos
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 15)

    def on_press(self): # When the button is pressed
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.background_down_color) # Change the color to the pressed state
            RoundedRectangle(size=self.size, pos=self.pos, radius=[15])
        activation_progress = MDApp.get_running_app().root.ids.activation_progress
        activation_progress.start_countdown() # Start the countdown
        self._trigger = Clock.schedule_once(self.activate_button, 3) # Schedule the activation after 3 seconds

    def on_release(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.background_normal_color)
            RoundedRectangle(size=self.size, pos=self.pos, radius=[15])
        activation_progress = MDApp.get_running_app().root.ids.activation_progress
        activation_progress.reset_progress()
        self.cancel_activation()

    def activate_button(self, dt):
        print("Button activated")

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
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#1F448C'))
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        Clock.schedule_interval(self.update_time, 1)  # Schedule time updates

    def update_time(self, *args):
        self.ids.time_label.text = datetime.now().strftime('%H:%M')

    
    def on_size(self, *args):
        self.rect.size = self.size
    
    def on_pos(self, *args):
        self.rect.pos = self.pos

class HCUIApp(MDApp): 
    def build(self):

        self.theme_cls.primary_palette = "Blue"

        return TouchScreen()

if __name__ == '__main__':
    HCUIApp().run()