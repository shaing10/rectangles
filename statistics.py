import numpy as np
import matplotlib.pyplot as plt
import gen_valid_data

if __name__ == '__main__':
    # generate data
    Num_of_rects = 50
    Num_epochs = 100
    R_maximal_val = 1000
    a = gen_valid_data.RectsAndR(Num_of_rects, R_maximal_val)  # create a class
    x_centers, y_centers = np.array([]), np.array([])
    mask = np.zeros((2*R_maximal_val+1, 2*R_maximal_val+1))
    rel_coverage = np.array([])
    for i in np.arange(Num_epochs):  # very large number of inputs
        R = a.gen_R_coords()  # generate R coordinates
        rects = a.gen_rects_coords()  # generate Num_of_rects valid rectangles
        x = np.append(rects, np.array([R]), 0)
        centers = a.compute_centers(x)
        x_centers, y_centers = np.append(x_centers, centers.transpose()[0]), np.append(y_centers, centers.transpose()[1])
        rel_coverage = np.append(rel_coverage, a.compute_rel_coverage())
        mask += a.create_a_mask()

    # Data analysis
    print(f"x centers std:{np.std(x_centers)}, y centers std{np.std(y_centers)}")
    print(f"mean rel_coverage={np.mean(rel_coverage)}")

    # 2d histogram for the rectangles centers
    boundaries = np.ones((2, 1)) * (-R_maximal_val)
    boundaries = np.append(boundaries, np.ones((2, 1)) * R_maximal_val, 1)
    # create an 2D histogram of x,y centers of input rectangles: R and {r_N}
    H, xedges, yedges = np.histogram2d(x_centers, y_centers, range=boundaries)
    H = H.T

    # plotting
    fig = plt.figure(figsize=(7, 3))
    ax = fig.add_subplot(111, title='input centers 2D hist')
    plt.imshow(H, interpolation='nearest', origin='lower',
               extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
    plt.show()

    # relative coverage histogram
    fig = plt.figure(figsize=(7, 3))
    plt.hist(rel_coverage, bins='auto')
    plt.title(f"rectangles' Relative Coverage Histogram - N={Num_of_rects}, epochs={Num_epochs}")
    plt.show()

    # rectangles coverage
    fig = plt.figure(figsize=(7, 3))
    plt.imshow(mask)
    plt.title(f"rectangles coverage for N={Num_of_rects}, Num_epochs={Num_epochs}, Num_of_rects={Num_of_rects}")
    plt.show()
