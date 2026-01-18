import win32api, win32con
import time
def gridRegionsToGroupSets(grid_regions):
    """
    Group sets are in the form (column,row)... -> colour
    """
    group_sets = [set() for _ in range(len(grid_regions))]

    for i in range(len(grid_regions)):
        for j in range(len(grid_regions[0])):
            group_sets[grid_regions[i][j]].add((j,i))
    return group_sets


def solve(group_sets):
    """Recursive auxiliary function that brute-forces the solution.

    This function takes the first coloured group and tries to place a queen on each
    position of that group, then removes all positions from the following groups that
    would clash with this queen, and then tries to solve the remainder of the puzzle
    recursively by ignoring the first coloured group.

    If we reach an impossible position, the function returns None to indicate failure.
    Upon success, the function returns a list of all the positions where queens must go.
    """
    if not group_sets:
        return []

    # Try to put the next queen at all positions of the next group.
    for tx, ty in group_sets[0]:
        new_group_sets = [
            {
                (x, y)
                for x, y in gs
                if (
                    x != tx  # Can't be in the same column.
                    and y != ty  # Can't be in the same row.
                    and abs(x - tx) + abs(y - ty) > 2  # Can't touch.
                )
            }
            for gs in group_sets[1:]
        ]
        if not all(new_group_sets):  # 1+ empty group sets, skip this attempt.
            continue

        result = solve(new_group_sets)
        if result is not None:
            return [(tx, ty)] + result

def complete_board(coords):
    for (x,y) in coords:
        # If you want to slow down the clicks, adjust the sleep duration below
        time.sleep(0.25)
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    