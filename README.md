# Thank you for checking this out!
OSRS has been my training ground for learning and mastering Python. This project exemplifies my experience with Python. Very little AI was used in the creation of this code! Experience, documentation, and help from these Youtube channels: Arjan Code and Corey Schaffer.

**This script is tailored to run on X11 Linux.**

&nbsp;

# runelite_library
This library serves as a base toolset for automating tasks around OSRS. I will highlight objects or take screenshots of items around the game to interact with. Using the ComputerVision library, I find coordinates of matched objects or colors in specific parts of the screen. These coordinates feed into Pyautogui for mouse movement and clicking.

## &nbsp; window_management
First of all, I needed to find and activate the RuneLite window. When capturing screenshots, it either captures the whole client or specific areas of the client. This gives me granular control over where I'm looking for specific colors or objects, especially if multiple exist on the screen.

## &nbsp; interact
The primary way of interacting with the game will be through click(). Since I could ask it to look for either a color (r,g,b) or match an image (filepath to image) I made this flexible to accept both as an input. 

## &nbsp; database
Tying into a Postgresql database is a new skill I added to this project. SQLAlchemy and a FastAPI backend brought this project together.

&nbsp; 

# main.py
You will not have success with running this script as-is! I have my object and tile markers specifically placed and it doesn't feel right to share it. 

Should you desire to use this project, don't! I've had several banned accounts using this methodology, but the journey has always been centered around gaining experience with Python.
