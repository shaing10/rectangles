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
    # add new rectangles that have a common edge(s) with R
    potential_rects = np.array([[[R[0][0], all_x[0]], [R[1][0], R[1][1]]],  # left new_rect
                                [[all_x[0], all_x[-1]], [all_y[-1], R[1][1]]],  # upper new_rect
                                [[all_x[0], all_x[-1]], [R[1][0], all_y[0]]],  # lower new_rect
                                [[all_x[-1], R[0][1]], [R[1][0], R[1][1]]]])  # right new_rect
    for i, j in itertools.product(np.arange(2 * N - 1), np.arange(2 * N - 1)):
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


def set_2_rect_arr(set_):
    """
    convert a set of 4 tuples (x,y) indicate the vertexes of a rectangle into an array [[x1,x2],[y1,y2]]
    :param set_: set of 4 vertexes
    :return: array that describes rectangle [[x1,x2],[y1,y2]]
    """

    list_ = list(set_)
    out = np.array([item for t in list_ for item in t])
    xs, ys = [out[0], out[len(set_)]], [out[1], out[len(set_)+1]]
    arr = np.array([[[np.min(xs), np.max(xs)], [np.min(ys), np.max(ys)]]])
    return arr


def opt_potential_rects(potential_rects):
    """
    :param potential_rects: ndarray of shape (M,2,2) with many rectangles' coordinates
    :return: merged_rects: ndarray of shape (K,2,2) where K<M - lower number of rectangles that cover the same area
    """

    i, j = 0, 1
    while i < potential_rects.shape[0]:
        if i != j:
            l1 = list(np.ravel(potential_rects[i]))
            l2 = list(np.ravel(potential_rects[j]))
            a = [(l1[n], l1[m]) for n in np.arange(2) for m in np.arange(2)+2]
            b = [(l2[n], l2[m]) for n in np.arange(2) for m in np.arange(2)+2]
            set_a, set_b = set(a), set(b)
            intersection = set_a.intersection(b)
            if len(intersection) == 2:  # two common vertices indicate that those rectangles can be merged
                new_set = set_a ^ set_b
                potential_rects = np.append(potential_rects, set_2_rect_arr(new_set), 0)
                potential_rects = np.delete(potential_rects, [i, j], 0)
                i = 0
            else:
                j += 1
        else:
            j += 1
        if j >= potential_rects.shape[0]:
            i += 1
            j = 0
    merged_rects = potential_rects
    return merged_rects
