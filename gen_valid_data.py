import numpy as np


class RectsAndR:
    def __init__(self, N=3, R_maximal_val=10):
        self.N = N
        self.R_maximal_val = R_maximal_val
        self.R_coords = []
        self.rects_coords = []
        self.centers = []
        self.rel_coverage = []

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

    def compute_centers(self, x):
        """
        :param x: 3darray of rectangles' coordinates (Number of rectangles, 2, 2)
        :return: rectangles' centers in array of [x, y] pairs
        """
        self.centers = np.mean(x, 2)
        return self.centers

    def compute_rel_coverage(self):
        """
        :return: relative coverage of rectangle in R
        """
        R = self.R_coords
        R_area = (R[0][1]-R[0][0])*(R[1][1]-R[1][0])
        a = self.rects_coords
        rects_coverage = np.sum((a[:, 1, 1] - a[:, 1, 0]) * (a[:, 0, 1] - a[:, 0, 0]))
        self.rel_coverage = rects_coverage/R_area
        return self.rel_coverage

    def create_a_mask(self):
        """
        :return: mask of size [[-self.R_maximal_val, self.R_maximal_val][-self.R_maximal_val, self.R_maximal_val]].
         quantize the rectangles coordinates on a grid. the mask equals '1' if it is inside a rectangle, and zeros
        otherwise. the bigger rectangles R are not part of this statistics
        """
        mask = np.zeros((2*self.R_maximal_val+1, 2*self.R_maximal_val+1))  # create a mask is the maximal possible size
        # turn coordinates into integers (quantization), plus translation to meet mask's indices properly
        a = self.rects_coords.astype(int) + self.R_maximal_val
        a = np.sort(a)
        for i in np.arange(a.shape[0]):
            mask[a[i, 0, 0]:a[i, 0, 1]+1, a[i, 1, 0]:a[i, 1, 1]+1] += 1  # manually create an histogram
        return mask.transpose()

