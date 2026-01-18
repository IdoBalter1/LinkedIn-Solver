# LinkedIn-Solver

An automated computer vision solution for detecting and solving Queens puzzles from LinkedIn images. The application captures screenshots, detects the game board, identifies colored regions, solves the puzzle, and displays the solution as a transparent overlay on your screen.

## Features

- **Live Screenshot Capture**: Automatically captures screenshots from your monitor
- **Board Detection**: Uses OpenCV to detect grid lines and extract the game board
- **Region Identification**: Identifies colored regions using connected components analysis
- **Puzzle Solving**: Solves the N-Queens puzzle with region constraints
- **Transparent Overlay**: Displays the solution as a click-through transparent window overlay

## Requirements

- Python 3.8+
- Windows (for transparent overlay functionality)
- `uv` package manager (recommended) or `pip`

## Installation

### Using `uv` (Recommended)

1. Install `uv` if you haven't already:
   ```bash
   pip install uv
   ```

2. Install dependencies:
   ```bash
   uv pip install opencv-python opencv-stubs PyQt5 mss numpy matplotlib
   ```

### Using `pip`

```bash
pip install opencv-python opencv-stubs PyQt5 mss numpy matplotlib
```

## Usage

1. Navigate to the `src` directory:
   ```bash
   cd src
   ```

2. Run the main script:
   ```bash
   python main.py
   ```

3. The application will:
   - Capture a screenshot of your primary monitor
   - Detect the game board grid
   - Identify colored regions
   - Solve the puzzle
   - Display the solution as a transparent overlay

4. The overlay window will appear on your screen showing where to place the queens. You can interact with your screen normally as clicks pass through the overlay.

5. Press 'q' in the overlay window to quit (if keyboard input is enabled).

## How It Works

### 1. Screenshot Capture (`inTime.py`)
- Uses the `mss` library to capture screenshots
- Supports multi-monitor setups
- Converts screenshots directly to OpenCV format (BGR)

### 2. Board Detection (`boardDetector.py`)
- **Edge Detection**: Uses Canny edge detection to find grid lines
- **Line Detection**: Uses HoughLinesP to detect horizontal and vertical lines
- **Line Filtering**: Filters lines based on intersection counts to identify valid grid lines
- **Grid Extraction**: Calculates cell coordinates and extracts the board region

### 3. Region Identification (`boardDetector.py`)
- Applies morphological operations to close gaps in borders
- Uses `cv.connectedComponents` to identify distinct colored regions
- Maps each grid cell to its corresponding region ID

### 4. Puzzle Solving (`queenSolver.py`)
- Converts grid regions to group sets (each color group)
- Uses recursive backtracking to solve the N-Queens problem
- Ensures queens don't attack each other and respects region constraints

### 5. Solution Display (`transparentwindow.py`)
- Creates a transparent PyQt5 window
- Uses Windows API to enable click-through functionality
- Overlays the solution directly on your screen

## Project Structure

```
LinkedIn-Solver/
├── src/
│   ├── main.py                 # Main entry point
│   ├── boardDetector.py        # Board detection and grid extraction
│   ├── queenSolver.py          # Puzzle solving logic
│   ├── transparentwindow.py   # Transparent overlay window
│   ├── inTime.py               # Screenshot capture functionality
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       ├── geometry_utils.py    # Line intersection, grid calculations
│       ├── image_utils.py       # Image processing utilities
│       └── display_utils.py     # Visualization functions
├── images/                      # Sample images (optional)
└── README.md
```

## Key Components

### `main.py`
- Orchestrates the entire workflow
- Handles retry logic for grid detection
- Creates and displays the transparent overlay

### `boardDetector.py`
- `get_grid_lines()`: Detects grid lines using HoughLinesP
- `filter_lines()`: Filters valid grid lines based on intersections
- `getGridColours()`: Identifies colored regions using connected components

### `queenSolver.py`
- `gridRegionsToGroupSets()`: Converts grid regions to color groups
- `solve()`: Recursive backtracking solver for N-Queens

### `transparentwindow.py`
- `TransWin`: PyQt5 window class with click-through transparency
- Uses Windows API (`WS_EX_TRANSPARENT`) for click-through functionality

## Troubleshooting

### Window Disappears on Click
- Ensure you're running on Windows (click-through uses Windows API)
- Check that `ctypes` is properly imported

### Grid Not Detected
- Adjust `minLineLength` and `maxLineGap` parameters in `get_grid_lines()`
- Ensure the board is clearly visible on your screen
- Try adjusting Canny edge detection thresholds

### Region Detection Issues
- Adjust morphological kernel sizes in `getGridColours()`
- Modify Canny thresholds for better border detection

## Notes

- The transparent overlay requires Windows for click-through functionality
- The application is designed for LinkedIn Queens puzzle images
- Grid detection may need parameter tuning for different board styles
- The overlay window stays on top and allows normal screen interaction

## License

This project is for educational purposes.




