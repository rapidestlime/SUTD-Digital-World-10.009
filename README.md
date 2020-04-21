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

 
P.S. : Do turn on your computer's speakers as there will sound effects in the game :)
 
## Overview of Game 

This is simple GUI Kivy-based game with state machine(libdw's SM class) integrated into it that is based on the classical game, hangman. In here, users will have to guess a word based on the hint displayed within the game with three tries and will either be brought to a  feedback screen that tells them that they either lose or win accompanied with sound effects. In each try, the screen will reflect different changes to the hangman progressively, with the start of a single bar followed by the head and the body with each being tagged to a state in the state machine in the code. 
 
## Explanation of code 
 
1. kv file : The .kv file acts as a 'CSS' like template for the Kivy App Instance to build upon where you can easily organize 
