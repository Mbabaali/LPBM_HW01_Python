# Program to Show how to use textinput  
# (UX widget) in kivy using .kv file 
  
# import kivy module     
import kivy   
       
# base Class of your App inherits from the App class.     
# app:always refers to the instance of your application    
from kivy.app import App  

from kivy.uix.vkeyboard import VKeyboard 
from kivy.uix.widget import Widget 
from kivy.uix.textinput import TextInput  
from kivy.uix.relativelayout import RelativeLayout 

keyboard = Window.request_keyboard(
    self._keyboard_close, self)
if keyboard.widget:
    vkeyboard = self._keyboard.widget
    vkeyboard.layout = 'numeric.json'
  
# Create the widget class 
class textinp(Widget): 
    pass
  
# Create the app class 
class MainApp(App): 
  
    # Building text input 
    def build(self): 
        return textinp() 
  
    # Arranging that what you write will be shown to you 
    # in IDLE 
    def process(self): 
        text = self.root.ids.input.text 
        print(text) 
  
# Run the App 
if __name__ == "__main__": 
    MainApp().run() 