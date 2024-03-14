from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton

class TestMDApp(MDApp):
    def build(self):
        return MDFlatButton(text='Hello, KivyMD!', pos_hint={'center_x': 0.5, 'center_y': 0.5})

if __name__ == '__main__':
    TestMDApp().run()
