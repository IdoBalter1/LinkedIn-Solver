import mss
import mss.tools
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
class BoardGrabber:
    def __init__(self):
        self.sct = mss.mss()
    
    def grab(self,screen):
        return self.sct.grab(screen)
    
    def screenshot(self):
        return self.sct.shot()

    def get_monitor_properties(self,monitor_number = 1):
        top = self.sct.monitors[monitor_number]['top']
        left =self.sct.monitors[monitor_number]['left']
        width = self.sct.monitors[monitor_number]['width']
        height = self.sct.monitors[monitor_number]['height']

        return top, left , width, height

    def screenshotPart(self,top,left,width,height,monitor_number = 1):
        mon = self.sct.monitors[monitor_number]
        monitor = {"top":mon['top'] + top, "left" : mon['left'] +left, "width" : width, "height": height}
        sct_image =  self.sct.grab(monitor)
        img_array = np.array(sct_image)
        img = cv.cvtColor(img_array,cv.COLOR_RGBA2RGB)
        # cv.imshow('image',img)
        # cv.waitKey(0)
        #mss.tools.to_png(sct_image.rgb,sct_image.size,output = f'screenshot{monitor_number}full.png')

        return img

    

image = Path("../images/linkedInqueens.png")

Grabber = BoardGrabber()
top,left, width, height = Grabber.get_monitor_properties(1)
#Grabber.screenshotPart(int(height/5.5),abs(left//4),width//2,height//2,2)
Grabber.screenshotPart(0,0,width,height,1)

    
    
    
        
