"""
Class to determine wind velocity at any given moment,
calculates a steady wind speed and uses a stochastic
process to represent wind gusts. (Follows section 4.4 in uav book)
"""
import sys
sys.path.append('..')
import numpy as np

class wind_simulation:
    def __init__(self, Ts):
        # steady state wind defined in the inertial frame
        self._steady_state = np.array([[0., 0., 0.]]).T
        # self.steady_state = np.array([[3., 1., 0.]]).T

        #   Dryden gust model parameters (pg 56 UAV book)
        # HACK:  Setting Va to a constant value is a hack.  We set a nominal airspeed for the gust model.
        # Could pass current Va into the gust function and recalculate A and B matrices.
        Va = 17

        sig_u = 2.12
        sig_v = sig_u
        sig_w = 1.4
        Lu = 200
        Lv = Lu
        Lw = 500

        self._A = np.array([[1 - Ts*c, -Ts*d], [Ts, 1]])
        self._B = np.array([[Ts], [0]])
        self._C = np.array([[a,b]])
        self._gust_state = np.array([1., 2., 3.])
        self._Ts = Ts

    def update(self):
        # returns a six vector.
        #   The first three elements are the steady state wind in the inertial frame
        #   The second three elements are the gust in the body frame
        return np.concatenate(( self._steady_state, self._gust() ))

    def _gust(self):
        # calculate wind gust using Dryden model.  Gust is defined in the body frame
        w = np.random.randn()  # zero mean unit variance Gaussian (white noise)
        # propagate Dryden model (Euler method): x[k+1] = x[k] + Ts*( A x[k] + B w[k] )
        self._gust_state += self._A @ self._gust_state + self._B * w
        # output the current gust: y[k] = C x[k]
        return self._C @ self._gust_state
