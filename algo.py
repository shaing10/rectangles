import numpy as np
import itertools


def center_in_rect(center_x, center_Y, rect):
    x1, y1, x2, y2 = rect[0][0], rect[1][0], rect[0][1], rect[1][1]
    x, y = center_x, center_Y
    if x1 < x < x2:
        if y1 < y < y2:
            return True
    return False


def fill_rect(R, rects):
    """
    :param R: 2s array - [x coords, y coords]. size(R) = [1,2,2]
    :param rects: 3d array - ([rect_num, x coords, y coords]). size(rects) = [N,2,2]
    :return:
        potential_rects: 3d array - ([new_rect_num, new_x coords, new_y coords]). size(filled_rects) = [M,2,2]
    """
    N = rects.shape[0]
    x1, x2, y1, y2 = np.reshape(np.ravel(rects), [4, rects.shape[0]], 'F')
    all_x = np.sort(np.concatenate((x1, x2)))
    all_y = np.sort(np.concatenate((y1, y2)))
    print(f"all_x= {all_x}, all y={all_y}")
    # add new rectangles that have a common edge(s) with R
    potential_rects = np.array([[[R[0][0], all_x[0]], [R[1][0], R[1][1]]],  # left new_rect
                                [[all_x[0], all_x[-1]], [all_y[-1], R[1][1]]],  # upper new_rect
                                [[all_x[0], all_x[-1]], [R[1][0], all_y[0]]],  # lower new_rect
                                [[all_x[-1], R[0][1]], [R[1][0], R[1][1]]]])  # right new_rect
    for i, j in itertools.product(np.arange(2*N-1), np.arange(2*N-1)):
        center_x, center_Y = (all_x[i + 1] - all_x[i]) / 2 + all_x[i], (all_y[j + 1] - all_y[j]) / 2 + all_y[j]
        valid = 1
        for c in np.arange(N):
            r = rects[c]
            if center_in_rect(center_x, center_Y, r):  # make sure that the new suggested rect is not inside rects
                valid = 0
                break
        if valid:
            potential_rects = np.append(potential_rects, [[[all_x[i], all_x[i + 1]], [all_y[j], all_y[j + 1]]]], 0)
    return potential_rects
