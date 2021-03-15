import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen

class KeyboardA(VKeyboard):
    def place(self):
        self.center_x = Window.center_x
        self.top = 0
        Animation(y=100, t='out_elastic', d=.4).start(self)

class KeyboardB(VKeyboard):
     def place(self):
        self.opacity = 0
        Animation(opacity=1).start(self)

class MyApp(App):
     def build(self):
         sm = ScreenManger()
         sm.add_widget(Screen(name='a'))
         sm.add_widget(Screen(name='b'))
         return sm

     def get_keyboard(self, **kwargs):
         if self.root.current == 'a':
             kb = KeyboardA(**kwargs)

         else:
             kb = KeyboardB(**kwargs)

         kb.place()
         return kb

Window.set_vkeyboard_class(MyApp.get_keyboard)