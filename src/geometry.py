from math import sqrt


def middle_point(x1, y1, x2, y2):
    return (x1 + x2) / 2, (y1 + y2) / 2


def slope(x1, y1, x2, y2):
    return (y1 - y2) / (x1 - x2)


def b(x, y, m):
    return y - m * x


def b_parallel(dp, m, b_dist):
    return dp * sqrt(pow(m, 2) + 1) + b_dist


def perpendicular_slope(m):
    return -1 / m


def orthogonal_point(m_perp, b_perp, m, b_prl):
    x_orth = (b_perp - b_prl) / (m - m_perp)
    y_orth = m * x_orth + b_prl
    return x_orth, y_orth


def point_on_line(x1, y1, x2, y2, t):
    xt = x1 + t / 100 * (x2 - x1)
    yt = y1 + t / 100 * (y2 - y1)
    return xt, yt


def get_ctrl_points(x1, y1, x2, y2, dist):
    m = slope(x1, y1, x2, y2)
    b_ = b(x1, y1, m)
    b_prl = b_parallel(dist, m, b_)
    m_perp = perpendicular_slope(m)
    x_p_1, y_p_1 = point_on_line(x1, y1, x2, y2, 40)
    x_p_2, y_p_2 = point_on_line(x1, y1, x2, y2, 60)
    b_perp_1 = b(x_p_1, y_p_1, m_perp)
    b_perp_2 = b(x_p_2, y_p_2, m_perp)

    x_ctrl_1, y_ctrl_1 = orthogonal_point(m_perp, b_perp_1, m, b_prl)
    x_ctrl_2, y_ctrl_2 = orthogonal_point(m_perp, b_perp_2, m, b_prl)

    return int(x_ctrl_1), int(y_ctrl_1), int(x_ctrl_2), int(y_ctrl_2)
