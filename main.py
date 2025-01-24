from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.properties import ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from random import *
import random
import sqlite3


#L3 2.1 & L3 3.1, genug Vorbereitung auf KA


background_music = SoundLoader.load("Audios/background.wav")


def create_database1():
    conn = sqlite3.connect('kasino_game.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS game_data (
            id INTEGER PRIMARY KEY,
            geld TEXT DEFAULT "10000",
            schwer TEXT DEFAULT "1"
        )
    ''')
    c.execute('INSERT OR IGNORE INTO game_data (id, geld, schwer) VALUES (1, "10000", "1")')
    conn.commit()
    conn.close()
    
def create_database2():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS game_data (
            id INTEGER PRIMARY KEY,
            score TEXT DEFAULT "0",
            highscore TEXT DEFAULT "999"
        )
    ''')
    c.execute('INSERT OR IGNORE INTO game_data (id, score, highscore) VALUES (2, "0", "999")')
    conn.commit()
    conn.close()
    
def create_database3():
    conn = sqlite3.connect('win.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS game_data (
            id INTEGER PRIMARY KEY,
            win TEXT DEFAULT "0"
        )
    ''')
    c.execute('INSERT OR IGNORE INTO game_data (id, win) VALUES (3, "0")')
    conn.commit()
    conn.close()
    
def create_upgrades():
    conn = sqlite3.connect('upgrades.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS upgrade_access (
            upgrade_name TEXT PRIMARY KEY,
            is_paid INTEGER DEFAULT 0
        )
    ''')
    upgrades = [
        ("$_pro_klick", 1),
        ("$_pro_balken", 1),
        ("Autoclicker", 0),
        ("GameTwo", 0),
        ("GameFour", 0),
        ("GameSix", 0),
        ("GameEight", 0),
    ]
    c.executemany('INSERT OR IGNORE INTO upgrade_access (upgrade_name, is_paid) VALUES (?, ?)', upgrades)
    conn.commit()
    conn.close()

