from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from libdw import sm
import random


bag_of_words = {'cotton': 'c _ t_ _ _', 'magnet': 'm _ _ m _ _ ', 'ghost': 'g _ o _ _',
                'poodle': '_ o _ _ l _', 'exodus': '_ x _ _  u _', 'sphinx': 's _ h _ _ _',
                'scratch': 's _ _ a _ _ _', 'vodka': 'v _ _ _ a', 'zombie': '_ o _ b _ _'
                }
references = ['cotton', 'magnet', 'ghost', 'poodle', 'exodus', 'sphinx', 'scratch', 'vodka', 'zombie']
answer = references[random.randint(0, len(references)-1)]  #sets randomized answer to guess in game
thehint = bag_of_words[answer]                  #provides hint to user match to answer variable



Builder.load_file('MainApp.kv')    #loads the kv file for usage


class MainGame(BoxLayout, sm.SM):  #maingame class
    def __init__(self, **kwargs):                    #set state of game at 0 (image w/ bar), with 1 as image w/ bar+head
        super(MainGame, self).__init__(**kwargs)     # and 2 as image w/ bar+head+body
        Clock.schedule_interval(self.init_ui, 0)     #used such that the hint can be initialized at the start
        self.state = 0
        self.correct = SoundLoader.load('correct_ans.mp3')  # loads the correct sound effect
        self.wrong = SoundLoader.load('wrong_ans.mp3')     #loads the wrong sound effect

    def init_ui(self, dt=0):
        global thehint                              #provides access to thehint variable at global lvl
        hint = self.ids.hints
        hint.text = thehint

    def get_next_values(self, state, inp):
        global answer                              #provides access to thehint, answer variables at global level
        global thehint                             
        image = self.ids.status
        if state == 0:
            if inp == answer:
                self.correct.play()
                new_state = 0
                answer = references[random.randint(0, len(references)-1)]
                thehint = bag_of_words[answer]
                return new_state, "scrn_win"      #screen transition to YouWin class window
            elif inp != answer:
                self.wrong.play()
                new_state = 1
                image.source = 'hangman1.jpg'     #img w/ bar+head
                return new_state, "scrn_game"
        if state == 1:
            if inp == answer:
                self.correct.play()
                new_state = 0
                image.source = 'hangman0.jpg'
                answer = references[random.randint(0, len(references)-1)]
                thehint = bag_of_words[answer]
                return new_state, "scrn_win"
            elif inp != answer:
                self.wrong.play()
                new_state = 2
                image.source = 'hangman2.jpg'    #img w/ bar+head+body
                return new_state, "scrn_game"
        elif state == 2:
            if inp == answer:
                self.correct.play()
                new_state = 0
                answer = references[random.randint(0, len(references)-1)]
                thehint = bag_of_words[answer]
                return new_state, "scrn_win"
            elif inp != answer:
                self.wrong.play()
                new_state = 0
                image.source = 'hangman0.jpg'
                answer = references[random.randint(0, len(references)-1)]
                thehint = bag_of_words[answer]
                return new_state, "scrn_lose"       #screen transition to YouLose class window



    def validate(self, *args):
        inputs = self.ids.guess
        inp = inputs.text
        print(inp)
        if inp == '' or None:      #this statement has to be used as you cannot pass inp as None in self.step(inp)
            pass
        else:
            o = self.step(inp)
            print(o)
            self.parent.parent.current = str(o)      #tells kivy what screen to show to user
            self.ids.guess.text = ''
            print(self.state)
            print('\n')



class YouLose(BoxLayout):
    pass

class YouWin(BoxLayout):
    pass

class MainWindow(BoxLayout):

    game_widget = MainGame()
    win_widget = YouWin()
    lose_widget = YouLose()

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        Clock.schedule_once(self.init_window, 0)
    def init_window(self, dt=0):
        self.ids.scrn_game.add_widget(self.game_widget)
        self.ids.scrn_win.add_widget(self.win_widget)
        self.ids.scrn_lose.add_widget(self.lose_widget)
        print(self.ids)

class MainApp(App):
    def build(self):
        return MainWindow()

if __name__=='__main__':
    MainApp().run()
