import numpy as np
def zoom(coords,img,dx,dy):
    topleftg = [coords[0][0][0] - dx, coords[0][0][1] - dy]
    toprightg = [coords[0][-1][0] + dx, coords[0][-1][1] - dy]
    bottomleftg = [coords[-1][0][0] - dx, coords[-1][0][1] + dy]
    bottomrightg = [coords[-1][-1][0] + dx, coords[-1][-1][1] + dy]
    min_x = int(min(topleftg[0], toprightg[0], bottomleftg[0], bottomrightg[0]))
    max_x = int(max(topleftg[0], toprightg[0], bottomleftg[0], bottomrightg[0]))
    min_y = int(min(topleftg[1], toprightg[1], bottomleftg[1], bottomrightg[1]))
    max_y = int(max(topleftg[1], toprightg[1], bottomleftg[1], bottomrightg[1]))
    # Ensure the ROI is within the image bounds:
    min_x = max(min_x, 0)
    min_y = max(min_y, 0)
    max_x = min(max_x, img.shape[1])
    max_y = min(max_y, img.shape[0])
    new_image = img[min_y:max_y, min_x:max_x] 
    return new_image, min_x, min_y, max_x,max_y

def mapNumbers(grid_regions):
    unique_numbers = np.unique(grid_regions)

    new_ids = {old_id : new_id for new_id,old_id in enumerate(unique_numbers)}

    for i in range(len(grid_regions)):
        for j in range(len(grid_regions)):
            grid_regions[i][j] = new_ids[grid_regions[i][j]]
    return grid_regions