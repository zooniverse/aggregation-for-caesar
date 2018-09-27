def ellipse_normalize(params):
    x, y, rx, ry, angle = params
    if ry <= rx:
        major = rx
        minor = ry
        angle %= 180
    else:
        major = ry
        minor = rx
        angle = (angle - 90) % 180
    return (x, y, major, minor, angle)


def line_normalize(params):
    x1, y1, x2, y2 = params
    forward = (x1, y1, x2, y2)
    backwards = (x2, y2, x1, y1)
    if x1 < x2:
        return forward
    elif x1 > x2:
        return backwards
    elif y1 < y2:
        return forward
    else:
        return backwards


def rotate_rectangle_normalize(params):
    x, y, width_in, height_in, angle = params
    if height_in <= width_in:
        x = x
        y = y
        width = width_in
        height = height_in
        angle %= 180
    else:
        delta = (height_in - width_in) / 2
        x -= delta
        y += delta
        width = height_in
        height = width_in
        angle = (angle - 90) % 180
    return (x, y, width, height, angle)


def triangle_normalize(params):
    x, y, r, angle = params
    return (x, y, r, angle % 120)


SHAPE_NORMALIZATION = {
    'ellipse': ellipse_normalize,
    'line': line_normalize,
    'rotateRectangle': rotate_rectangle_normalize,
    'triangle': triangle_normalize
}
