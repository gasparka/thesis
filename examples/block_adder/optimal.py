from pyha.common.const import Const
from pyha.common.sfix import Sfix, resize, fixed_truncate, fixed_wrap
from pyha.common.hwsim import HW
import numpy as np
from pyha.simulation.simulation_interface import debug_assert_sim_match, SIM_GATE, plot_assert_sim_match, SIM_MODEL, \
    SIM_HW_MODEL, SIM_RTL
import matplotlib.pyplot as plt


class OptimalBlockAdd(HW):
    def __init__(self, window_size):
        # registers
        self.shr = [0] * window_size
        self.sum = 0

        # module delay
        self._delay = 2

    def main(self, x):
        self.next.shr = [x] + self.shr[:-1]

        self.next.sum = self.sum + x - self.shr[-1]

        return self.sum

    def model_main(self, xl):
        # return np.convolve(xl, [1] * 4)
        xl = [0, 0, 0] + xl
        y = []
        for i in range(len(xl) - 3):
            s = sum(xl[i: i + 4])
            y.append(s)

        return y


def test_lastacc():
    dut = OptimalBlockAdd(4)
    x = [0, 1, 2, 3, 2, 1, 0]

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_RTL],
                               dir_path='/home/gaspar/git/thesis/playground')

    plt.figure(figsize=(8, 2))
    plt.stem(x, label='x', basefmt=" ")
    plt.plot(r[0], label='y: Model')
    plt.plot(r[1], label='y: Pyha')
    plt.plot(r[2], label='y: RTL')
    # plt.plot(r[3], label='y: GATE')

    plt.grid()
    plt.xlabel("Sample number")
    plt.ylabel("Value")
    plt.legend()
    plt.savefig('img/sim_tmp.png', bbox_inches='tight')
    plt.show()

    print(r)


class OptimalBlockAddFix(HW):
    def __init__(self, window_size):
        self.window_size = window_size
        # registers
        self.shr = [Sfix()] * window_size
        # self.sum = Sfix(left=0, overflow_style=fixed_wrap)
        self.sum = Sfix(left=0)

        # module delay
        self._delay = 1

    def main(self, x):
        self.next.shr = [x] + self.shr[:-1]

        self.next.sum = self.sum + x - self.shr[-1]

        return self.sum

    def model_main(self, xl):
        return np.convolve(xl, [1.0] * self.window_size)[:-self.window_size + 1]


def test_lastacc_fix():
    dut = OptimalBlockAddFix(4)

    x = np.random.uniform(-0.8, 0.8, 64)

    fs = 128
    x = np.sin(2 * np.pi * 1 * np.linspace(0, 2, 2 * fs)) * 0.27
    # x = [0.3, 0.3, 0.3, 0.3, 0.3, -0.3, -0.3, -0.3]

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_RTL],
                               dir_path='/home/gaspar/git/thesis/playground')

    plt.figure(figsize=(8, 2))
    # plt.stem(x, label='x', basefmt=" ")
    # plt.plot(x)
    plt.plot(r[0], label='y: Model')
    plt.plot(r[1], label='y: Pyha')
    plt.plot(r[2], label='y: RTL')
    plt.plot(r[2], label='y: GATE')

    plt.title('x=[0.15]*8')
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