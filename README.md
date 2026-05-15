# Thank you for checking this out!
OSRS has been my training ground for learning and mastering Python. This project has gone through many iterations, but before I take this further I need to share it with the world for constructive feedback.

It started off as a vibe-coded project. I still ask ChatGPT for advice, but I'm noticing it has severe limitations (which I consider as a sign of growth).

**This script is tailored to run on Rocky Linux.**

Finally, you'll find the history of this project and get an understanding of where it is headed by checking out my other repository, [*OldSchoolRS-CV2*](https://github.com/RobbyTee/OldSchoolRS-CV2). OSRS-NewSchool aims to be the final iteration of this toolset by applying everything I've learned.

&nbsp;

# runelite_library
This library serves as a base toolset for automating tasks around OSRS. I will highlight objects or take screenshots of items around the game to interact with. Using the ComputerVision library, I find coordinates of matched objects or colors in specific parts of the screen. These coordinates feed into Pyautogui for mouse movement and clicking.

## &nbsp; window_management
First of all, I needed to find and activate the RuneLite window. When capturing screenshots, it either captures the whole client or specific areas of the client. This gives me granular control over where I'm looking for specific colors or objects, especially if multiple exist on the screen.

## &nbsp; interact
The primary way of interacting with the game will be through click(). Since I could ask it to look for either a color (r,g,b) or match an image (filepath to image) I made this flexible to accept both as an input. 

I've made several auxilliary functions to handle specific, repetitive tasks.

## &nbsp; rune_logger
I'm still not certain on when / what to log. Typically I'll put in a log entry if I have a particularly stubborn or inconsistent function. I'll use more logging when I build out the actual tasks.

&nbsp; 

# main.py
An example of how these pieces will fit together in a task. Please check out [*OldSchoolRS-CV2*](https://github.com/RobbyTee/OldSchoolRS-CV2) *tasks* folder for the future potential of this toolset.
