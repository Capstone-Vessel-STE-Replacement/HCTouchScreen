from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivy.uix.floatlayout import FloatLayout  # Import FloatLayout
from kivy.graphics import Color
from kivy.utils import get_color_from_hex

class TouchScreen(FloatLayout):  # Change to FloatLayout
    def __init__(self, **kwargs):
        super(TouchScreen, self).__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#1F448C'))

class TestMDApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        # Create an instance of the TouchScreen class
        screen = TouchScreen()
        # Add the MDFlatButton to the TouchScreen layout
        button = MDFlatButton(text='Hello, KivyMD!', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        screen.add_widget(button)
        return screen

if __name__ == '__main__':
    TestMDApp().run()
