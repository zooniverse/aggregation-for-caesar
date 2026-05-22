SHAPE_LUT = {
    'circle': ['x', 'y', 'r'],
    'column': ['x', 'width'],
    'ellipse': ['x', 'y', 'rx', 'ry', 'angle'],
    'fullWidthLine': ['y'],
    'fullHeightLine': ['x'],
    'line': ['x1', 'y1', 'x2', 'y2'],
    'point': ['x', 'y'],
    'rectangle': ['x', 'y', 'width', 'height'],
    'rotateRectangle': ['x', 'y', 'width', 'height', 'angle'],
    'triangle': ['x', 'y', 'r', 'angle'],
    'fan': ['x', 'y', 'radius', 'spread', 'rotation'],
    'temporalRotateRectangle': ['x_center', 'y_center', 'width', 'height', 'angle', 'displayTime'],
    'temporalPoint': ['x', 'y', 'displayTime']
}

SHAPE_LUT_FEM = {
    'circle': ['x_center', 'y_center', 'r'],
    'ellipse': ['x_center', 'y_center', 'rx', 'ry', 'angle'],
    'line': ['x1', 'y1', 'x2', 'y2'],
    'point': ['x', 'y'],
    'rectangle': ['x_center', 'y_center', 'width', 'height'],
    'rotateRectangle': ['x_center', 'y_center', 'width', 'height', 'angle'],
    'graph2dRangeX': ['x', 'width'],  # could use either graph2dRangeX or column
    'column': ['x', 'width'],  # could use either graph2dRangeX or column
    'temporalRotateRectangle': ['x_center', 'y_center', 'width', 'height', 'angle', 'displayTime'],
    'temporalPoint': ['x', 'y', 'displayTime']
}
