import cv2 as cv
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import sys

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
import argparse
# from PIL import Image

# This overrides Qt's silly trapping of Ctrl-C,
# so you don't have to Ctrl-\ and get a core dump every time.
from PyQt5 import QtCore, QtGui, QtWidgets
import signal
from utils import (
    line_intersection,
    get_valid_lines,
    cell_size,
    extract_grid_coords,
    mapNumbers,
    create_colored_grid,
    count_intersections,
    answer_to_grid
)

from queenSolver import(
    gridRegionsToGroupSets,
    solve
) 
from transparentwindow import TransWin


filter = True
img_path = Path("../images/screenshot2full.png" )
img = cv.imread(img_path)

def get_grid_lines(img,minLineLength = 300,maxLineGap = 10):
    
    #img = img[200:660,600:1200]
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray,0,150)
    # Resize and show 'cannyedges' in a smaller window with same aspect ratio
    display_scale = 0.7  # 50% of original, adjust as needed
    cannyedges_small = cv.resize(edges, (0, 0), fx=display_scale, fy=display_scale)

    #cv.imshow('cannyedges', cannyedges_small)

    kernel = np.ones((3,3),np.uint8)
    edges = cv.dilate(edges,kernel,iterations = 1)
    kernel = np.ones((5,5),np.uint8)
    edges = cv.erode(edges,kernel,iterations = 1)
    #cv.imwrite('canny.jpg',edges)

    # Resize and show 'edges' in a smaller window with same aspect ratio
    # edges_small = cv.resize(edges, (0, 0), fx=display_scale, fy=display_scale)
    #cv.imshow('edges', edges_small)
    # HoughLinesP returns line segments with endpoints
    lines = cv.HoughLinesP(edges, 1, np.pi/180, threshold=100,
                        minLineLength=minLineLength, maxLineGap=maxLineGap)

    cv.waitKey(0)
    return lines





def filter_lines(horizontal_lines, vertical_lines):
    valid_hlines = []
    for line in (horizontal_lines):
        count = count_intersections(line,vertical_lines)
        if count >= len(vertical_lines)//2 + 1:
            valid_hlines.append(line)
    valid_vlines = []
    for line in (vertical_lines):
        count = count_intersections(line,horizontal_lines)
        #print(count)
        
        if count >= len(horizontal_lines)//2 + 1:
            valid_vlines.append(line)
    return valid_hlines,valid_vlines

    

def getGridColours(new_image,coords,min_x,min_y):
    gray = cv.cvtColor(new_image,cv.COLOR_BGR2GRAY)
    #cv.imshow('gray',gray)

    blur = cv.GaussianBlur(gray,(13,13),cv.BORDER_DEFAULT) 
    #cv.imshow('blur',blur)
    
    canny = cv.Canny(blur,20,80) 
    #cv.imshow('canny',canny)
    
    # Close gaps in borders before inverting
    kernel = np.ones((31, 31), np.uint8)
    closed_borders = cv.morphologyEx(canny, cv.MORPH_CLOSE, kernel)

    #cv.imshow('borders',closed_borders)
    
    regions = 255 - closed_borders
    _, labels = cv.connectedComponents(regions)

    grid_regions = np.zeros((len(coords),len(coords)), dtype=np.int32)

    for i in range(len(coords)):
        for j in range(len(coords)):
            x,y = int(coords[i][j][0]) - min_x,int(coords[i][j][1])-min_y
            region_id = labels[y,x]
            grid_regions[i,j] = region_id

    return grid_regions




    




        
        
        
        
        
