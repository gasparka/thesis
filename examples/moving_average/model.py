import numpy as np

from pyha.common.const import Const
from pyha.common.hwsim import HW, default_sfix
from pyha.common.sfix import Sfix, left_index, right_index, fixed_wrap, fixed_truncate
from pyha.common.sfix import resize
from pyha.common.util import is_power2
from pyha.simulation.simulation_interface import assert_sim_match


class MovingAverage(HW):
    def __init__(self, window_len):
        self.window_len = window_len
        self.window_pow = int(np.log2(window_len))

        # registers
        self.shr = [Sfix()] * self.window_len
        self.sum = Sfix(0, self.window_pow, -17, overflow_style=fixed_wrap)
        self.mul = Sfix(0, 0, -17, round_style=fixed_truncate, overflow_style=fixed_wrap)

        # these can be removed actually? Fitter optimizes this out
        self.window_pow = Const(self.window_pow)
        self.coef = Sfix(1/window_len, 0, -17)

        # module delay
        self._delay = 2

    def main(self, x):
        self.next.shr = [x] + self.shr[:-1]
        self.next.sum = self.sum + x - self.shr[-1]

        self.next.mul = self.sum * self.coef
        return self.mul

    # def main(self, x):
    #     mul = x >> self.window_pow
    #
    #     self.next.shift_register = [mul] + self.shift_register[:-1]
    #
    #     # calculate new sum
    #     self.next.sum = self.sum + mul - self.shift_register[-1]
    #
    #     return self.sum

    def model_main(self, inputs):
        taps = [1 / self.window_len] * self.window_len
        ret = np.convolve(inputs, taps, mode='full')
        return ret[:-self.window_len + 1]


def test_convert():
    mov = MovingAverage(window_len=4)
    x = [-0.2, 0.05, 1.0, -0.9571, 0.0987]
    expected = [-0.05, -0.0375, 0.2125, -0.026775, 0.0479]
    assert_sim_match(mov, expected, x, dir_path='/home/gaspar/git/thesis/playground')