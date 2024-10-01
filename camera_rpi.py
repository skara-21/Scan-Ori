import cv2
import numpy as np
import os
import time
from picamera2 import Picamera2
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.IN)
GPIO.output(11,GPIO.LOW)
page=1

def pic_take():
    picam2.start()
    time.sleep(3)
    picam2.capture_file(os.path.join('Book','img.jpg'))
    picam2.stop()
    return os.path.join('Book','img.jpg')


def cut_image(image_path):
    image=cv2.imread(image_path)
    # Define the starting point (x, y) and the size (width, height)
    start_x = 324
    start_y = 109
    width = 1270
    height = 810

    # Cut the rectangular region from the image
    cropped_image = image[start_y:start_y + height, start_x:start_x + width]
    
    # Save or display the cropped image
    path='Book/'+f'page_{page}.jpg'
    cv2.imwrite(path, cropped_image)
    os.remove(image_path)
    return os.path.join('Book',f'page_{page}.jpg')

def detect_book_edges(image_path):
    # Step 1: Load the image
    image = cv2.imread(image_path)
    
    # Step 2: Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Step 3: Apply adaptive thresholding to separate the book from the background
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)
    
    # Step 4: Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Step 5: Draw contours on the original image (optional)
    contours_image = image.copy()
    cv2.drawContours(contours_image, contours, -1, (0, 255, 0), 2)  # Draw in green
    
    # Step 6: Show the detected contours
    #cv2.imshow('Detected Book Edges', contours_image)
    
    # Step 7: Find the largest contour (assuming it's the book)
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Step 8: Draw the bounding box around the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)
    #cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw rectangle in blue
    
    # Step 9: Crop the region of the book using the bounding box coordinates
    cropped_book = image[y:y+h, x:x+w]
    
    # Step 10: Show the cropped book image
    #cv2.imshow('Cropped Book', cropped_book)
    
    # Step 11: Save the cropped image (optional)
    cv2.imwrite('cropped_book2.jpg', cropped_book)
    
    # Show final result with bounding box
    #cv2.imshow('Detected Book with Bounding Box', image)
    
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (1920, 1080)})
picam2.configure(config)
if not os.path.exists('Book'):
    os.mkdir('Book')

try:
    while True:
        GPIO.output(11,GPIO.HIGH)
        while not GPIO.input(13):
            sleep(0.01)
        else:
            GPIO.output(11,GPIO.LOW)
            sleep(0.5)
            image_path=pic_take()
            new_path=cut_image(image_path)
            page+=1
            #detect_book_edges(new_path)
            sleep(0.01)
        sleep(0.01)
except KeyboardInterrupt:
    GPIO.output(11,GPIO.LOW)
    GPIO.cleanup()