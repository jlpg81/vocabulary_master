import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)
from kivy.uix.widget import Widget
from kivy.graphics import Color
from kivy.app import App
import sqlite3
import datetime
import os
from install import install_database
current_cards = []
# from button import BlueButton
# from kivy.graphics import Rectangle

# class BlueButton(Button):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

#         with self.canvas:
#             Rectangle(source = "./images/button/blue_button.jpg", size = (500, 100))
            

"""
Main Functions - We can send these to other files if needed
"""
def days_left():
    c.execute("SELECT * FROM flashcards")
    cards = c.fetchall()
    try:
        for i in cards:
            # print(i)
            year = int(i[4][0:4])
            month = int(i[4][5:7])
            day = int(i[4][8:10])
            last_date = datetime.date(year, month, day)
            days_added = spaced_repetition(i[3])
            days_left = last_date + datetime.timedelta(days_added) - datetime.date.today()
            a = str(days_left).replace("0:00:00","")
            try:
                a = a.strip(" days,")
            except:
                a = 0
            c.execute("REPLACE INTO flashcards VALUES (:id, :english, :vietnamese, :word_level, :word_date, :days_left)",
            {'id':i[0], 'english':i[1], 'vietnamese':i[2], 'word_level':i[3], 'word_date':i[4], 'days_left': a})
            conn.commit()
    except:
        pass
        
def repeat():
    if current_cards[0][3] >= 1:
        new_level = current_cards[0][3] - 1
    else:
        current_cards.append(current_cards[0])
        new_level = 0
    # print(new_level)
    # print(current_cards[0])
    # print("repeat at lvl 0") 
    c.execute("REPLACE INTO flashcards VALUES (:id, :english, :vietnamese, :word_level, :word_date, :days_left)",
    {'id':current_cards[0][0], 'english':current_cards[0][1], 'vietnamese':current_cards[0][2], 'word_level':new_level, 'word_date':datetime.date.today(), 'days_left': 0})
    conn.commit()

def add_one_level():
    new_level = current_cards[0][3] + 1
    # print(new_level)
    # print(current_cards[0])
    # print("advance 1 level") 
    c.execute("REPLACE INTO flashcards VALUES (:id, :english, :vietnamese, :word_level, :word_date, :days_left)",
    {'id':current_cards[0][0], 'english':current_cards[0][1], 'vietnamese':current_cards[0][2], 'word_level':new_level, 'word_date':datetime.date.today(), 'days_left': spaced_repetition(new_level)})
    conn.commit()

def add_two_levels():
    new_level = current_cards[0][3] + 2
    # print(new_level)
    # print(current_cards[0])
    # print("advance 2 levels") 
    c.execute("REPLACE INTO flashcards VALUES (:id, :english, :vietnamese, :word_level, :word_date, :days_left)",
    {'id':current_cards[0][0], 'english':current_cards[0][1], 'vietnamese':current_cards[0][2], 'word_level':new_level, 'word_date':datetime.date.today(), 'days_left': spaced_repetition(new_level)})
    conn.commit()

def spaced_repetition(level):
    if level == 0:
        return 0
    elif level == 1:
        return 1
    elif level == 2:
        return 2
    elif level == 3:
        return 3
    elif level == 4:
        return 4
    elif level == 5:
        return 5
    elif level == 6:
        return 6
    elif level == 7:
        return 7
    elif level == 8:
        return 8


"""
Database code
"""
#Installing database
if os.path.exists("flashcards.db"):
    # print("Database exists")
    pass
else:
    # print("Installing database...")
    install_database()

#Accessing Database
conn = sqlite3.connect("flashcards.db")
c = conn.cursor()

#Recalculate days left until cards reappear
days_left()


#Requesting new cards
c.execute("SELECT * FROM flashcards WHERE days_left <= 0")
current_cards = c.fetchmany(10)


"""
Kivy Pages
"""
class MainPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__( **kwargs)
        self.cols = 1

        self.img=Image(source ='.\\images\\logo\\logo.png')
        self.img
        self.add_widget(self.img)

        self.start_button = Button(text='Start')
        self.start_button.bind(on_press = self.start)
        self.add_widget(self.start_button)

        self.statistics_button = Button(text='Statistics')
        self.statistics_button.bind(on_press = self.statistics)
        self.add_widget(self.statistics_button)

        self.instructions_button = Button(text='Instructions')
        self.instructions_button.bind(on_press = self.instructions)
        self.add_widget(self.instructions_button)

        self.quit_button = Button(text='Quit')
        self.quit_button.bind(on_press = self.quit)
        self.add_widget(self.quit_button)
    
    def start(self, instance):
        if current_cards == []:
            language_app.screen_manager.current = "Finished"
        else:
            language_app.screen_manager.current = "Flash"

    def statistics(self, instance):
        language_app.screen_manager.current = "Statistics"
    
    def instructions(self, instance):
        language_app.screen_manager.current = "Instructions"

    def quit(self, instance):
        quit()

class FlashcardsPage(GridLayout):
    def __init__(self, **kwargs):
        super(FlashcardsPage, self).__init__( **kwargs)
        self.cols = 1
        try:
            self.title = Label(text=current_cards[0][2], color=[0, 0, 0, 1])
            self.add_widget(self.title)

            self.img=Image(source ='.\\images\\{}\\{}.jpg'.format(current_cards[0][0], current_cards[0][1]))
            self.add_widget(self.img)

            #Display buttons
            self.results_button = Button(text='Next')
            self.results_button.bind(on_press = self.results)
            self.add_widget(self.results_button)
        except:
            language_app.screen_manager.current = "Main"

    def results(self, instance):
        App.get_running_app().results_page.title.text = current_cards[0][2]
        App.get_running_app().results_page.answer.text = current_cards[0][1]
        App.get_running_app().results_page.img.source = '.\\images\\{}\\{}.jpg'.format(current_cards[0][0], current_cards[0][1])
        language_app.screen_manager.current = "Result"

    def finished(self):
        language_app.screen_manager.current = "Main"