def create_game_access_table():
    conn = sqlite3.connect('kasino_game.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS game_access (
            game_name TEXT PRIMARY KEY,
            is_paid INTEGER DEFAULT 0
        )
    ''')
    games = [
        ("GameOne", 0),
        ("GameTwo", 0),
        ("GameThree", 0),
        ("GameFour", 0),
        ("GameFive", 0),
        ("GameSix", 0),
        ("GameSeven", 0),
        ("GameEight", 0),
        ("Upgrades", 0),
        ("Statistics", 0)
    ]
    c.executemany('INSERT OR IGNORE INTO game_access (game_name, is_paid) VALUES (?, ?)', games)
    conn.commit()
    conn.close()

def check_game_payment(game_name):
    conn = sqlite3.connect('kasino_game.db')
    c = conn.cursor()
    c.execute('SELECT is_paid FROM game_access WHERE game_name = ?', (game_name,))
    row = c.fetchone()
    conn.close()
    return bool(row[0]) if row else False

def mark_game_as_paid(game_name):
    conn = sqlite3.connect('kasino_game.db')
    c = conn.cursor()
    c.execute('UPDATE game_access SET is_paid = 1 WHERE game_name = ?', (game_name,))
    conn.commit()
    conn.close()

def load_game_data1():
    conn = sqlite3.connect('kasino_game.db')
    c = conn.cursor()
    c.execute('SELECT geld, schwer FROM game_data WHERE id = 1')
    row = c.fetchone()
    conn.close()
    return row if row else ("10000", "1")

def load_game_data2():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('SELECT score, highscore FROM game_data WHERE id = 2')
    row = c.fetchone()
    conn.close()
    return row if row else ("0", "999")

def load_game_data3():
    conn = sqlite3.connect('win.db')
    c = conn.cursor()
    c.execute('SELECT win FROM game_data WHERE id = 3')
    row = c.fetchone()
    conn.close()
    return row[0] if row else "0"

def load_upgrades(upgrade_name):
    conn = sqlite3.connect('upgrades.db')
    c = conn.cursor()
    c.execute('SELECT is_paid FROM upgrade_access WHERE upgrade_name = ?', (upgrade_name,))
    row = c.fetchone()
    conn.close()
    return bool(row[0]) if row else False

def save_game_data1(geld, schwer):
    conn = sqlite3.connect('kasino_game.db')
    c = conn.cursor()
    c.execute('''
        UPDATE game_data
        SET geld = ?, schwer = ?
        WHERE id = 1
    ''', (geld, schwer))
    conn.commit()
    conn.close()
    
def save_game_data2(score, highscore):
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('''
        UPDATE game_data
        SET score = ?, highscore = ?
        WHERE id = 2
    ''', (score, highscore))
    conn.commit()
    conn.close()

def save_game_data3(win):
    conn = sqlite3.connect('win.db')
    c = conn.cursor()
    c.execute('''
        UPDATE game_data
        SET win = ?
        WHERE id = 3
    ''', (win,))
    conn.commit()
    conn.close()
    
def save_upgrades(upgrade_name):
    conn = sqlite3.connect('upgrades.db')
    c = conn.cursor()
    c.execute('UPDATE upgrade_access SET is_paid = is_paid + 1 WHERE upgrade_name = ?', (upgrade_name,))
    conn.commit()
    conn.close()


class MyScreenManager(ScreenManager):
    shared_variable = StringProperty("10000")
    shared_variable2 = StringProperty("1")
    
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        geld, schwer = load_game_data1()
        self.win = int(load_game_data3())
        self.shared_variable = geld
        self.shared_variable2 = schwer
        self.bind(shared_variable = self.on_shared_variable_change)

    def transition_to(self, screen_name):
        previous_transition = self.transition
        self.transition = FadeTransition()
        self.current = screen_name
        self.transition = previous_transition
    
    def on_shared_variable_change(self, instance, value):
        if int(self.shared_variable) >= 1000000 * int(self.shared_variable2):
            if int(self.shared_variable2) < 5:
                content = BoxLayout(orientation="vertical", padding=10, spacing=10)
                message = Label(text="Du hast die maximale Geldmenge erreicht.\nDie Schwierigkeitsstufe wird erhöht!")
                close_button = Button(text="OK")
                content.add_widget(message)
                content.add_widget(close_button)
                popup = Popup(
                    title="Schwierigkeitsstufe wird erhöht",
                    content=content,
                    size_hint=(0.8, 0.4),
                    auto_dismiss=False
                )
                close_button.bind(on_press=popup.dismiss)
                popup.open()
                self.transition_to("Kasino")
                self.on_shared_variable2_change(instance, value)
                self.shared_variable = "10000"
                self.reset_game_access()
            else:
                if self.win == 0:
                    content = BoxLayout(orientation="vertical", padding=10, spacing=10)
                    message = Label(text="Viel Spaß beim Gambeln")
                    close_button = Button(text="OK")
                    content.add_widget(message)
                    content.add_widget(close_button)
                    popup = Popup(
                        title="Du hast es geschafft!",
                        content=content,
                        size_hint=(0.8, 0.4),
                        auto_dismiss=False
                    )
                    close_button.bind(on_press=popup.dismiss)
                    popup.open()
                    self.win += 1
                    save_game_data3(self.win)
                    
    def on_shared_variable2_change(self, instance, value):
        new_shared_variable2 = str(int(self.shared_variable2) + 1)
        self.shared_variable2 = new_shared_variable2
        save_game_data1(self.shared_variable, self.shared_variable2)
        
    def reset_game_access(self, exclude_games=None):
        if exclude_games is None:
            exclude_games = ["Upgrades", "Statistics"]
        
        conn = sqlite3.connect('kasino_game.db')
        c = conn.cursor()
        
        try:
            placeholders = ', '.join(['?'] * len(exclude_games))
            sql_query = f'UPDATE game_access SET is_paid = 0 WHERE game_name NOT IN ({placeholders})'
            c.execute(sql_query, exclude_games)
            conn.commit()
            print(f"Alle Einträge außer {exclude_games} wurden gelöscht.")
        except sqlite3.Error as e:
            print(f"Fehler beim Löschen der Einträge: {e}")
        finally:
            conn.close()

class Start(Screen):
    def on_enter(self):
        screen_width = Window.width
        screen_height = Window.height
        font_size = screen_width * 0.07
        self.ids.gruss.font_size = font_size
        self.start_text_animation()

    def start_text_animation(self):
        label = self.ids.gruss
        animation = Animation(opacity=0.5, duration=0.75) + \
                    Animation(opacity=1.5, duration=0.5)
        animation.repeat = True
        animation.start(label)

    def orange(self):
        self.ids.farbe.text = "Orange"
    
    def lila(self):
        self.ids.farbe.text = "Lila"
    
    def grün(self):
        self.ids.farbe.text = "Grün"
    
    def weiß(self):
        self.ids.farbe.text = "Weiß"
    
    def schwarz(self):
        self.ids.farbe.text = "Schwarz"
         

class Kasino(Screen):
    score_music = SoundLoader.load("Audios/score.mp3")
    
    def on_enter(self):
        score, highscore = load_game_data2()
        self.ids.labels2.text = score
        self.ids.labelh2.text = highscore
        self.ids.geld2.text = self.manager.shared_variable
        self.ids.schwer.text = self.manager.shared_variable2
        
    def button_m(self):
        self.ids.label2.text = str(int(self.ids.label2.text) - 1)
    
    def button_p(self):
        self.ids.label2.text = str(int(self.ids.label2.text) + 1)
    
    def button_ok(self):
        z = str(randint(1, 1000))
        r = int(self.ids.label2.text)
        d = int(z) - r
        
        if int(self.ids.geld2.text) - 1000 < 2000 * int(self.ids.schwer.text):
            if not check_game_payment("GameOne"):
                self.ids.button3.text = "Du musst dir erst GameOne kaufen!"
                self.ids.button3.disabled = True
        else:
            self.ids.button3.disabled = False

        if int(self.ids.geld2.text) - 500 < 0:
            self.ids.button3.text = "Du hast nicht genügend Geld!"
        else:
            if d < 0:
                d = str(d - 2 * d)
            else:
                d = str(d)
                        
            if int(d) < 1:
                self.ids.geld2.text = str(int(self.ids.geld2.text) + 50000 * int(self.ids.schwer.text))
                self.ids.labels2.text = str(int(self.ids.labels2.text) + 50000 * int(self.ids.schwer.text))
                self.score_music.play()
            elif int(d) < 6:
                self.ids.geld2.text = str(int(self.ids.geld2.text) + 10000 * int(self.ids.schwer.text))
                self.ids.labels2.text = str(int(self.ids.labels2.text) + 10000 * int(self.ids.schwer.text))
                self.score_music.play()
            elif int(d) < 11:
                self.ids.geld2.text = str(int(self.ids.geld2.text) + 1000 * int(self.ids.schwer.text))
                self.ids.labels2.text = str(int(self.ids.labels2.text) + 1000 * int(self.ids.schwer.text))
                self.score_music.play()
            elif int(d) < 26:
                self.ids.geld2.text = str(int(self.ids.geld2.text) + 500 * int(self.ids.schwer.text))
                self.ids.labels2.text = str(int(self.ids.labels2.text) + 500 * int(self.ids.schwer.text))
                self.score_music.play()
            elif int(d) < 51:
                self.ids.geld2.text = str(int(self.ids.geld2.text) + 100 * int(self.ids.schwer.text))
                self.ids.labels2.text = str(int(self.ids.labels2.text) + 100 * int(self.ids.schwer.text))
                self.score_music.play()
                            
            self.ids.label1.text = "Ich dachte an die Zahl " + z + ", damit lagst du um " + d + " daneben."
                    
            if int(d) < int(self.ids.labelh2.text):
                self.ids.labelh2.text = d
                            
            self.ids.geld2.text = str(int(self.ids.geld2.text) - 500)
            
        self.manager.shared_variable = self.ids.geld2.text
        save_game_data1(self.ids.geld2.text, self.ids.schwer.text)
        save_game_data2(self.ids.labels2.text, self.ids.labelh2.text)

class GameOne(Screen):
    left_music = SoundLoader.load("Audios/left.wav")
    
    def on_enter(self):
        self.ids.geld4.text = self.manager.shared_variable
        self.ids.schwer1.text = self.manager.shared_variable2
        self.ids.bar.max = 20 * int(self.ids.schwer1.text)
        self.pro_klick = load_upgrades("$_pro_klick")
        if not check_game_payment("GameOne"):
            self.show_payment_popup("GameOne")
        else:
            self.ids.geld4.text = self.manager.shared_variable
            self.ids.schwer1.text = self.manager.shared_variable2

    def show_payment_popup(self, game_name):
        content = BoxLayout(orientation = "vertical", padding = 10, spacing = 10)
        message = Label(text = "Du musst " + str(2000  * int(self.ids.schwer1.text)) + "$ bezahlen, um dieses Spiel zu starten.")
        pay_button = Button(text = "Bezahlen")
        close_button = Button(text = "Abbrechen")
        content.add_widget(message)
        content.add_widget(pay_button)
        content.add_widget(close_button)

        popup = Popup(
            title = "Zugriff kaufen",
            content = content,
            size_hint = (0.8, 0.4),
            auto_dismiss = False
        )

        def process_payment(instance):
            if int(self.manager.shared_variable) >= 2000 * int(self.ids.schwer1.text):
                self.manager.shared_variable = str(int(self.manager.shared_variable) - 2000 * int(self.ids.schwer1.text))
                save_game_data1(self.manager.shared_variable, self.manager.shared_variable2)
                mark_game_as_paid(game_name)
                print(f"Markiere Spiel '{game_name}' als bezahlt.")
                popup.dismiss()
                self.ids.geld4.text = self.manager.shared_variable
                self.ids.schwer1.text = self.manager.shared_variable2
            else:
                message.text = "Nicht genug Geld!"

        def cancel_payment(instance):
            popup.dismiss()
            self.manager.current = "Kasino"
            self.manager.transition.direction = "left"

        pay_button.bind(on_press = process_payment)
        close_button.bind(on_press = cancel_payment)
        popup.open()
        
    def button_s1(self):
        self.ids.bar.value = self.ids.bar.value + 1
        self.ids.geld4.text = str(int(self.ids.geld4.text) + 100000 * int(self.ids.schwer1.text) * self.pro_klick)
        if self.ids.bar.value == 20 * int(self.ids.schwer1.text):
            self.left_music.play()
            self.ids.bar.value = 0
            self.ids.geld4.text = str(int(self.ids.geld4.text) + round(50 * int(self.ids.schwer1.text)))
                
        self.manager.shared_variable = self.ids.geld4.text
        save_game_data1(self.ids.geld4.text, self.ids.schwer1.text)

class GameTwo(Screen):
    right_r_music = SoundLoader.load("Audios/right_right.wav")
    right_w_music = SoundLoader.load("Audios/right_wrong.mp3")
    
    def on_enter(self):
        self.ids.geld6.text = self.manager.shared_variable
        self.ids.schwer2.text = self.manager.shared_variable2
        if not check_game_payment("GameTwo"):
            self.show_payment_popup("GameTwo")
        else:
            self.ids.geld6.text = self.manager.shared_variable
            self.ids.schwer2.text = self.manager.shared_variable2

    def show_payment_popup(self, game_name):
        content = BoxLayout(orientation = "vertical", padding = 10, spacing = 10)
        message = Label(text = "Du musst " + str(5000 * int(self.ids.schwer2.text)) + "$ bezahlen, um dieses Spiel zu starten.")
        pay_button = Button(text = "Bezahlen")
        close_button = Button(text = "Abbrechen")
        content.add_widget(message)
        content.add_widget(pay_button)
        content.add_widget(close_button)

        popup = Popup(
            title = "Zugriff kaufen",
            content = content,
            size_hint = (0.8, 0.4),
            auto_dismiss = False
        )

        def process_payment(instance):
            if int(self.manager.shared_variable) >= 5000 * int(self.ids.schwer2.text):
                self.manager.shared_variable = str(int(self.manager.shared_variable) - 5000 * int(self.ids.schwer2.text))
                save_game_data1(self.manager.shared_variable, self.manager.shared_variable2)
                mark_game_as_paid(game_name)
                popup.dismiss()
                self.ids.geld6.text = self.manager.shared_variable
                self.ids.schwer2.text = self.manager.shared_variable2
            else:
                message.text = "Nicht genug Geld!"

        def cancel_payment(instance):
            popup.dismiss()
            self.manager.current = "Kasino"
            self.manager.transition.direction = "right"

        pay_button.bind(on_press = process_payment)
        close_button.bind(on_press = cancel_payment)
        popup.open()
        
    def start_timer1(self):
        Clock.unschedule(self.set_timer1)
        self.ids.timer1.value = 0
        self.ids.ergebnis1.text = ""
        Clock.schedule_interval(self.set_timer1, 0.1)
        self.ids.zahl1.text = str(randint(1, 100))
        self.ids.zahl2.text = str(randint(1, 100))
        
        
    def set_timer1(self, dt):
        self.ids.timer1.value += 1
        if self.ids.timer1.value == 60:
            if self.ids.ergebnis1.text == "":
                self.right_w_music.play()
                self.ids.ergebnis1.background_color = [0.8, 0, 0, 1]
                Clock.unschedule(self.set_timer1)
                self.ids.timer1.value = 0
            elif not self.ids.ergebnis1.text.isdigit():
                self.right_w_music.play()
                self.ids.ergebnis1.background_color = [0.8, 0, 0, 1]
                Clock.unschedule(self.set_timer1)
                self.ids.timer1.value = 0
            elif int(self.ids.ergebnis1.text) == int(self.ids.zahl1.text) + int(self.ids.zahl2.text):
                self.right_r_music.play()
                self.ids.ergebnis1.background_color = [0, 0.8, 0, 1]
                self.ids.geld6.text = str(int(self.ids.geld6.text) + round(5000 / int(self.ids.schwer2.text)))
                Clock.unschedule(self.set_timer1)
            else:
                self.right_w_music.play()
                self.ids.ergebnis1.background_color = [0.8, 0, 0, 1]
                Clock.unschedule(self.set_timer1)
                self.ids.timer1.value = 0
                
        self.manager.shared_variable = self.ids.geld6.text
        save_game_data1(self.ids.geld6.text, self.ids.schwer2.text)

class GameThree(Screen):
    left_music = SoundLoader.load("Audios/left.wav")
    
    def on_enter(self):
        self.ids.geld8.text = self.manager.shared_variable
        self.ids.schwer3.text = self.manager.shared_variable2
        if not check_game_payment("GameThree"):
            self.show_payment_popup("GameThree")
        else:
            self.ids.geld8.text = self.manager.shared_variable
            self.ids.schwer3.text = self.manager.shared_variable2

    def show_payment_popup(self, game_name):
        content = BoxLayout(orientation = "vertical", padding = 10, spacing = 10)
        message = Label(text = "Du musst " + str(15000 * int(self.ids.schwer3.text)) + "$ bezahlen, um dieses Spiel zu starten.")
        pay_button = Button(text = "Bezahlen")
        close_button = Button(text = "Abbrechen")
        content.add_widget(message)
        content.add_widget(pay_button)
        content.add_widget(close_button)

        popup = Popup(
            title = "Zugriff kaufen",
            content = content,
            size_hint = (0.8, 0.4),
            auto_dismiss = False
        )

        def process_payment(instance):
            if int(self.manager.shared_variable) >= 10000 * int(self.ids.schwer3.text):
                self.manager.shared_variable = str(int(self.manager.shared_variable) - 10000 * int(self.ids.schwer3.text))
                save_game_data1(self.manager.shared_variable, self.manager.shared_variable2)
                mark_game_as_paid(game_name)
                popup.dismiss()
                self.ids.geld8.text = self.manager.shared_variable
                self.ids.schwer3.text = self.manager.shared_variable2
            else:
                message.text = "Nicht genug Geld!"

        def cancel_payment(instance):
            popup.dismiss()
            self.manager.current = "GameOne"
            self.manager.transition.direction = "up"

        pay_button.bind(on_press = process_payment)
        close_button.bind(on_press = cancel_payment)
        popup.open()
        
    def start_balken(self):
        Clock.unschedule(self.update_progress)
        Clock.schedule_interval(self.update_progress, 0.05)
        self.ids.balken2.value = randint(1, 100)
        
    def update_progress(self, dt):
        if self.ids.balken1.value < self.ids.balken1.max:
            self.ids.balken1.value += 1
        else:
            self.ids.balken1.value = 0
    
    def stopp_balken(self):
        Clock.unschedule(self.update_progress)
        if self.ids.balken1.value == self.ids.balken2.value + 5 or self.ids.balken2.value - 5:
            if int(self.ids.schwer3.text) == 1:
                self.left_music.play()
                self.ids.geld8.text = str(int(self.ids.geld8.text) + 100)
        elif self.ids.balken1.value == self.ids.balken2.value + 4 or self.ids.balken2.value - 4:
            if int(self.ids.schwer3.text) < 3:
                self.left_music.play()
                self.ids.geld8.text = str(int(self.ids.geld8.text) + round(200 / int(self.ids.schwer3.text)))
        elif self.ids.balken1.value == self.ids.balken2.value + 3 or self.ids.balken2.value - 3:
            if int(self.ids.schwer3.text) < 4:
                self.left_music.play()
                self.ids.geld8.text = str(int(self.ids.geld8.text) + round(300 / int(self.ids.schwer3.text)))
        elif self.ids.balken1.value == self.ids.balken2.value + 2 or self.ids.balken2.value - 2:
            if int(self.ids.schwer3.text) < 5:
                self.left_music.play()
                self.ids.geld8.text = str(int(self.ids.geld8.text) + round(700 / int(self.ids.schwer3.text)))
        elif self.ids.balken1.value == self.ids.balken2.value + 1 or self.ids.balken2.value - 1:
            self.left_music.play()
            self.ids.geld8.text = str(int(self.ids.geld8.text) + round(1500 / int(self.ids.schwer3.text)))
        elif self.ids.balken1.value == self.ids.balken2.value:
            self.left_music.play()
            self.ids.geld8.text = str(int(self.ids.geld8.text) + round(2500 / int(self.ids.schwer3.text)))
        
        self.manager.shared_variable = self.ids.geld8.text
        save_game_data1(self.ids.geld8.text, self.ids.schwer3.text)
        
class GameFour(Screen):
    right_r_music = SoundLoader.load("Audios/right_right.wav")
    right_w_music = SoundLoader.load("Audios/right_wrong.mp3")
    
    def on_enter(self):
        self.ids.geld10.text = self.manager.shared_variable
        self.ids.schwer4.text = self.manager.shared_variable2
        if not check_game_payment("GameFour"):
            self.show_payment_popup("GameFour")
        else:
            self.ids.geld10.text = self.manager.shared_variable
            self.ids.schwer4.text = self.manager.shared_variable2

    def show_payment_popup(self, game_name):
        content = BoxLayout(orientation = "vertical", padding = 10, spacing = 10)
        message = Label(text = "Du musst " + str(15000  * int(self.ids.schwer4.text)) + "$ bezahlen, um dieses Spiel zu starten.")
        pay_button = Button(text = "Bezahlen")
        close_button = Button(text = "Abbrechen")
        content.add_widget(message)
        content.add_widget(pay_button)
        content.add_widget(close_button)

        popup = Popup(
            title = "Zugriff kaufen",
            content = content,
            size_hint = (0.8, 0.4),
            auto_dismiss = False
        )

        def process_payment(instance):
            if int(self.manager.shared_variable) >= 15000 * int(self.ids.schwer4.text):
                self.manager.shared_variable = str(int(self.manager.shared_variable) - 15000 * int(self.ids.schwer4.text))
                save_game_data1(self.manager.shared_variable, self.manager.shared_variable2)
                mark_game_as_paid(game_name)
                popup.dismiss()
                self.ids.geld10.text = self.manager.shared_variable
                self.ids.schwer4.text = self.manager.shared_variable2
            else:
                message.text = "Nicht genug Geld!"

        def cancel_payment(instance):
            popup.dismiss()
            self.manager.current = "GameTwo"
            self.manager.transition.direction = "down"

        pay_button.bind(on_press = process_payment)
        close_button.bind(on_press = cancel_payment)
        popup.open()
        
    def start_timer2(self):
        Clock.unschedule(self.set_timer2)
        self.ids.timer2.value = 0
        self.ids.ergebnis2.text = ""
        Clock.schedule_interval(self.set_timer2, 0.1)
        self.ids.zahl3.text = str(randint(1, 100))
        self.ids.zahl4.text = str(randint(1, 100))
        while int(self.ids.zahl3.text) < int(self.ids.zahl4.text):
            self.ids.zahl3.text = str(randint(1, 100))
            self.ids.zahl3.text = str(randint(1, 100))
        
    def set_timer2(self, dt):
        self.ids.timer2.value += 1
        if self.ids.timer2.value == 60:
            if self.ids.ergebnis2.text == "":
                self.right_w_music.play()
                self.ids.ergebnis2.background_color = [0.8, 0, 0, 1]
                Clock.unschedule(self.set_timer2)
                self.ids.timer2.value = 0
            elif not self.ids.ergebnis2.text.isdigit():
                self.right_w_music.play()
                self.ids.ergebnis2.background_color = [0.8, 0, 0, 1]
                Clock.unschedule(self.set_timer2)
                self.ids.timer2.value = 0
            elif int(self.ids.ergebnis2.text) == int(self.ids.zahl3.text) - int(self.ids.zahl4.text):
                    self.right_r_music.play()
                    self.ids.ergebnis2.background_color = [0, 0.8, 0, 1]
                    self.ids.geld10.text = str(int(self.ids.geld10.text) + round(10000 / int(self.ids.schwer4.text)))
                    Clock.unschedule(self.set_timer2)
            else:
                self.right_w_music.play()
                self.ids.ergebnis2.background_color = [0.8, 0, 0, 1]
                Clock.unschedule(self.set_timer2)
                self.ids.timer2.value = 0
        
        self.manager.shared_variable = self.ids.geld10.text
        save_game_data1(self.ids.geld10.text, self.ids.schwer4.text)

class GameFive(Screen):
    left_music = SoundLoader.load("Audios/left.wav")
    losing_music = SoundLoader.load("Audios/left_ttt.mp3")

    def on_enter(self):
        self.ids.geld12.text = self.manager.shared_variable
        self.ids.schwer5.text = self.manager.shared_variable2
        if not check_game_payment("GameFive"):
            self.show_payment_popup("GameFive")
        else:
            self.ids.geld12.text = self.manager.shared_variable
            self.ids.schwer5.text = self.manager.shared_variable2

    def show_payment_popup(self, game_name):
        content = BoxLayout(orientation = "vertical", padding = 10, spacing = 10)
        message = Label(text = "Du musst " + str(25000 * int(self.ids.schwer5.text)) + "$ bezahlen, um dieses Spiel zu starten.")
        pay_button = Button(text = "Bezahlen")
        close_button = Button(text = "Abbrechen")
        content.add_widget(message)
        content.add_widget(pay_button)
        content.add_widget(close_button)

        popup = Popup(
            title = "Zugriff kaufen",
            content = content,
            size_hint = (0.8, 0.4),
            auto_dismiss = False
        )

        def process_payment(instance):
            if int(self.manager.shared_variable) >= 25000 * int(self.ids.schwer5.text):
                self.manager.shared_variable = str(int(self.manager.shared_variable) - 25000 * int(self.ids.schwer5.text))
                save_game_data1(self.manager.shared_variable, self.manager.shared_variable2)
                mark_game_as_paid(game_name)
                popup.dismiss()
                self.ids.geld12.text = self.manager.shared_variable
                self.ids.schwer5.text = self.manager.shared_variable2
            else:
                message.text = "Nicht genug Geld!"

        def cancel_payment(instance):
            popup.dismiss()
            self.manager.current = "GameThree"
            self.manager.transition.direction = "right"

        pay_button.bind(on_press = process_payment)
        close_button.bind(on_press = cancel_payment)
        popup.open()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.TikTakToe = []
        self.create_ttt()
        
    def create_ttt(self):
        self.ids.ttt.text = "Besiege mich in TikTakToe"
        self.TikTakToe = [[True, True, True]]
        
        grds = [self.ids.grd1, self.ids.grd2, self.ids.grd3]
        for grid in grds:
            grid.clear_widgets()
            
        self.buttons = []
        
        for a, grid in enumerate(grds):
            for b in range(0, 3):
                btn = Button(text = "")
                btn.id = str(a) + str(b)
                btn.bind(on_press = self.btn_pressed)
                grid.add_widget(btn)
                self.buttons.append(btn)
                    
    def btn_pressed(self, instance):
        instance.text = "X"
        instance.disabled = True
        self.check_winner()
        self.press_random_button()
        
    def check_winner(self):
        grid_state = [[None for _ in range(3)] for _ in range(3)]
        for btn in self.buttons:
            row, col = map(int, btn.id)
            grid_state[row][col] = btn.text

        for row in grid_state:
            if row[0] == row[1] == row[2] == "O":
                self.ids.ttt.text = "Du hast verloren"
                self.losing_music.play()
                for btn in self.buttons:
                    btn.disabled = True
            elif row[0] == row[1] == row[2] == "X":
                self.ids.geld12.text = str(int(self.ids.geld12.text) + round(3000 / int(self.ids.schwer5.text)))
                self.ids.ttt.text = "Du hast gewonnen"
                self.left_music.play()
                for btn in self.buttons:
                    btn.disabled = True

        for col in range(3):
            if grid_state[0][col] == grid_state[1][col] == grid_state[2][col] == "O":
                self.ids.ttt.text = "Du hast verloren"
                self.losing_music.play()
                for btn in self.buttons:
                    btn.disabled = True
            elif grid_state[0][col] == grid_state[1][col] == grid_state[2][col] == "X":
                self.ids.geld12.text = str(int(self.ids.geld12.text) + round(3000 / int(self.ids.schwer5.text)))
                self.ids.ttt.text = "Du hast gewonnen"
                self.left_music.play()
                for btn in self.buttons:
                    btn.disabled = True

        if grid_state[0][0] == grid_state[1][1] == grid_state[2][2] == "O":
            self.ids.ttt.text = "Du hast verloren"
            self.losing_music.play()
            for btn in self.buttons:
                btn.disabled = True
        elif grid_state[0][0] == grid_state[1][1] == grid_state[2][2] == "X":
            self.ids.geld12.text = str(int(self.ids.geld12.text) + round(3000 / int(self.ids.schwer5.text)))
            self.ids.ttt.text = "Du hast gewonnen"
            self.left_music.play()
            for btn in self.buttons:
                btn.disabled = True

        if grid_state[0][2] == grid_state[1][1] == grid_state[2][0] == "O":
            self.ids.ttt.text = "Du hast verloren"
            self.losing_music.play()
            for btn in self.buttons:
                btn.disabled = True
        elif grid_state[0][2] == grid_state[1][1] == grid_state[2][0] == "X":
            self.ids.geld12.text = str(int(self.ids.geld12.text) + round(3000 / int(self.ids.schwer5.text)))
            self.ids.ttt.text = "Du hast gewonnen"
            self.left_music.play()
            for btn in self.buttons:
                btn.disabled = True
        
    def press_random_button(self):
        available_buttons = [btn for btn in self.buttons if btn.text == ""]
        if available_buttons:
            random_button = random.choice(available_buttons)
            random_button.text = "O"
            self.check_winner()
            random_button.disabled = True  
        else:
            self.ids.ttt.text = "Unentschieden"
            self.check_winner()
            if self.ids.ttt.text == "Unentschieden":
                self.losing_music.play()
                
        self.manager.shared_variable = self.ids.geld12.text
        save_game_data1(self.ids.geld12.text, self.ids.schwer5.text)
    
class GameSix(Screen):
    right_r_music = SoundLoader.load("Audios/right_right.wav")
    right_w_music = SoundLoader.load("Audios/right_wrong.mp3")

    def on_enter(self):
        self.ids.geld14.text = self.manager.shared_variable
        self.ids.schwer6.text = self.manager.shared_variable2
        if not check_game_payment("GameSix"):
            self.show_payment_popup("GameSix")
        else:
            self.ids.geld14.text = self.manager.shared_variable
            self.ids.schwer6.text = self.manager.shared_variable2

    def show_payment_popup(self, game_name):
        content = BoxLayout(orientation = "vertical", padding = 10, spacing = 10)
        message = Label(text = "Du musst " + str(50000 * int(self.ids.schwer6.text)) + "$ bezahlen, um dieses Spiel zu starten.")
        pay_button = Button(text = "Bezahlen")
        close_button = Button(text = "Abbrechen")
        content.add_widget(message)
        content.add_widget(pay_button)
        content.add_widget(close_button)

        popup = Popup(
            title = "Zugriff kaufen",
            content = content,
            size_hint = (0.8, 0.4),
            auto_dismiss = False
        )

        def process_payment(instance):
            if int(self.manager.shared_variable) >= 50000 * int(self.ids.schwer6.text):
                self.manager.shared_variable = str(int(self.manager.shared_variable) - 50000 * int(self.ids.schwer6.text))
                save_game_data1(self.manager.shared_variable, self.manager.shared_variable2)
                mark_game_as_paid(game_name)
                popup.dismiss()
                self.ids.geld14.text = self.manager.shared_variable
                self.ids.schwer6.text = self.manager.shared_variable2
            else:
                message.text = "Nicht genug Geld!"

        def cancel_payment(instance):
            popup.dismiss()
            self.manager.current = "GameFour"
            self.manager.transition.direction = "left"

        pay_button.bind(on_press = process_payment)
        close_button.bind(on_press = cancel_payment)
        popup.open()
        
    def start_timer3(self):
        Clock.unschedule(self.set_timer3)
        self.ids.timer3.value = 0
        self.ids.ergebnis3.text = ""
        Clock.schedule_interval(self.set_timer3, 0.12)
        self.ids.zahl5.text = str(randint(1, 20))
        self.ids.zahl6.text = str(randint(1, 20))    
        
    def set_timer3(self, dt):
        self.ids.timer3.value += 1
        if self.ids.timer3.value == 60:
            if self.ids.ergebnis3.text == "":
                self.right_w_music.play()
                self.ids.ergebnis3.background_color = [0.8, 0, 0, 1]
                Clock.unschedule(self.set_timer3)
                self.ids.timer3.value = 0
            elif not self.ids.ergebnis3.text.isdigit():
                self.right_w_music.play()
                self.ids.ergebnis3.background_color = [0.8, 0, 0, 1]
                Clock.unschedule(self.set_timer3)
                self.ids.timer3.value = 0
            elif int(self.ids.ergebnis3.text) == int(self.ids.zahl5.text) * int(self.ids.zahl6.text):
                    self.right_r_music.play()
                    self.ids.ergebnis3.background_color = [0, 0.8, 0, 1]
                    self.ids.geld14.text = str(int(self.ids.geld14.text) + round(25000 / int(self.ids.schwer6.text)))
                    Clock.unschedule(self.set_timer3)
            else:
                self.right_w_music.play()
                self.ids.ergebnis3.background_color = [0.8, 0, 0, 1]
                Clock.unschedule(self.set_timer3)
                self.ids.timer3.value = 0
                
        self.manager.shared_variable = self.ids.geld14.text
        save_game_data1(self.ids.geld14.text, self.ids.schwer6.text)

class GameSeven(Screen, BoxLayout):
    left_music = SoundLoader.load("Audios/left.wav")
    bomb = SoundLoader.load("Audios/bomb.mp3")
    rows = 10
    cols = 10
    
    def on_enter(self):
        self.ids.geld16.text = self.manager.shared_variable
        self.ids.schwer7.text = self.manager.shared_variable2
        if not check_game_payment("GameSeven"):
            self.show_payment_popup("GameSeven")
        else:
            self.ids.geld16.text = self.manager.shared_variable
            self.ids.schwer7.text = self.manager.shared_variable2

    def show_payment_popup(self, game_name):
        content = BoxLayout(orientation = "vertical", padding = 10, spacing = 10)
        message = Label(text = "Du musst " + str(75000 * int(self.ids.schwer7.text)) + "$ bezahlen, um dieses Spiel zu starten.")
        pay_button = Button(text = "Bezahlen")
        close_button = Button(text = "Abbrechen")
        content.add_widget(message)
        content.add_widget(pay_button)
        content.add_widget(close_button)

        popup = Popup(
            title = "Zugriff kaufen",
            content = content,
            size_hint = (0.8, 0.4),
            auto_dismiss = False
        )

        def process_payment(instance):
            if int(self.manager.shared_variable) >= 75000 * int(self.ids.schwer7.text):
                self.manager.shared_variable = str(int(self.manager.shared_variable) - 75000 * int(self.ids.schwer7.text))
                save_game_data1(self.manager.shared_variable, self.manager.shared_variable2)
                mark_game_as_paid(game_name)
                popup.dismiss()
                self.ids.geld16.text = self.manager.shared_variable
                self.ids.schwer7.text = self.manager.shared_variable2
            else:
                message.text = "Nicht genug Geld!"

        def cancel_payment(instance):
            popup.dismiss()
            self.manager.current = "GameFive"
            self.manager.transition.direction = "right"

        pay_button.bind(on_press = process_payment)
        close_button.bind(on_press = cancel_payment)
        popup.open()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.minefield = []
        self.create_minefield()
        
    def create_minefield(self):
        grids = [self.ids.grid1, self.ids.grid2, self.ids.grid3, self.ids.grid4, self.ids.grid5]
        for grid in grids:
            rows, cols = 2, 10 
            minefield = [
                [bool(random.getrandbits(1)) for _ in range(cols)]
                for _ in range(rows)
            ]
            grid.clear_widgets()
            for row in minefield:
                for cell in row:
                    btn = Button(text = "")
                    btn.type = "money" if cell else "bomb"
                    btn.bind(on_press=self.cell_pressed)
                    grid.add_widget(btn)
    
    def cell_pressed(self, instance):
        if int(self.ids.geld16.text) < 20000 * int(self.ids.schwer7.text):
            self.ids.labelm.text = "Du hast zu wenig Geld um zu spielen!"
        else:
            if instance.type == "money":
                self.left_music.play()
                instance.background_color = [0, 0.8, 0, 1]
                instance.background_normal = ''
                instance.background_down = ''
                instance.text = "$"
                instance.unbind(on_press=self.cell_pressed)
                self.ids.geld16.text = str(round(int(self.ids.geld16.text) * (1.21 - int(self.ids.schwer7.text) * 0.01)))           
            else:
                self.bomb.play()
                instance.background_color = [0.8, 0, 0, 1]
                instance.background_normal = ''
                instance.background_down = ''
                instance.text = "X"
                instance.unbind(on_press = self.cell_pressed)
                self.ids.geld16.text = str(int(self.ids.geld16.text) - 20000 * int(self.ids.schwer7.text))
                    
        self.manager.shared_variable = self.ids.geld16.text
        save_game_data1(self.ids.geld16.text, self.ids.schwer7.text)
    
class GameEight(Screen):
    right_r_music = SoundLoader.load("Audios/right_right.wav")
    right_w_music = SoundLoader.load("Audios/right_wrong.mp3")

    def on_enter(self):
        self.ids.geld18.text = self.manager.shared_variable
        self.ids.schwer8.text = self.manager.shared_variable2
        
        if not check_game_payment("GameEight"):
            self.show_payment_popup("GameEight")
        else:
            self.ids.geld18.text = self.manager.shared_variable
            self.ids.schwer8.text = self.manager.shared_variable2
            
    def show_payment_popup(self, game_name):
        content = BoxLayout(orientation = "vertical", padding = 10, spacing = 10)
        message = Label(text = "Du musst " + str(100000 * int(self.ids.schwer8.text)) + "$ bezahlen, um dieses Spiel zu starten.")
        pay_button = Button(text = "Bezahlen")
        close_button = Button(text = "Abbrechen")
        content.add_widget(message)
        content.add_widget(pay_button)
        content.add_widget(close_button)

        popup = Popup(
            title = "Zugriff kaufen",
            content = content,
            size_hint = (0.8, 0.4),
            auto_dismiss = False
        )

        def process_payment(instance):
            if int(self.manager.shared_variable) >= 100000 * int(self.ids.schwer8.text):
                self.manager.shared_variable = str(int(self.manager.shared_variable) - 100000 * int(self.ids.schwer8.text))
                save_game_data1(self.manager.shared_variable, self.manager.shared_variable2)
                mark_game_as_paid(game_name)
                popup.dismiss()
                self.ids.geld18.text = self.manager.shared_variable
                self.ids.schwer8.text = self.manager.shared_variable2
            else:
                message.text = "Nicht genug Geld!"

        def cancel_payment(instance):
            popup.dismiss()
            self.manager.current = "GameSix"
            self.manager.transition.direction = "left"

        pay_button.bind(on_press = process_payment)
        close_button.bind(on_press = cancel_payment)
        popup.open()
        
    def start_timer4(self):
        Clock.unschedule(self.set_timer4)
        self.ids.timer4.value = 0
        self.ids.ergebnis4.text = ""
        Clock.schedule_interval(self.set_timer4, 0.12)
        self.ids.zahl7.text = str(randint(1, 1000))
        self.ids.zahl8.text = str(randint(1, 1000))
        while not int(self.ids.zahl7.text) % int(self.ids.zahl8.text) == 0:
            self.ids.zahl7.text = str(randint(1, 1000))
            self.ids.zahl8.text = str(randint(1, 1000))
        
    def set_timer4(self, dt):
        self.ids.timer4.value += 1
        if self.ids.timer4.value == 60:
            if self.ids.ergebnis4.text == "":
                self.right_w_music.play()
                self.ids.ergebnis4.background_color = [0.8, 0, 0, 1]
                Clock.unschedule(self.set_timer4)
                self.ids.timer4.value = 0
            elif not self.ids.ergebnis4.text.isdigit():
                self.right_w_music.play()
                self.ids.ergebnis4.background_color = [0.8, 0, 0, 1]
                Clock.unschedule(self.set_timer4)
                self.ids.timer4.value = 0
            elif int(self.ids.ergebnis4.text) == int(self.ids.zahl7.text) / int(self.ids.zahl8.text):
                    self.right_r_music.play()
                    self.ids.ergebnis4.background_color = [0, 0.8, 0, 1]
                    gewinn = round(25000 / int(self.ids.schwer8.text))
                    self.ids.geld18.text = str(int(self.ids.geld18.text) + gewinn)
                    Clock.unschedule(self.set_timer4)
            else:
                self.right_w_music.play()
                self.ids.ergebnis4.background_color = [0.8, 0, 0, 1]
                Clock.unschedule(self.set_timer4)
                self.ids.timer4.value = 0
                
        self.manager.shared_variable = self.ids.geld18.text
        save_game_data1(self.ids.geld18.text, self.ids.schwer8.text)
        
        
class Upgrades(Screen):
    def on_enter(self):
        self.ids.geld20.text = self.manager.shared_variable
        self.ids.schwer9.text = self.manager.shared_variable2
        
        if not check_game_payment("Upgrades"):
            self.show_payment_popup("Upgrades")
        else:
            self.ids.geld20.text = self.manager.shared_variable
            self.ids.schwer9.text = self.manager.shared_variable2
            
    def show_payment_popup(self, game_name):
        content = BoxLayout(orientation = "vertical", padding = 10, spacing = 10)
        message = Label(text = "Du musst einmalig 500000$ bezahlen, um die Upgrades freizuschalten.")
        pay_button = Button(text = "Bezahlen")
        close_button = Button(text = "Abbrechen")
        content.add_widget(message)
        content.add_widget(pay_button)
        content.add_widget(close_button)

        popup = Popup(
            title = "Zugriff kaufen",
            content = content,
            size_hint = (0.8, 0.4),
            auto_dismiss = False
        )

        def process_payment(instance):
            if int(self.manager.shared_variable) >= 500000:
                self.manager.shared_variable = str(int(self.manager.shared_variable) - 500000)
                save_game_data1(self.manager.shared_variable, self.manager.shared_variable2)
                mark_game_as_paid(game_name)
                popup.dismiss()
                self.ids.geld20.text = self.manager.shared_variable
                self.ids.schwer9.text = self.manager.shared_variable2
            else:
                message.text = "Nicht genug Geld!"

        def cancel_payment(instance):
            popup.dismiss()
            self.manager.current = "GameSeven"
            self.manager.transition.direction = "right"

        pay_button.bind(on_press = process_payment)
        close_button.bind(on_press = cancel_payment)
        popup.open()


    def pro_klick(self):
        save_upgrades("$_pro_klick")
        self.ids.pro_klick1.text = "1"
 
 
class Statistics(Screen):
    def on_enter(self):
        self.ids.geld22.text = self.manager.shared_variable
        self.ids.schwer10.text = self.manager.shared_variable2
        
        if not check_game_payment("Statistics"):
            self.show_payment_popup("Statistics")
        else:
            self.ids.geld22.text = self.manager.shared_variable
            self.ids.schwer10.text = self.manager.shared_variable2
            
    def show_payment_popup(self, game_name):
        content = BoxLayout(orientation = "vertical")
        message = Label(text = "Du musst einmalig 500000$ bezahlen, \num die Statistiken einsehen zu können.")
        pay_button = Button(text = "Bezahlen")
        close_button = Button(text = "Abbrechen")
        content.add_widget(message)
        content.add_widget(pay_button)
        content.add_widget(close_button)

        popup = Popup(
            title = "Zugriff kaufen",
            content = content,
            auto_dismiss = False
        )

        def process_payment(instance):
            if int(self.manager.shared_variable) >= 500000:
                self.manager.shared_variable = str(int(self.manager.shared_variable) - 500000)
                save_game_data1(self.manager.shared_variable, self.manager.shared_variable2)
                mark_game_as_paid(game_name)
                popup.dismiss()
                self.ids.geld22.text = self.manager.shared_variable
                self.ids.schwer10.text = self.manager.shared_variable2
            else:
                message.text = "Nicht genug Geld!"

        def cancel_payment(instance):
            popup.dismiss()
            self.manager.current = "GameEight"
            self.manager.transition.direction = "left"

        pay_button.bind(on_press = process_payment)
        close_button.bind(on_press = cancel_payment)
        popup.open()
        
        

class MainApp(App):
    def build(self):
        create_database1()
        create_database2()
        create_database3()
        create_upgrades()
        create_game_access_table()
        Window.set_icon("icon.png")
        sm = MyScreenManager(transition = SlideTransition())
        sm.add_widget(Start(name = "Start"))
        sm.add_widget(Kasino(name = "Kasino"))
        sm.add_widget(GameOne(name = "GameOne"))
        sm.add_widget(GameTwo(name = "GameTwo"))
        sm.add_widget(GameThree(name = "GameThree"))
        sm.add_widget(GameFour(name = "GameFour"))
        sm.add_widget(GameFive(name = "GameFive"))
        sm.add_widget(GameSix(name = "GameSix"))
        sm.add_widget(GameSeven(name = "GameSeven"))
        sm.add_widget(GameEight(name = "GameEight"))
        sm.add_widget(Upgrades(name = "Upgrades"))
        sm.add_widget(Statistics(name = "Statistics"))
        pb = ProgressBar(max=500)
        pb.value = 0
        if background_music:
            background_music.loop = True
            background_music.volume = 0.5
            background_music.play()
        sm.transition = SlideTransition()
        return sm
    
    background_color = ListProperty([])
    
    def background_color_set(self):
        return [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1]

    def change_color(self, color):
        self.background_color = color
    
    def transition_to(self, screen_name):
            self.manager.transition = FadeTransition()
            self.manager.current = screen_name
    
    def on_stop(self):
        if background_music:
            background_music.stop()
    

if __name__ == '__main__':
    MainApp().run()