import mss
import cv2
import pyautogui
import time
import numpy as np
import keyboard


def take_screenshot():
	with mss.mss() as sct:
		filename = sct.shot(output='fullscreen.png')
	return filename

def get_frame(region):
	with mss.mss() as sct:
		screen = np.asarray(sct.grab(region))
		screen_grayscale = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
		# print(screen_grayscale.shape)
		# cv2.imwrite("region_dino_chrome.png", screen_grayscale)
	return screen_grayscale

def print_lines(region):
	with mss.mss() as sct:
		full_screen = {"top": 0, "left":0, "width": 1366, "height": 768}
		screen = np.asarray(sct.grab(full_screen))
		screen_grayscale = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
		for i in [region['top'], region['top'] + 70]:
			for j in range(region['left'], region['left'] + region['width']):
				screen_grayscale[i,j] = 130
	cv2.imwrite("region_on_screen.png", screen_grayscale)

def collision_detected(frame):
		for x in [0,39]:
			if len(set(frame[x])) > 2:
				return True
		return False


region = {
	"top":320,
	"left":95,
	"width":150,
	"height":40,
}

# take_screenshot()
#frame = get_frame(region)
# print_lines(frame)

while True:
	# if keyboard.is_pressed('q'):
		# break
	start_time = time.time()
	frame = get_frame(region)
	if collision_detected(frame):
		pyautogui.keyDown('space')
	print("%d FPS" % (1/(time.time() - start_time)))