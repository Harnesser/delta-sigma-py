# Models of Delta-Sigma ADC Modulators
import numpy as np

def run(t, vin):

    return _mash_2_1(t, vin)
    #return _mash_1_1(t, vin)
    #return _first_order(t, vin)
    #return _second_order(t, vin)
        


def _first_order(t, vin):
    y = np.zeros( len(t), dtype=float)
    u = np.zeros( len(t), dtype=float)

    for n in range(1, len(vin)):
        u[n] = ( vin[n] - y[n-1] ) + u[n-1]
        y[n] = ( 1.0 if u[n] > 0.0 else -1.0 )

    return (vin, u, y), ('v(in)', 'v(u)', 'v(y)')


def _second_order(t, vin):
    y = np.zeros( len(t), dtype=float)
    u = np.zeros( len(t), dtype=float)
    v = np.zeros( len(t), dtype=float)

    for n in range(1, len(vin)):
        u[n] = ( vin[n] - y[n-1] ) + u[n-1]
        v[n] = ( u[n] - y[n-1] ) + v[n-1]
        y[n] = ( 1.0 if v[n] > 0.0 else -1.0 )

    return (vin, u,v, y), ('v(in)', 'v(u)', 'v(v)', 'v(y)')


def _mash_1_1(t, vin):
    e1 = np.zeros( len(t), dtype=float)
    y2d = np.zeros( len(t), dtype=float)
    y = np.zeros( len(t), dtype=float)

    for n in range(1, len(vin)):

        # MASH-(1)-1 : signal modulator
        (_, u1, y1), _ = _first_order(t, vin)

        # MASH-1-(1) : noise modulator
        e1[n] = y1[n-1] - u1[n]
        (_, _, y2), _ = _first_order(t, e1)

        # reconstruction
        y2d[n] = y2[n] - y2[n-1]
        y[n] = y1[n] - y2d[n]

    return (vin, e1, y), ('v(in)', 'e(1)', 'v(y)')


def _mash_2_1(t, vin):
    e1 = np.zeros( len(t), dtype=float)
    y2d = np.zeros( len(t), dtype=float)
    y2dd = np.zeros( len(t), dtype=float)
    y = np.zeros( len(t), dtype=float)

    for n in range(1, len(vin)):

        # MASH-(2)-1 : signal modulator
        (_, u1, v1, y1), _ = _second_order(t, vin)

        # MASH-2-(1) : noise modulator
        e1[n] = y1[n-1] - u1[n]
        (_, _, y2), _ = _first_order(t, e1)

        # reconstruction
        y2d[n] = y2[n] - y2[n-1]
        y2dd[n] = y2d[n] - y2d[n-1]
        y[n] = y1[n] - y2dd[n]

    return (vin, e1, y), ('v(in)', 'e(1)', 'v(y)')