class ResultsPage(GridLayout):
    def __init__(self, **kwargs):
        super(ResultsPage, self).__init__( **kwargs)
        self.cols = 1

        # Display current card data
        try:
            self.title = Label(text=current_cards[0][2], color=[0, 0, 0, 1])
            self.add_widget(self.title)

            self.img=Image(source ='.\\images\\{}\\{}.jpg'.format(current_cards[0][0], current_cards[0][1]))
            self.add_widget(self.img)

            self.answer = Label(text=current_cards[0][1], color=[0, 0, 0, 1])
            self.add_widget(self.answer)
        except:
            language_app.screen_manager.current = "Main"

        #Display buttons
        self.repeat_button = Button(text='Repeat (-1)')
        self.repeat_button.bind(on_press = self.repeat_card)
        self.add_widget(self.repeat_button)

        self.ok_button = Button(text='Ok (+1)')
        self.ok_button.bind(on_press = self.ok_card)
        self.add_widget(self.ok_button)

        self.easy_button = Button(text='Easy (+2)')
        self.easy_button.bind(on_press = self.easy_card)
        self.add_widget(self.easy_button)

        self.add_widget(Label(text=''))

        self.back_button = Button(text='Back to main menu')
        self.back_button.bind(on_press = self.back)
        self.add_widget(self.back_button)


    def repeat_card(self, instance):
        print("repeat card..")
        try:
            repeat()
            current_cards.pop(0)
            App.get_running_app().flashcards_page.title.text = current_cards[0][2]
            App.get_running_app().flashcards_page.img.source = '.\\images\\{}\\{}.jpg'.format(current_cards[0][0], current_cards[0][1])
            language_app.screen_manager.current = "Flash"
        except:
            language_app.screen_manager.current = "Finished"

    def ok_card(self, instance):
        print("ok card..")
        try:
            add_one_level()
            current_cards.pop(0)
            App.get_running_app().flashcards_page.title.text = current_cards[0][2]
            App.get_running_app().flashcards_page.img.source = '.\\images\\{}\\{}.jpg'.format(current_cards[0][0], current_cards[0][1])
            language_app.screen_manager.current = "Flash"
        except:
            language_app.screen_manager.current = "Finished"

    def easy_card(self, instance):
        print("easy card..")
        try:
            add_two_levels()
            current_cards.pop(0)
            App.get_running_app().flashcards_page.title.text = current_cards[0][2]
            App.get_running_app().flashcards_page.img.source = '.\\images\\{}\\{}.jpg'.format(current_cards[0][0], current_cards[0][1])
            # print(current_cards)
            language_app.screen_manager.current = "Flash"
        except:
            language_app.screen_manager.current = "Finished"

    def back(self, instance):
        language_app.screen_manager.current = "Main"

class FinishedPage(GridLayout):
    def __init__(self, **kwargs):
        super(FinishedPage, self).__init__( **kwargs)
        self.cols = 1
        
        self.add_widget(Label(text="You finished your cards for today. Please come back tomorrow.", color=[0, 0, 0, 1]))

        self.finished_button = Button(text='Finish')
        self.finished_button.bind(on_press = self.finished)
        self.add_widget(self.finished_button)

    def finished(self, instance):
        language_app.screen_manager.current = "Main"

class StatisticsPage(GridLayout):
    def __init__(self, **kwargs):
        super(StatisticsPage, self).__init__( **kwargs)
        self.cols = 1

        self.add_widget(Label(text='Statistics page here...', color=[0, 0, 0, 1]))

        self.back_button = Button(text='Back to main menu')
        self.back_button.bind(on_press = self.back)
        self.add_widget(self.back_button)

    def back(self, instance):
        language_app.screen_manager.current = "Main"


class InstructionsPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__( **kwargs)
        self.cols = 1

        self.add_widget(Label(text='Welcome to VocabularyMaster', color=[0, 0, 0, 1]))

        self.add_widget(Label(text='Instructions will be written here soon...', color=[0, 0, 0, 1]))

        self.back_button = Button(text='Back to main menu')
        self.back_button.bind(on_press = self.back)
        self.add_widget(self.back_button)


    def back(self, instance):
        language_app.screen_manager.current = "Main"
        

class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        
        self.main_page = MainPage()
        screen = Screen(name = "Main")
        screen.add_widget(self.main_page)
        self.screen_manager.add_widget(screen)

        self.flashcards_page = FlashcardsPage()
        screen = Screen(name = "Flash")
        screen.add_widget(self.flashcards_page)
        self.screen_manager.add_widget(screen)

        self.results_page = ResultsPage()
        screen = Screen(name = "Result")
        screen.add_widget(self.results_page)
        self.screen_manager.add_widget(screen)

        self.finished_page = FinishedPage()
        screen = Screen(name = "Finished")
        screen.add_widget(self.finished_page)
        self.screen_manager.add_widget(screen)

        self.statistics_page = StatisticsPage()
        screen = Screen(name = "Statistics")
        screen.add_widget(self.statistics_page)
        self.screen_manager.add_widget(screen)

        self.instructions_page = InstructionsPage()
        screen = Screen(name = "Instructions")
        screen.add_widget(self.instructions_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

if __name__ == "__main__":
    # add database creation if it does not yet exist, by running install.py
    language_app = MyApp()
    language_app.run()