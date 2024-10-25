from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from random import *

class MyGridLayout(GridLayout):
    def button_m(self):
        self.ids.label2.text = str(int(self.ids.label2.text) - 1)
    
    def button_p(self):
        self.ids.label2.text = str(int(self.ids.label2.text) + 1)
    
    def button_ok(self):
        z = str(randint(1, 1000))
        r = int(self.ids.label2.text)
        d = int(z) - r
        
        if d < 0:
            d = str(d - 2 * d)
        else:
            d = str(d)
            
        if int(d) < 1:
            self.ids.labels2.text = str(int(self.ids.labels2.text) + 100)
        elif int(d) < 6:
            self.ids.labels2.text = str(int(self.ids.labels2.text) + 50)
        elif int(d) < 11:
            self.ids.labels2.text = str(int(self.ids.labels2.text) + 25)
        elif int(d) < 26:
            self.ids.labels2.text = str(int(self.ids.labels2.text) + 10)
        elif int(d) < 51:
            self.ids.labels2.text = str(int(self.ids.labels2.text) + 5)
        self.ids.label1.text = "Ich dachte an die Zahl " + z + ", damit lagst du um " + d + " daneben."
        
        if int(d) < int(self.ids.labelh2.text):
            self.ids.labelh2.text = d

    
    

class MainApp(App):
    def build(self):
        return Builder.load_file("main.kv")

if __name__ == "__main__":
    MainApp().run()
