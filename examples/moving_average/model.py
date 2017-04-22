import numpy as np

from pyha.common.const import Const
from pyha.common.hwsim import HW, default_sfix
from pyha.common.sfix import Sfix, left_index, right_index, fixed_wrap, fixed_truncate
from pyha.common.sfix import resize
from pyha.common.util import is_power2


class MovingAverage(HW):
    def __init__(self, window_len):
        if window_len < 2:
            raise AttributeError('Window length must be >= 2')

        if not is_power2(window_len):
            raise AttributeError('Window length must be power of 2')

        self.window_len = window_len
        self.window_pow = int(np.log2(window_len))

        # registers
        self.shift_register = [Sfix()] * self.window_len
        self.sum = Sfix(0, 0, -17, overflow_style=fixed_wrap, round_style=fixed_truncate)

        # these can be removed actually? Fitter optimizes this out
        self.window_pow = Const(self.window_pow)

        # module delay
        self._delay = 1

    def main(self, x):
        mul = x >> self.window_pow

        self.next.shift_register = [mul] + self.shift_register[:-1]

        # calculate new sum
        self.next.sum = self.sum + mul - self.shift_register[-1]

        return self.sum

    def model_main(self, inputs):
        taps = [1 / self.window_len] * self.window_len
        ret = np.convolve(inputs, taps, mode='full')
        return ret[:-self.window_len + 1]
