'''
SUBMITTED BY

SARTHAK CHANDNA 
102053037

GUNEEV KAUR
102003259

PROJECT DESCRIPTION:

************************************************  TEACH - SCREEN ***************************************************

OUR PROJECT HAS THE FOLLOWING FEATURES :

IT CONSISTS OF A TOOL BAR FROM WHICH THE USER CAN SELECT THE DESIRED TOOL FROM THE GIVEN OPTIONS: LINE, DRAW, RECTANGLE, CIRCLE AND ERASER.
THE USER CAN PERFORM THE FOLLOWING ACTION JUST BY CLOSING THE FIST AND ONLY OPENING THE INDEX FINGER OF THE HAND ON THE REQUIRED TOOL.
THIS SELECTS THE TOOL AND THEN MOVE THE INDEX FINGER TO THE DESIRED LOCATION ON THE SCREEN WHERE YOU WANT TO START DRAWING FROM. 
ON REACHING THAT LOCATION, OPEN THE OTHER FINGERS OF YOUR HAND AND RELEASE WHEN YOU'RE DONE WITH DRAWING THE SHAPE OF THE NECESSARY SIZE.


THE PROJECT CAN HAVE MULTIPLE USES IN THE INDUSTRY OF TEACHING, ESPECIALLY IN ONLINE TEACHING THAT CAN HELP THE STUDENTS LEARN IN 
A DIFFERENT AND AN INTERACTIVE WAY.



'''



#importing required libraries

import mediapipe as mp #Mediapipe Library:Provides customizable ML solutions for live and streaming media.
import cv2 #OpenCv Library: used to deal with images
import numpy as np #Numpy : Adds support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions
import time #Used to access real time.

#constant values
ml = 150
max_x, max_y = 250+ml, 50
curr_tool = "select tool"
time_init = True
rad = 40
var_inits = False
thick = 4
prevx, prevy = 0,0

#get tools function: to select the tool user wants to use.
def getTool(x):
	if x < 50 + ml:
		return "Line"

	elif x<100 + ml:
		return "Rectangle"

	elif x < 150 + ml:
		return "Draw"

	elif x<200 + ml:
		return "Circle"

	else:
		return "Eraser"

def index_raised(yi, y9):
	if (y9 - yi) > 40:
		return True

	return False


#detection of hand of the user
hands = mp.solutions.hands
hand_landmark = hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6, max_num_hands=1)
draw = mp.solutions.drawing_utils


# drawing tools
tools = cv2.imread("tools.png")
tools = tools.astype('uint8')

mask = np.ones((480, 640))*255
mask = mask.astype('uint8')

#Getting the real time information through the video camera, for example: hand gestures, movement detection,etc.
#This section contains the funtions to detect hand gestures of the user and to perform the necessary action by drawing the required tool on the screen.
cap = cv2.VideoCapture(0)
while True:
	_, frm = cap.read()
	frm = cv2.flip(frm, 1)

	rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)

	op = hand_landmark.process(rgb)

	if op.multi_hand_landmarks:
		for i in op.multi_hand_landmarks:
			draw.draw_landmarks(frm, i, hands.HAND_CONNECTIONS)
			x, y = int(i.landmark[8].x*640), int(i.landmark[8].y*480)

			if x < max_x and y < max_y and x > ml:
				if time_init:
					ctime = time.time()
					time_init = False
				ptime = time.time()

				cv2.circle(frm, (x, y), rad, (253, 174, 249), 2)
				rad -= 1

				if (ptime - ctime) > 0.8:
					curr_tool = getTool(x)
					print("Selected Tool : ", curr_tool)
					time_init = True
					rad = 40

			else:
				time_init = True
				rad = 40

			if curr_tool == "Draw":
				xi, yi = int(i.landmark[12].x*640), int(i.landmark[12].y*480)
				y9  = int(i.landmark[9].y*480)

				if index_raised(yi, y9):
					cv2.line(mask, (prevx, prevy), (x, y), 0, thick)
					prevx, prevy = x, y

				else:
					prevx = x
					prevy = y



			elif curr_tool == "Line":
				xi, yi = int(i.landmark[12].x*640), int(i.landmark[12].y*480)
				y9  = int(i.landmark[9].y*480)

				if index_raised(yi, y9):
					if not(var_inits):
						xii, yii = x, y
						var_inits = True

					cv2.line(frm, (xii, yii), (x, y), (253, 174, 249), thick)

				else:
					if var_inits:
						cv2.line(mask, (xii, yii), (x, y), 0, thick)
						var_inits = False

			elif curr_tool == "Rectangle":
				xi, yi = int(i.landmark[12].x*640), int(i.landmark[12].y*480)
				y9  = int(i.landmark[9].y*480)

				if index_raised(yi, y9):
					if not(var_inits):
						xii, yii = x, y
						var_inits = True

					cv2.rectangle(frm, (xii, yii), (x, y), (253, 174, 249), thick)

				else:
					if var_inits:
						cv2.rectangle(mask, (xii, yii), (x, y), 0, thick)
						var_inits = False

			elif curr_tool == "Circle":
				xi, yi = int(i.landmark[12].x*640), int(i.landmark[12].y*480)
				y9  = int(i.landmark[9].y*480)

				if index_raised(yi, y9):
					if not(var_inits):
						xii, yii = x, y
						var_inits = True

					cv2.circle(frm, (xii, yii), int(((xii-x)**2 + (yii-y)**2)**0.5), (253, 174, 249), thick)

				else:
					if var_inits:
						cv2.circle(mask, (xii, yii), int(((xii-x)**2 + (yii-y)**2)**0.5), (0,255,0), thick)
						var_inits = False

			elif curr_tool == "Eraser":
				xi, yi = int(i.landmark[12].x*640), int(i.landmark[12].y*480)
				y9  = int(i.landmark[9].y*480)

				if index_raised(yi, y9):
					cv2.circle(frm, (x, y), 30, (0,0,0), -1)
					cv2.circle(mask, (x, y), 30, 255, -1)



	op = cv2.bitwise_and(frm, frm, mask=mask)
	frm[:, :, 1] = op[:, :, 1]
	frm[:, :, 2] = op[:, :, 2]

	frm[:max_y, ml:max_x] = cv2.addWeighted(tools, 0.7, frm[:max_y, ml:max_x], 0.3, 0)

	cv2.putText(frm, curr_tool, (270+ml,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
	cv2.imshow("TEACH-SCREEN", frm) #Captioning the Teach Screen

#The teach screen will be displayed on the user's screen.
	if cv2.waitKey(1) == 27:
		cv2.destroyAllWindows()
		cap.release()
		break
 