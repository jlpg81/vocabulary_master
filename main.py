import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)
from kivy.graphics import Color
import sqlite3
# from flashcards import FlashcardsPage
# global current_cards
# from kivy.properties import ObjectProperty, ListProperty
current_cards = []
import random
from kivy.app import App
from kivy.properties import ObjectProperty


#Access Database
conn = sqlite3.connect("flashcards.db")
c = conn.cursor()
c.execute("SELECT * FROM flashcards WHERE word_date = 0")
current_cards = c.fetchmany(5)
print(current_cards)

sm = """
ScreenManager:
    id:manager
    FlashcardsPage:
        id:FlashcardsPage
    ResultsPage:
        id:ResultsPage
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
        language_app.screen_manager.current = "Flash"

    def statistics(self, instance):
        language_app.screen_manager.current = "Statistics"
    
    def instructions(self, instance):
        language_app.screen_manager.current = "Instructions"

    def quit(self, instance):
        quit()

class FlashcardsPage(GridLayout):
    flashcard_stuff = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(FlashcardsPage, self).__init__( **kwargs)
        self.cols = 1

        if current_cards == []:
            self.add_widget(Label(text="You finished your cards for today. Please come back tomorrow.", color=[0, 0, 0, 1]))

            self.finished_button = Button(text='Finish')
            self.finished_button.bind(on_press = self.finished)
            self.add_widget(self.finished_button)
        
        else:
            # Display current card data
            self.title = Label(text=current_cards[0][2], color=[0, 0, 0, 1])
            self.add_widget(self.title)

            self.img=Image(source ='.\\images\\{}\\{}.jpg'.format(current_cards[0][0], current_cards[0][1]))
            self.add_widget(self.img)

            #Display buttons
            self.results_button = Button(text='Next')
            self.results_button.bind(on_press = self.results)
            self.add_widget(self.results_button)

    def results(self, instance):
        # current_cards.pop(0)
        # self.title.text = current_cards[0][2]
        # self.img.source = '.\\images\\{}\\{}.jpg'.format(current_cards[0][0], current_cards[0][1])
        # print(App.get_running_app().root.ids)
        # self.title.text = str(random.randint(0,200))
        # print(App.get_running_app().root.parent.FlashcardsPage)
        # self.update()
        # object_methods = [method_name for method_name in dir(App.get_running_app()) if callable(getattr(App.get_running_app(), method_name))]
        # print(object_methods)
        language_app.screen_manager.current = "Result"

    def finished(self, instance):
        language_app.screen_manager.current = "Main"

    def update(self):
        # self.results_button.clear_widgets
        pass

class ResultsPage(GridLayout):
    results_stuff = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ResultsPage, self).__init__( **kwargs)
        self.cols = 1

        # Display current card data
        self.data = current_cards
        
        try:
            self.title = Label(text=self.data[0][2], color=[0, 0, 0, 1])
            self.add_widget(self.title)


            self.img=Image(source ='.\\images\\{}\\{}.jpg'.format(current_cards[0][0], current_cards[0][1]))
            self.add_widget(self.img)

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
        except:
            pass

    def repeat_card(self, instance):
        print("repeat card..")
        try:
            current_cards.pop(0)
            App.get_running_app().flashcards_page.title.text = current_cards[0][2]
            App.get_running_app().flashcards_page.img.source = '.\\images\\{}\\{}.jpg'.format(current_cards[0][0], current_cards[0][1])
            print(current_cards)
            print("doing try")
            language_app.screen_manager.current = "Flash"
            App.get_running_app().results_page.title.text = current_cards[0][2]
            App.get_running_app().results_page.img.source = '.\\images\\{}\\{}.jpg'.format(current_cards[0][0], current_cards[0][1])
        except:
            language_app.screen_manager.current = "Main"

    def ok_card(self, instance):
        print("ok card..")
        try:
            current_cards.pop(0)
            App.get_running_app().flashcards_page.title.text = current_cards[0][2]
            App.get_running_app().flashcards_page.img.source = '.\\images\\{}\\{}.jpg'.format(current_cards[0][0], current_cards[0][1])
            print(current_cards)
            print("doing try")
            language_app.screen_manager.current = "Flash"
            App.get_running_app().results_page.title.text = current_cards[0][2]
            App.get_running_app().results_page.img.source = '.\\images\\{}\\{}.jpg'.format(current_cards[0][0], current_cards[0][1])
        except:
            language_app.screen_manager.current = "Main"

    def easy_card(self, instance):
        print("easy card..")
        try:
            current_cards.pop(0)
            App.get_running_app().flashcards_page.title.text = current_cards[0][2]
            App.get_running_app().flashcards_page.img.source = '.\\images\\{}\\{}.jpg'.format(current_cards[0][0], current_cards[0][1])
            print(current_cards)
            print("doing try")
            language_app.screen_manager.current = "Flash"
            App.get_running_app().results_page.title.text = current_cards[0][2]
            App.get_running_app().results_page.img.source = '.\\images\\{}\\{}.jpg'.format(current_cards[0][0], current_cards[0][1])
        except:
            language_app.screen_manager.current = "Main"

    def back(self, instance):
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


        # screen.add_widget(FlashcardsPage())
        # MyApp.screen_manager.add_widget(Screen(name = "Flash"))


        self.results_page = ResultsPage()
        screen = Screen(name = "Result")
        screen.add_widget(self.results_page)
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


        # return MainMenu()

if __name__ == "__main__":
    # add database creation if it does not yet exist, by running install.py
    language_app = MyApp()
    language_app.run()