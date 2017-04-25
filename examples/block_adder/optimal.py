from pyha.common.const import Const
from pyha.common.sfix import Sfix, resize, fixed_truncate, fixed_wrap
from pyha.common.hwsim import HW
import numpy as np
from pyha.simulation.simulation_interface import debug_assert_sim_match, SIM_GATE, plot_assert_sim_match, SIM_MODEL, \
    SIM_HW_MODEL, SIM_RTL
import matplotlib.pyplot as plt


class OptimalSlideAdd(HW):
    def __init__(self, window_len):
        self.window_len = window_len
        self.mem = [0] * window_len
        self.sum = 0

        self._delay = 1

    def main(self, x):
        self.next.mem = [x] + self.mem[:-1]

        self.next.sum = self.sum + x - self.mem[-1]
        return self.sum

    def model_main(self, xl):
        return np.convolve(xl, [1.0] * self.window_len)[:-self.window_len + 1]


def test_OptimalSlideAdd():
    dut = OptimalSlideAdd(4)
    x = [ 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1]

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_RTL],
                               dir_path='/home/gaspar/git/thesis/playground')



    plt.figure(figsize=(8, 1.5))
    plt.plot(x, label='x')
    plt.plot(r[0], label='y: Model')
    plt.plot(r[1], label='y: Pyha')
    plt.plot(r[2], label='y: RTL')
    plt.plot(r[2], label='y: GATE')

    plt.yticks([-4, -1, 1, 4])
    plt.grid()
    plt.xlabel("Sample number")
    plt.ylabel("Value")
    plt.legend()
    plt.savefig('img/sim_tmp.png', bbox_inches='tight')
    plt.show()

    print(r)



class OptimalSlidingAddFix(HW):
    def __init__(self, window_len):
        self.window_len = window_len

        self.mem = [Sfix()] * window_len
        self.sum = Sfix(left=0)

        self._delay = 1

    def main(self, x):
        self.next.mem = [x] + self.mem[:-1]

        self.next.sum = self.sum + x - self.mem[-1]

        return self.sum

    def model_main(self, xl):
        return np.convolve(xl, [1.0] * self.window_len)[:-self.window_len + 1]


def test_lastacc_fix():
    dut = OptimalSlidingAddFix(4)

    x = np.random.uniform(-0.5, 0.5, 64)

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_RTL],
                               dir_path='/home/gaspar/git/thesis/playground')

    plt.figure(figsize=(8, 1.5))
    # plt.stem(x, label='x', basefmt=" ")
    # plt.plot(x)
    plt.plot(r[0], label='y: Model')
    plt.plot(r[1], label='y: Pyha')
    plt.plot(r[2], label='y: RTL')
    plt.plot(r[2], label='y: GATE')

    plt.grid()
    plt.xlabel("Sample number")
    plt.ylabel("Value")
    plt.legend()
    plt.savefig('img/sim_fix_tmp.png', bbox_inches='tight')
    plt.show()

    print(r)


def test_sat_wrap_plot():
    dut = OptimalBlockAddFix(4)


    fs = 128
    x = np.sin(2 * np.pi * 1 * np.linspace(0, 2, 2 * fs)) * 1.2


    y = [Sfix(xi, 0, -17) for xi in x]
    y_wrap = [Sfix(xi, 0, -17, overflow_style=fixed_wrap) for xi in x]


    fig, axes = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(8, 3))
    # add a big axes, hide frame
    fig.add_subplot(111, frameon=False)
    axes[0].plot(x, label='signal')
    axes[0].legend(loc='upper right')
    axes[0].grid()

    axes[1].plot(y, 'r', label='Saturated [-1;1]')
    axes[1].legend(loc='upper right')
    axes[1].grid()

    axes[2].plot(y_wrap, 'g',  label='Wrapped [-1;1]')
    axes[2].legend(loc='upper right')
    axes[2].grid()


    # hide tick and tick label of the big axes
    plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
    plt.xlabel("Sample number")
    plt.ylabel("Amplitude")
    plt.savefig('img/fix_sat_wrap.png', bbox_inches='tight')

    plt.show()


    print(r)