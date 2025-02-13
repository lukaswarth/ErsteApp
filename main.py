from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.lang import Builder
import sqlite3


class MyGridLayout(GridLayout):
    values = ListProperty()
    
class Cocktail:
    def __init__(self):
        conn = sqlite3.connect("cocktail.db")
        c = conn.cursor()
        c.execute('CREATE TABLE if not exists cocktails(cocktailName text, zutaten text);')
        conn.commit()
        conn.close()
        
    def getAlleCocktails(self):
        conn = sqlite3.connect('cocktail.db')
        c = conn.cursor()
        c.execute('SELECT cocktailName FROM cocktails;')
        records = c.fetchall()
        cocktails = []
        for record in records:
            cocktails.append(record[0])
        conn.close()
        return cocktails
    
    def getZutaten(self,cocktail):
        conn = sqlite3.connect('cocktail.db')
        c = conn.cursor()
        statement = "SELECT zutaten FROM cocktails where cocktailName = '" + cocktail + "';"
        c.execute(statement)
        records = c.fetchall()
        zutaten = ['keine Zutatenliste vorhanden']
        if len(records) > 0:
            zutaten =  records[0][0].split(";")
        conn.close()
        return zutaten
    
class CocktailApp(App):
    def build(self):
        self.title = 'Cocktail-App'
        self.ce = Cocktail()
        return Builder.load_file("main.kv")
    
    def on_start(self):
        self.root.ids.spinner.values = self.ce.getAlleCocktails()
    
    def callback(self,instance):
        cocktail = self.root.ids.spinner.text
        zutatenListe = 'gefundene Zutaten:\n' + '\n'.join(self.ce.getZutaten(cocktail))
        
        self.root.ids.label.text = zutatenListe     

        
if __name__ == '__main__':
    CocktailApp().run()