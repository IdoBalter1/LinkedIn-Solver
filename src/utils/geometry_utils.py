import numpy as np

def line_intersection(line1,line2):
    x1,y1,x2,y2 = line1[0]
    x3,y3,x4,y4 = line2[0]
    d1 = (x2 - x1, y2 - y1)
    d2 = (x4 - x3, y4 - y3)
    denom = d1[0] * d2[1] - d1[1] * d2[0]
     
    if abs(denom) < 1e-10:
        return False
    t = ((x3 - x1) * d2[1] - (y3 - y1) * d2[0]) / denom
    s = ((x3 - x1) * d1[1] - (y3 - y1) * d1[0]) / denom
    
    # Check if intersection is within both line segments
    if 0 <= t <= 1 and 0 <= s <= 1:
       return True
    return False


def count_intersections(line, lines):
    count = 0
    for line_ in lines:
        if np.array_equal(line_[0],line[0]):
            print('here')
            continue
        if line_intersection(line,line_):
            count +=1
    return count

def get_valid_lines(img,lines):
    horizontal_lines = []
    vertical_lines = []

    for line in lines:
        x1, y1, x2, y2 = line[0]
        
        # Calculate angle
        dx = x2 - x1
        dy = y2 - y1
        angle = np.arctan2(abs(dy), abs(dx)) * 180 / np.pi
        
        # Filter by angle
        if angle < 5:  # Horizontal (approximately 0°)
            horizontal_lines.append(line)
        elif angle > 85:  # Vertical (approximately 90°)
            vertical_lines.append(line)

    return horizontal_lines, vertical_lines

def cell_size(valid_hlines,valid_vlines):
    xs = []
    for line in valid_vlines:
        x1, y1, x2, y2 = line[0]
        xs.append(min(x1, x2))  # Use minimum x (leftmost)
    xs = sorted(xs)
    
    # For horizontal lines: get y-coordinate (both y1 and y2 should be same, but use min to be safe)
    ys = []
    for line in valid_hlines:
        x1, y1, x2, y2 = line[0]
        ys.append(min(y1, y2))  # Use minimum y (topmost)
    ys = sorted(ys)
    
    originalx = xs[0]
    originaly = ys[0]
    dx= 0
    dy =0
    count = 0
    for x,y  in zip(xs[1:],ys[1:]):
        dx += x - originalx
        dy += y - originaly
        originaly = y
        originalx = x
        count +=1
    dx /= count
    dy /= count
    return dx,dy, xs,ys

def extract_grid_coords(dx, dy, xs, ys):
    """
    Given cell size dx, dy, and grid line positions xs, ys,
    calculate and return the (x, y) center positions of each cell center
    as a (len(ys)+1) x (len(xs)+1) 2D list.
    """
    coords = [[None for _ in range(len(xs) + 1)] for _ in range(len(ys) + 1)]
    topleft = [min(xs) - (dx / 2), min(ys) - (dy / 2)]
    for i in range(len(ys) + 1):
        for j in range(len(xs) + 1):
            coords[i][j] = [topleft[0] + j * dx, topleft[1] + i * dy]
    
 
    return coords

