import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Rectangle
import algo
import gen_valid_data


def isOverlap_1d(coords, N):
    """
    :param coords: 1darray with 2N values which are couples of indices, each couple represents a line (aligns to one
    of the axes)
    :param N: number of objects
    :return: candidates: list of N arrays.
             The ith array contains all jth indices which might be overlapping with ith object according to this axis
    """
    coords_order = coords.argsort() % N
    candidates = []
    for ind in np.arange(N):
        bool_arr = coords_order - ind == 0
        cands_range = [i for i, x in enumerate(bool_arr) if x]
        candidates.append([np.unique(coords_order[cands_range[0] + 1:cands_range[1]])])
    return candidates


def is_valid(rects, R, N):
    """
    checks if:
    (1): rects are non overlapping
    (2): all rects are in R bounds
    :param rects: rectangles coordinates, ndarray of shape (N,2,2)
    :param R: bigger rectanle coordinates, ndarray of shape (2,2)
    :return: boolean. is the input valid or not
    """
    rects = np.sort(rects)  # values should be sorted to match the algorithm
    # rearrange to have an array for each coord type rather than each rectangle
    rects = np.reshape(np.ravel(rects), [4, N], 'F')

    # check condition (1): validate that rects are non overlapping
    if N > 1:
        x_coords = np.concatenate((rects[0], rects[1]))
        x_candidates = isOverlap_1d(x_coords, N)  # overlapping check on x axis
        y_coords = np.concatenate((rects[2], rects[3]))
        y_candidates = isOverlap_1d(y_coords, N)  # overlapping check on x axis

        # is there a rectangle that overlaps in x *and* y?
        for ind in np.arange(N):
            curr_cand_x = np.array(x_candidates[ind][0])
            curr_cand_y = np.array(y_candidates[ind][0])
            if curr_cand_x.size == 0 or curr_cand_y.size == 0:
                continue
            is_overlap = any(np.array(curr_cand_x == curr_cand_y))
            if is_overlap:
                print('rectangles are overlapping')
                return 0
    # check condition (2): validate that all rects are in R bounds
    bounds_max = np.max(rects, 1)  # second line of rects are the bigger x's, forth line are the bigger y's
    bounds_min = np.min(rects, 1)  # first line of rects are the smaller x's, third line are the smaller y's
    in_bounds = R[0][0] < bounds_min[0] and R[0][1] > bounds_max[1] and R[1][0] < bounds_min[2] and R[1][1] > \
                bounds_max[3]
    if not in_bounds:
        print('not all rectangles are in R bounds')
        return 0
    return 1


def plotting(rects, R, N, new_rects=[]):
    """
    visualization of the rectangles - both given (R, {c_N}) and new (if supplied)
    :param rects: rectangles coordinates, ndarray of shape (N,2,2)
    :param R: bigger rectanle coordinates, ndarray of shape (2,2)
    :param N: number of smaller rectangles
    :param new_rects, ndarray of shape (M,2,2)
    :return:
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    handles = []

    # plot R
    R_rect = matplotlib.patches.Rectangle((R[0][0], R[1][0]),
                                          np.abs(R[0][1] - R[0][0]), np.abs(R[1][1] - R[1][0]),
                                          color='pink',
                                          ec='black',
                                          lw=1)

    ax.add_patch(R_rect)
    handles.append(matplotlib.patches.Patch(color='pink', label='R'))

    # plot each given rectangle
    for ind in np.arange(N):
        x1, x2 = rects[ind][0][0], rects[ind][0][1]
        y1, y2 = rects[ind][1][0], rects[ind][1][1]
        assert x2 >= x1, y2 >= y1
        rect = matplotlib.patches.Rectangle((x1, y1),
                                            np.abs(x2 - x1), np.abs(y2 - y1),
                                            color='green',
                                            ec='green',
                                            lw=1)

        ax.add_patch(rect)
    handles.append(matplotlib.patches.Patch(color='green', label='given rects'))

    # plot each new rectangle
    if np.array(new_rects).shape[0] > 0:
        for ind in np.arange(new_rects.shape[0]):
            x1, x2 = new_rects[ind][0][0], new_rects[ind][0][1]
            y1, y2 = new_rects[ind][1][0], new_rects[ind][1][1]
            assert x2 >= x1, y2 >= y1
            new_rect = matplotlib.patches.Rectangle((x1, y1),
                                                    np.abs(x2 - x1), np.abs(y2 - y1),
                                                    color='grey',
                                                    ec='k',
                                                    lw=1)
            ax.add_patch(new_rect)
        handles.append(matplotlib.patches.Patch(color='grey', label='new rects'))

    ax.autoscale_view()
    plt.legend(handles=handles)
    plt.show()


if __name__ == '__main__':
    # generate data
    Nun_of_rects = 5
    a = gen_valid_data.RectsAndR(Nun_of_rects, R_maximal_val=10)  # create a class
    R = a.gen_R_coords()  # generate R coordinates
    rects = a.gen_rects_coords()  # generate Nun_of_rects of valid rectangles
    # check validity
    input_is_valid = is_valid(rects, R, Nun_of_rects)
    print(f"input_is_valid={input_is_valid}")
    plotting(rects, R, Nun_of_rects)
    # find new rectangles to cover R\{c_N}
    potential_rects = algo.fill_rect(R, rects)
    # merge rectangles which have 2 common vertices
    # final_rects = algo.opt_potential_rects(potential_rects)
    plotting(rects, R, Nun_of_rects, potential_rects)
    # plotting(rects, R, Nun_of_rects, final_rects)
