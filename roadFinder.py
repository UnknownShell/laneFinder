import numpy as np
from PIL import ImageGrab
import cv2
import time

def draw_lines(img, lines): # Line function
    try:
        for line in lines: # Loops through all lines
            coords = line[0] # Sets up coords to be used to draw lines
            cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 255, 255], 3) # Draws lines on img using coords
    except:
        pass

def roi(img, vertices): # ROI
    mask = np.zeros_like(img) # Blank mask 
    cv2.fillPoly(mask, vertices, 255) # Fill mask using vertices
    masked = cv2.bitwise_and(img, mask) # ROI is left
    return masked # returns masked img to function

def process_img(original_image): # Defines process_img function
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY) # BGR to Grayscale
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300) # Edgy detection
    processed_img = cv2.GaussianBlur(processed_img, (5,5), 0) # Blurs so lines arent so jagged
    vertices = np.array([[10, 500], [10, 300], [300, 200], [500, 200], [800, 300], [800, 500]]) # Defines ROI
    processed_img = roi(processed_img, [vertices]) # ROI Function
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]), 150, 10) # Feeding Canny Edgy Detection to HoughLines
    draw_lines(processed_img, lines)
    return processed_img # returns processed_img for function

def main(): # main function
    last_time = time.time() # sets last time before loop
    while(True):
        screen = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(0,40,800,640))), cv2.COLOR_BGR2RGB) # Screen Grab
        new_screen = process_img(screen) # Processed Screen

        print('Loop took {} seconds'.format(time.time()-last_time)) # Speed Test
        last_time = time.time() # Set last time for Speed Test

        cv2.imshow("Bot View", new_screen) # Show Processed Screen

        if cv2.waitKey(5) & 0xFF == ord('q'): # On key press 'q'
            cv2.destroyAllWindows() # destroy windows
            break # break while loop

main() # Calls main

