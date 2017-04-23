import numpy as np

from pyha.common.const import Const
from pyha.common.hwsim import HW, default_sfix
from pyha.common.sfix import Sfix, left_index, right_index, fixed_wrap, fixed_truncate
from pyha.common.sfix import resize
from pyha.common.util import is_power2
from pyha.simulation.simulation_interface import assert_sim_match, debug_assert_sim_match, SIM_MODEL, SIM_HW_MODEL, \
    SIM_RTL, SIM_GATE
import matplotlib.pyplot as plt


class MovingAverageSimple(HW):
    def __init__(self):
        # registers
        self.shr = [Sfix()] * 4
        self.sum = Sfix(0, 0, -17, overflow_style=fixed_wrap)

        self._delay = 1

    def main(self, x):
        div = x >> 2

        self.next.shr = [div] + self.shr[:-1]
        self.next.sum = self.sum + div - self.shr[-1]
        return self.sum

    def model_main(self, inputs):
        taps = [1 / self.window_len] * self.window_len
        ret = np.convolve(inputs, taps, mode='full')
        return ret[:-self.window_len + 1]


class MovingAverage(HW):
    def __init__(self, window_len):
        self.window_len = window_len

        self.shr = [Sfix()] * self.window_len
        self.sum = Sfix(0, 0, -17, overflow_style=fixed_wrap)

        self.window_pow = Const(int(np.log2(window_len)))

        self._delay = 1

    def main(self, x):
        div = x >> self.window_pow

        self.next.shr = [div] + self.shr[:-1]
        self.next.sum = self.sum + div - self.shr[-1]
        return self.sum

    def model_main(self, inputs):
        taps = [1 / self.window_len] * self.window_len
        ret = np.convolve(inputs, taps, mode='full')
        return ret[:-self.window_len + 1]


def test_convert():
    mov = MovingAverage(window_len=4)
    x = [-0.2, 0.05, 1.0, -0.9571, 0.0987]
    expected = [-0.05, -0.0375, 0.2125, -0.026775, 0.0479]
    assert_sim_match(mov, expected, x, dir_path='/home/gaspar/git/thesis/playground')


def test_match_filtering():
    from pyha.common.util import hex_to_bool_list, bools_to_bitstr, hex_to_bitstr
    sps = 16
    noise_amp = 0.8
    bits = hex_to_bool_list('a12345')
    nrz = [[1] * sps if x else [-1] * sps for x in bits]
    nrz = np.array(nrz).flatten()

    # noise
    sig = nrz + np.random.uniform(-noise_amp, noise_amp, len(nrz))

    # sig *= 0.5

    dut = MovingAverage(window_len=16)
    r = debug_assert_sim_match(dut, None, sig,
                               simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_RTL],
                               dir_path='/home/gaspar/git/thesis/playground')

    fig, axes = plt.subplots(2, 1, sharex=True, sharey=True, figsize=(8, 4))
    # add a big axes, hide frame
    fig.add_subplot(111, frameon=False)
    axes[0].plot(sig, label='x')
    axes[0].legend(loc='upper right')
    axes[0].set_title('(a) Digital signal, 16 samples per symbol')
    axes[0].grid()



    axes[1].plot(r[0], label='y: Model')
    axes[1].plot(r[1], label='y: Pyha')
    axes[1].plot(r[2], label='y: RTL')
    axes[1].plot(r[2], label='y: GATE')
    axes[1].legend(loc='upper right')

    axes[1].set_title('(b) Averaged by 16')
    axes[1].grid()

    # hide tick and tick label of the big axes
    plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
    plt.xlabel("Sample number")
    plt.ylabel("Amplitude")
    plt.savefig('img/moving_average_matched.png', bbox_inches='tight')

    plt.show()