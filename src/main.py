import cv2 as cv
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import time

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
import argparse
# from PIL import Image

# This overrides Qt's silly trapping of Ctrl-C,
# so you don't have to Ctrl-\ and get a core dump every time.
from PyQt5 import QtCore, QtGui, QtWidgets
import signal
import sys
from utils import (
    line_intersection,
    get_valid_lines,
    cell_size,
    extract_grid_coords,
    mapNumbers,
    create_colored_grid,
    count_intersections,
    answer_to_grid,
    plot_lines,
    zoom,
    plotColouredGrid,
)

from queenSolver import(
    gridRegionsToGroupSets,
    solve
) 

from boardDetector import(
    get_grid_lines,
    filter_lines,
    getGridColours

)

from transparentwindow import TransWin

from inTime import BoardGrabber


if __name__ == '__main__':

    grabber = BoardGrabber()
    t,l,w,h = grabber.get_monitor_properties(1)
    max_attempts = 400
    attempt = 0
    while True:
        if attempt >= max_attempts:
            print("Reached maximum number of attempts without finding a valid grid.")
            break
        img = grabber.screenshotPart(0,0,w,h,1)

        lines = get_grid_lines(img,minLineLength = 300, maxLineGap = 10)
        if len(lines) == 0:
            attempt +=1
            continue
        h_lines,v_lines = get_valid_lines(img,lines)
        if len(h_lines)== 0 or len(v_lines)== 0:
            attempt +=1
            continue
        valid_hlines,valid_vlines = filter_lines(h_lines,v_lines)
        print(len(valid_hlines),len(valid_vlines))
        if len(valid_hlines) == len(valid_vlines) and len(valid_hlines) > 1:
            break
        attempt += 1
        

    plot_lines(img,h_lines,v_lines)
    plot_lines(img,valid_hlines,valid_vlines)
    
    dx,dy,xs,ys = cell_size(valid_hlines,valid_vlines)
    coords = extract_grid_coords(dx,dy,xs,ys)
    zoomed, min_x, min_y, max_x,max_y = zoom(coords,img,dx,dy)
    grid_regions = getGridColours(zoomed,coords,min_x,min_y)
    mapped_regions = mapNumbers(grid_regions)

    group_sets = gridRegionsToGroupSets(mapped_regions)

    answer = solve(group_sets)

    answer_to_grid(answer,coords,img)
    temp_path = 'solution_overlay.png'
    cv.imwrite(temp_path,zoomed)



    # Create colored grid
    colored_grid = create_colored_grid(grid_regions)
    plotColouredGrid(zoomed,grid_regions,colored_grid)


    topleftg = [coords[0][0][0] - dx, coords[0][0][1] - dy]
    toprightg = [coords[0][-1][0] + dx, coords[0][-1][1] - dy]
    bottomleftg = [coords[-1][0][0] - dx, coords[-1][0][1] + dy]
    bottomrightg = [coords[-1][-1][0] + dx, coords[-1][-1][1] + dy]

        
    # parser = argparse.ArgumentParser(
    #     description="Show an image transparently, with click-through")
    # parser.add_argument('imgfile', help='Image to show')
    # parser.add_argument('-p', '--position', nargs=2, type=int,
    #                     default=topleftg, help="Window position")
    # parser.add_argument('-o', '--opacity', type=int, default=50,
    #                     help='opacity (percent: default 50)')
    # args = parser.parse_args(sys.argv[1:])

    app = QApplication(sys.argv)
    window = TransWin(temp_path,
                      position=[int(topleftg[0]),int(topleftg[1])], opacity=50)
    window.show()
    import os
    if os.path.exists(temp_path):
        os.remove(temp_path)
    sys.exit(app.exec_())
    






    
