import numpy as np


class RectsAndR:
    def __init__(self, N=3, R_maximal_val=10):
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
        create np.array with N arrays of [[x1,x2],[y1,y2]] - non overlapping rectangles inside R_coords
        non overlapping is ensured by separation on x-axis (it could be y-axis as well, random choice)
        :return: coordinates of {r}_N - smaller non-overlapping rectangles
        """
        Rx1, Rx2, Ry1, Ry2 = self.R_coords[0][0], self.R_coords[0][1], self.R_coords[1][0], self.R_coords[1][1]
        x_coords = np.sort(np.random.uniform(Rx1, Rx2, [2*self.N]))
        y_coords = np.random.uniform(Ry1, Ry2, [2*self.N])
        x_1, x_2 = x_coords[0::2], x_coords[1::2]
        y_1, y_2 = y_coords[0::2], y_coords[1::2]
        c = np.array([[x_1, y_1], [x_2, y_2]])
        self.rects_coords = c.transpose()
        return np.sort(self.rects_coords)

