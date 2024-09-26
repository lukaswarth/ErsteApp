from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder 
from random import *


class MyGridLayout(GridLayout):
    def button_neu(self):
        self.ids.label2.text = str(randint(1, 100))
        self.ids.label3.text = str(randint(1, 100))
        self.ids.label1.text = "Rechenart?"
        
    def button_plus(self):
        self.e = int(self.ids.label2.text) + int(self.ids.label3.text)
        self.ids.label1.text = str(self.e)
       
    def button_minus(self):
        self.e = int(self.ids.label2.text) - int(self.ids.label3.text)
        self.ids.label1.text = str(self.e)
       
    def button_mal(self):
        self.e = int(self.ids.label2.text) * int(self.ids.label3.text)
        self.ids.label1.text = str(self.e)
       
    def button_geteilt(self):
        self.e = int(self.ids.label2.text) / int(self.ids.label3.text)
        self.ids.label1.text = str(self.e)
       
      
class MainApp(App):
    def build(self):
        return Builder.load_file("main.kv")

if __name__ == "__main__":
    MainApp().run()