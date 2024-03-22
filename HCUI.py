from enum import auto
from kivymd.app import MDApp  
from kivymd.uix.progressbar import MDProgressBar 
from kivymd.uix.label import MDIcon
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
from kivy.properties import BooleanProperty, StringProperty
import requests
import subprocess
from kivy.uix.floatlayout import FloatLayout

import requests
import subprocess
import STEdata2

class ActivationProgressBar(BoxLayout):
    requested_operation = None

    def __init__(self, **kwargs):
        super(ActivationProgressBar, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = '100dp'

        self.progress_bar = MDProgressBar(max=2, value=0, size_hint_x=3.5)
        self.progress_bar.size_hint_y = None
        self.progress_bar.height = dp(50)

        self.add_widget(self.progress_bar)

        # Create a container for either the timer label or the completion icon
        self.label_or_icon_container = FloatLayout(size_hint=(0.5, 1.15))
        self.add_widget(self.label_or_icon_container)

        # Initially, we display the timer label
        self.timer_label = Label(text='2', size_hint=(None, None), size=(dp(48), dp(48)), halign='center', bold=True, font_size=dp(26))
        self.timer_label.pos_hint = {'center_x': 0.5, 'center_y': 0.23}
        self.label_or_icon_container.add_widget(self.timer_label)

    def start_countdown(self): # Start the countdown
        self.progress_bar.value = 0
        self.timer_label.text = '2'
        Clock.schedule_interval(self.update_progress, 0.1)

    def update_progress(self, dt):
        if self.progress_bar.value >= self.progress_bar.max:
            Clock.unschedule(self.update_progress)
            # Remove the timer label and add a checkmark icon
            self.label_or_icon_container.clear_widgets()
            self.add_completion_icon()
            # Perform the requested operation upon progress completion
            if self.requested_operation:
                self.perform_requested_operation()
            return False

        self.progress_bar.value += dt
        remaining_time = 2 - int(self.progress_bar.value)
        self.timer_label.text = str(max(0, remaining_time))

    def perform_requested_operation(self):
        # Assuming the operation is stored as a callable
        if callable(self.requested_operation):
            self.requested_operation()
        # Reset the requested operation to None
        self.requested_operation = None
    def add_completion_icon(self):
        completion_icon = MDIcon(icon="check", pos_hint={'center_x': 0.5, 'center_y': 0.2}, font_size=dp(48))
        self.label_or_icon_container.add_widget(completion_icon)

    def reset_progress(self):
        Clock.unschedule(self.update_progress)
        self.progress_bar.value = 0
        # Clear any icons and re-add the timer label for the next countdown
        self.label_or_icon_container.clear_widgets()
        self.label_or_icon_container.add_widget(self.timer_label)
        self.timer_label.text = '2'

    def reset_progress_and_operation(self):
        self.reset_progress()  # Assuming this resets the progress bar visually
        self.requested_operation = None  # Clear any previously set operation
    def set_requested_operation(self, operation):
        self.requested_operation = operation
    def cancel_progress_and_operation_if_incomplete(self):
        if self.progress_bar.value < self.progress_bar.max:
            self.reset_progress_and_operation()




        
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

    def on_press(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.background_down_color)
            RoundedRectangle(size=self.size, pos=self.pos, radius=[15])
    
        if self.text in ['ACTIVE', 'PASSIVE', 'STANDBY', 'POWER']:
            activation_progress = MDApp.get_running_app().root.ids.activation_progress
        # Start the countdown directly
            activation_progress.set_requested_operation(self.get_operation())
            activation_progress.start_countdown()

    def on_release(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.background_normal_color)
            RoundedRectangle(size=self.size, pos=self.pos, radius=[15])
    
        # Cancel the progress and any operation if the button is released early
        activation_progress = MDApp.get_running_app().root.ids.activation_progress
        activation_progress.cancel_progress_and_operation_if_incomplete()


    def cancel_activation(self):
        if self._trigger:
            Clock.unschedule(self._trigger)
            self._trigger = None
    def get_operation(self):
        if self.text == 'POWER':
            return lambda: getattr(MDApp.get_running_app().root, 'shutdown_system')()
        else:
            return lambda: getattr(MDApp.get_running_app().root, f'activate_{self.text.lower()}_mode')()


class TouchScreen(BoxLayout):
    #init ready checks
    mode_text = StringProperty('STANDBY')
    sd_card_ready = BooleanProperty(False)
    rf_transmitter_ready = BooleanProperty(False)
    system_controller_ready = BooleanProperty(False)
    downlink_status_ready = BooleanProperty(False)

    def __init__(self, **kwargs): 
        super(TouchScreen, self).__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#1F448C'))
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        Clock.schedule_interval(self.update_time, 1)  # Schedule time updates
        Clock.schedule_interval(self.update_status, 1)

    def update_time(self, *args):
        self.ids.time_label.text = datetime.now().strftime('%H:%M')
    def update_status(self, *args):
        # Update properties with the result of the readiness checks
        self.sd_card_ready = STEdata2.storage_ready()
        self.rf_transmitter_ready = STEdata2.rf_transmitter()
        self.system_controller_ready = STEdata2.system_controller()
        self.downlink_status_ready = STEdata2.downlink_status()
    
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
        activation_progress = MDApp.get_running_app().root.ids.activation_progress
        # Check if the progress bar is full
        if activation_progress.progress_bar.value >= activation_progress.progress_bar.max:
            STEdata2.change_mode(STEdata2.ACTIVE)
            self.mode_text = 'ACTIVE'
            activation_progress.reset_progress() 

    def activate_passive_mode(self):
        activation_progress = MDApp.get_running_app().root.ids.activation_progress
        if activation_progress.progress_bar.value >= activation_progress.progress_bar.max:
            STEdata2.change_mode(STEdata2.PASSIVE)
            self.mode_text = 'PASSIVE'
            activation_progress.reset_progress()

    def activate_standby_mode(self):
        activation_progress = MDApp.get_running_app().root.ids.activation_progress
        if activation_progress.progress_bar.value >= activation_progress.progress_bar.max:
            STEdata2.change_mode(STEdata2.STANDBY)
            self.mode_text = 'STANDBY'
            activation_progress.reset_progress()

    def update_operational_status(self, mode):
        self.ids.operaradio_ting_mode_label.text = f"MODE: {mode.upper()}"
    
    def shutdown_system(self):
        try:
            subprocess.call(['sudo', 'shutdown', '-h', 'now'])
        except Exception as e:
            print(f"Error shutting down: {e}")


class HCUIApp(MDApp): 
    def build(self):

        self.theme_cls.primary_palette = "Blue"
        Window.fullscreen = 'auto'

        return TouchScreen()

