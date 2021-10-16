import numpy as np


class RectsAndR:
    def __init__(self, N=3, R_maximal_val=100):
        self.N = N
        self.R_maximal_val = R_maximal_val
        self.R_coords = []
        self.rects_coords = []

    def gen_R_coords(self):
        """
        create an array of R coordinates: [[x1,x2],[y1,y2]]
        :return: R_coords: [[x1,x2],[y1,y2]] where x2>x1, y2>y1
        """
        R_coords = self.R_maximal_val * (2 * np.random.random([2, 2]) - 1)
        self.R_coords = np.sort(R_coords)
        return self.R_coords

    def gen_rects_coords(self):
        """
        create N arrays of [[x1,x2],[y1,y2]] values in range [-rect_size,rect_size], non overlapping
        :return: coordinates of {r}_N - the smaller non-overlapping rectangles
        """
        # generate one axis non-integers coordinates inside R boundaries
        # ind = 1
        # while ind < self.N
        #     curr_rect_x = np.random.uniform(self.R_coords[0][0], self.R_coords[0][1])
        #     curr_rect_y = np.random.uniform(self.R_coords[1][0], self.R_coords[1][1])
        #     if
        #     self.rects_coords.append

        # sorted_partial_coords = np.sort(partial_coords)

        print(sorted_partial_coords)
        rects_coords = np.random.random(self.N, 2, 1)

        self.rects_coords = np.sort(rects_coords)
        return self.rects_coords


if __name__ == '__main__':
    0