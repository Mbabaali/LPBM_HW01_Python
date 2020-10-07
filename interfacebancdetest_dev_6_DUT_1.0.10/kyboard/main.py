# Program to Show how to use textinput  
# (UX widget) in kivy using .kv file 
  
# import kivy module     
import kivy   
       
# base Class of your App inherits from the App class.     
# app:always refers to the instance of your application    
from kivy.app import App  
     
# this restrict the kivy version i.e   
# below this kivy version you cannot   
# use the app or software   
kivy.require('1.9.0') 
  
# Widgets are elements 
# of a graphical user interface 
# that form part of the User Experience. 
from kivy.uix.widget import Widget 
  
# The TextInput widget provides a 
# box for editable plain text 
from kivy.uix.textinput import TextInput 
  
# This layout allows you to set relative coordinates for children.  
from kivy.uix.relativelayout import RelativeLayout 

# VKeyboard is an onscreen keyboard 
# for Kivy. Its operation is intended 
# to be transparent to the user.  
from kivy.uix.vkeyboard import VKeyboard 
  
# Create the widget class 
class textinp(Widget): 
    pass

class Test(VKeyboard): 
    player = VKeyboard() 

# Create the App class 
class VkeyboardApp(App): 
    def build(self): 
        return Test() 
  
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
    VkeyboardApp().run()