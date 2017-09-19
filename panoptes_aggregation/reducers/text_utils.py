def overlap(x, y):
    '''Check if two line segments overlap

    Parameters
    ----------
    x : list
        A list with the start and end point of the first line segment
    y : lits
        A list with the start and end point of the second line segment

    Returns
    -------
    overlap : bool
        True if the two line segments overlap, False otherwise
    '''
    return x[1] >= y[0] and y[1] >= x[0]


def gutter(lines_in):
    '''Cluster list of input line segments by what side of
    the page gutter they are on.

    Parameters
    ----------
    lines_in : list
        A list-of-lists containing one line segment per item. Each line
        segment should contain only the x-coordinate of each point on the line.

    Returns
    -------
    gutter_index : array
        A numpy array containing the cluster label for each input line. This label
        idicates what side of the gutter(s) the input line segment is on.
    '''
    lines = [[min(l), max(l)] for l in lines_in]
    overlap_lines = []
    for ldx, l in enumerate(lines):
        if ldx == 0:
            overlap_lines = np.array([l])
        else:
            o_lines = np.array([overlap(o, l) for o in overlap_lines])
            if o_lines.any():
                comp = np.vstack([overlap_lines[o_lines], l])
                overlap_lines[o_lines] = [comp.min(), comp.max()]
                overlap_lines = np.unique(overlap_lines).reshape(-1, 2)
            else:
                overlap_lines = np.vstack([overlap_lines, l])
    overlap_lines.sort(axis=0)
    gutter_label = -np.ones(len(lines), dtype=int)
    for odx, o in enumerate(overlap_lines):
        gdx = np.array([overlap(o, l) for l in lines])
        gutter_label[gdx] = odx
    return gutter_label


def angle_metric(t1, t2):
    '''A metric for the distance between angles in the [-180, 180] range

    Parameters
    ----------
    t1 : float
        Theta one in degrees
    t2 : float
        Theta two in degrees

    Returns
    -------
    distance : float
        The distance between the two input angles in degrees
    '''
    d = abs(t1 - t2)
    if d > 180:
        d = 360 - d
    return d


def avg_angle(theta):
    '''A function that finds the avage of an array of angles that are
    in the range [-180, 180].

    Parameters
    ----------
    theta : array
        An array of angles that are in the range [-180, 180] degrees

    Returns
    -------
    average : float
        The average angle
    '''
    if theta.max() - theta.min() > 180:
        theta[theta < 0] += 360
    return theta.mean()
