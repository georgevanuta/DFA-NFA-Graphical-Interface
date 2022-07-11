# BEZIER FUNCTIONS FOR GI

def point_on_bezier(x1, y1, x2, y2, x3, y3, x4, y4, t):
    xt = pow(1 - t, 3) * x1 + 3 * t * pow(1 - t, 2) * x2 + 3 * pow(t, 2) * (1 - t) * x3 + pow(t, 3) * x4
    yt = pow(1 - t, 3) * y1 + 3 * t * pow(1 - t, 2) * y2 + 3 * pow(t, 2) * (1 - t) * y3 + pow(t, 3) * y4

    return xt, yt


def point_on_bezier_derivative(x1, y1, x2, y2, x3, y3, x4, y4, t):
    xt_derivative = 3 * pow(1 - t, 2) * (x2 - x1) + 6 * (1 - t) * t * (x3 - x2) + 3 * pow(t, 2) * (x4 -  x3)
    yt_derivative = 3 * pow(1 - t, 2) * (y2 - y1) + 6 * (1 - t) * t * (y3 - y2) + 3 * pow(t, 2) * (y4 -  y3)

    return xt_derivative, yt_derivative
