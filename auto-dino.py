import mss
import cv2
import pyautogui
import time
import numpy as np
import keyboard

# first let's take a full screenshot
def take_screenshot():
	with mss.mss() as sct:
		filename = sct.shot(output='fullscreen.png')
	return filename

# Now we need to first determine what is the region we want to jump when OpenCV detects any obstacles
# This is a little bit tricky, because there are other obstacles in the background and you need to specify the exact location of the 
# obstacles that have hit box.

def get_frame(region):
	with mss.mss() as sct:
		screen = np.asarray(sct.grab(region))
		screen_grayscale = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
		# print(screen_grayscale.shape)
		# cv2.imwrite("region_dino_chrome.png", screen_grayscale)
	return screen_grayscale
# In this function we need to draw two lines. First we need the region and then we draw to test if we are jumping in the range of both 
# Birds and Fences.
def print_lines(region):
	with mss.mss() as sct:
		full_screen = {"top": 0, "left":0, "width": 1366, "height": 768}
		screen = np.asarray(sct.grab(full_screen))
		screen_grayscale = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
		for i in [region['top'], region['top'] + 70]:
			for j in range(region['left'], region['left'] + region['width']):
				screen_grayscale[i,j] = 130
	cv2.imwrite("region_on_screen.png", screen_grayscale)
	

# Well, this simple function does the main Jumping part.
# If we have more than 5 different colors, we press the jump button
def collision_detected(frame):
		for x in [0,39]:
			if len(set(frame[x])) > 5:
				return True
		return False


# This is our region. You have to find it by using a simple drawing application. Paint in Windows, GIMP in GNU/Linux
region = {
	"top":320,
	"left":95,
	"width":150,
	"height":40,
}

# The following parts are the first steps of the program. You need to take a screen shot and then get the frame.
# Later on, in next steps, you have to print lines using the third statement.
"""
take_screenshot()
frame = get_frame(region)
print_lines(frame)
"""

# Unlimited loop, first if is wheter you need to quit your program by pressing Q on your keyboard.
# Time functions here help us calculate the start time and the end time for showing FPS.
while True:
	if keyboard.is_pressed('q'):
		break
	start_time = time.time()
	frame = get_frame(region)
	if collision_detected(frame):
		pyautogui.keyDown('space')
	print("%d FPS" % (1/(time.time() - start_time)))
