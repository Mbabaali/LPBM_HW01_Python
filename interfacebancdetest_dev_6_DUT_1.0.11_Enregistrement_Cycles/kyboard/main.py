# Program to Show how to use textinput (UX widget) in kivy  
  
# import kivy module     
import kivy   
from kivy.app import App  
from kivy.uix.label import Label  
from kivy.uix.floatlayout import FloatLayout  
from kivy.uix.scatter import Scatter 
from kivy.uix.textinput import TextInput 
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.vkeyboard import VKeyboard 
from kivy.config import Config

Config.set('kivy', 'keyboard_mode', 'systemandmulti')
  
# Create the App class 
class TutorialApp(App): 
      
    def build(self): 
  
        b = BoxLayout(orientation ='vertical') 
  
        # Adding the text input 
        t = TextInput(font_size = 50, 
                      size_hint_y = None, 
                      height = 100) 
          
        f = FloatLayout() 
  
        # By this you are abel to move the 
        # Text on the screen to anywhere you want 
        s = Scatter() 
  
        l = Label(text ="Hello !", 
                  font_size = 50) 
  
        f.add_widget(s) 
        s.add_widget(l) 
  
        b.add_widget(t) 
        b.add_widget(f) 
  
        # Binding it with the label 
        t.bind(text = l.setter('text')) 
  
          
        return b 
  
# Run the App 
if __name__ == "__main__": 
    TutorialApp().run() 