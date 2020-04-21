# SUTD-Digital-World-10.009 Final Programming Assignment

Hi Profs, in here you will find the explanations on the final exam programming assignment gameplay as well as the code.  

## Installation  
 
Do ensure that the .py, .kv, .jpg and .mp3 files included are all in the same single folder to ensure smooth operation of the game. 
The files are:   
1. hangmanv2.py 
2. MainApp.kv 
3. hangman0.jpg 
4. hangman1.jpg 
5. hangman2.jpg  
6. correct.mp3 
7. wrong.mp3  
 
Ensure your dependencies are of the latest version:     
1. kivy_deps.gstreamer  0.2.0   
2. kivy_deps.angle      0.2.0  
3. kivy_deps.glew       0.2.0  
4. kivy_deps.sdl2       0.2.0  
5. kivy                 1.11.1
 
ZIP FILE LINK(To download the required files as one whole file): 
 
P.S. : Do turn on your computer's speakers as there will sound effects in the game :)
 
## Overview of Game 

This is simple GUI Kivy-based game with state machine(libdw's SM class) integrated into it that is based on the classical game, hangman. In here, users will have to guess a word based on the hint displayed within the game with three tries and will either be brought to a  feedback screen that tells them that they either lose or win accompanied with sound effects. In each try, the screen will reflect different changes to the hangman progressively, with the start of a single bar followed by the head and the body with each being tagged to a state in the state machine in the code. (Refer to state machine flowchart pdf for clearer representation)
 
## Explanation of code 
 
1. kv file : The .kv file acts as a 'CSS' like template for the Kivy App Instance to build upon where you can easily organize and add widgets and its attributes. In this .kv, we first create a screen manager class and its three screen classes(game window, win window and lose window) for the <Main Window> class. Then we create the <MainGame>, <YouWin>, <YouLose> classes and start filling each window up with the required layout which is BoxLayout and widgets within the BoxLayout such as AsyncImage(allows images to be changed as required), Button, TextInput and link to functions from widgets like Buttons in the .py file. It also allows easy tagging of widgets with the use of ids such that they can be easily referred to in .py file as or when is needed.
  
2. The .py file will hold the 'logic' code for the game to run smoothly. This code will be explained by parts as shown below:
 
Lines 1-7:  
To import required libraries like random module, kivy classes, libdw's SM class. 
```python   
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from libdw import sm
import random  
``` 
Lines 10-16:  
Provides the word bank of guesses for app to randomly generate out for player to guess. 

```python 
bag_of_words = {'cotton': 'c _ t_ _ _', 'magnet': 'm _ _ m _ _ ', 'ghost': 'g _ o _ _',
                'poodle': '_ o _ _ l _', 'exodus': '_ x _ _  u _', 'sphinx': 's _ h _ _ _',
                'scratch': 's _ _ a _ _ _', 'vodka': 'v _ _ _ a', 'zombie': '_ o _ b _ _'
                }
references = ['cotton', 'magnet', 'ghost', 'poodle', 'exodus', 'sphinx', 'scratch', 'vodka', 'zombie']
answer = references[random.randint(0, len(references)-1)]  #sets randomized answer to guess in game
thehint = bag_of_words[answer]                  #provides hint to user match to answer variable 
``` 
Line 20:   
This line will load the .kv file for the kivy App Instance to build upon. 

```python  
Builder.load_file('MainApp.kv')    #loads the kv file for usage
```
Line 23 to 94: 
This part will create the MainGame class.  
In here, the initialization part, which inherits from BoxLayout and sm.SM, will include the start state which is set to initial state 0, 
loading the required sound effects for wrong and correct guesses, as well as setting callbacks to the function init_ui for the game to constantly reflect the correct hint to be reflected to the user.  
The get_next_values function inherited from the sm.SM class will help the game transit into different transitions like changing the different states of the hangman and providing the sound effects as players input guesses, and checks with the answer that is located at a global level. If the answer is correct, it will reset the hint and answer at the global level.
The validate function will be activated when player presses the check button in the game. If there is no input in the textbox, nothing will happen as we cannot have a NoneType input into the step function which will in turn call the get_next_values as this will produce error. If there is input, it will be eventually translated into the get_next_values function through the step function and the output will be current screen that the game is suppose to show depending on what the state machine generates. After every guess, it automatically blanks out the textbox so players can key in guesses at a blank state. 

```python 
class MainGame(BoxLayout, sm.SM):  #maingame class
    def __init__(self, **kwargs):                    #set state of game at 0 (image w/ bar), with 1 as image w/ bar+head
        super(MainGame, self).__init__(**kwargs)     # and 2 as image w/ bar+head+body
        Clock.schedule_interval(self.init_ui, 0)     #used such that the hint can be initialized at the start
        self.state = 0
        self.correct = SoundLoader.load('correct_ans.mp3')  # loads the correct sound effect
        self.wrong = SoundLoader.load('wrong_ans.mp3')     #loads the wrong sound effect

    def init_ui(self, dt=0):
        global thehint                              #provides access to thehint variable at global level
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
```  

Line 98 to 102: 
Creates the YouLose and YouWin class, which in turn is linked to the .kv file.  

```python
class YouLose(BoxLayout):
    pass

class YouWin(BoxLayout):
    pass 
```  

Line 104 to 117: 
Creates the MainWindow class, which is linked in the to the .kv file. Linking the game screen to MainGame class, win screen to the YouWin class and lose screen to the YouLose class and adding them to the screen manager, as indicated in the .kv file for the <MainWindow> class through the add_widget function with the help of ids.   
 
```python 
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
```

Line 119 to 124:  
Creates the MainApp class and inherit the kivy's App class and instantiates the MainWindow class when .py is being run.
  
```python
class MainApp(App):
    def build(self):
        return MainWindow()

if __name__=='__main__':
    MainApp().run() 
```
