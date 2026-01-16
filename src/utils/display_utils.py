import cv2 as cv
import numpy as np



def plot_lines(img,horizontal_lines, vertical_lines):
    img_with_lines = img.copy()

    # Draw horizontal lines in green
    for line in horizontal_lines:
        x1, y1, x2, y2 = line[0]
        cv.line(img_with_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green

    # Draw vertical lines in red
    for line in vertical_lines:
        x1, y1, x2, y2 = line[0]
        cv.line(img_with_lines, (x1, y1), (x2, y2), (0, 0, 255), 2) 

    #cv.imshow('Filtered Lines', img_with_lines)

    #cv.waitKey(0)
    #cv.destroyAllWindows()

def create_colored_grid(grid_regions):
    """
    Create a colored image where each unique region ID gets a different color
    """
    rows, cols = grid_regions.shape
    
    # Create color map for unique region IDs
    unique_ids = np.unique(grid_regions)
    num_regions = len(unique_ids)
    
    # Generate distinct colors for each region ID
    # Using HSV color space for better color distribution
    colored_grid = np.zeros((rows, cols, 3), dtype=np.uint8)
    
    for idx, region_id in enumerate(unique_ids):
        # Create distinct colors using HSV
        hue = int(180 * idx / max(num_regions, 1))  # Hue from 0-180 (OpenCV uses 0-180)
        color_bgr = cv.cvtColor(np.uint8([[[hue, 255, 255]]]), cv.COLOR_HSV2BGR)[0][0]
        
        # Set all cells with this region_id to this color
        mask = (grid_regions == region_id)
        colored_grid[mask] = color_bgr
    
    return colored_grid

def plotColouredGrid(zoomed,grid_regions,colored_grid):
    
    cell_height = zoomed.shape[0] // grid_regions.shape[0]
    cell_width = zoomed.shape[1] // grid_regions.shape[1]

    # Scale up the colored grid to match image size
    colored_grid_large = cv.resize(colored_grid, 
                                    (zoomed.shape[1], zoomed.shape[0]), 
                                    interpolation=cv.INTER_NEAREST)  # Use nearest to keep sharp edges

    # Create side-by-side visualization
    combined = np.hstack([zoomed, colored_grid_large])

    # Display images
    #cv.imshow('Original Grid', zoomed)
    #cv.imshow('Colored Regions', colored_grid_large)
    #cv.imshow('Side by Side: Original | Colored Regions', combined)




    #cv.waitKey(0)
    #cv.destroyAllWindows()

def answer_to_grid(answer, coords, img, color=(0, 0, 255), radius=15, thickness=3):
    for (i, j) in answer:
        x, y = coords[j][i]
        center = (int(x), int(y))
        cv.circle(img, center, radius, color, thickness)
    return img


        


