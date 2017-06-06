from pyha.common.hwsim import HW
from pyha.common.sfix import Sfix
from pyha.simulation.simulation_interface import assert_sim_match, debug_assert_sim_match, plot_assert_sim_match, \
    SIM_MODEL, SIM_HW_MODEL, SIM_RTL

from examples.moving_average.model import MovingAverage
import numpy as np
import matplotlib.pyplot as plt


class DCRemoval(HW):
    def __init__(self, window_len):
        self.mavg = [MovingAverage(window_len), MovingAverage(window_len),
                     MovingAverage(window_len), MovingAverage(window_len)]
        self.y = Sfix(0, 0, -17)

        self._delay = 1

    def main(self, x):
        # run input signal over all the MA's
        tmp = x

        for mav in self.mavg:
            tmp = mav.main(tmp)

        # dc-free signal
        self.next.y = x - tmp
        return self.y

    def model_main(self, xl):
        tmp = xl
        for mav in self.mavg:
            tmp = mav.model_main(tmp)

        # this actually not quite equal to main, delay issues?

        y = xl - np.array([0, 0, 0] + tmp.tolist()[:-3])
        return y


def test_quad4_len32():
    x = [0.5] * 64 + [-0.5] * 64

    dut = DCRemoval(64)
    plot_assert_sim_match(dut, None, x,
                          simulations=[SIM_MODEL, SIM_HW_MODEL],
                          dir_path='/home/gaspar/git/thesis/playground')


def test_plot():
    x = np.sin(10 * np.pi * np.linspace(0, 10, 512)) * 0.5
    x += 0.5
    dut = DCRemoval(64)

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_RTL],
                               dir_path='/home/gaspar/git/thesis/playground')

    plt.figure(figsize=(8, 1.5))
    # plt.plot(x, label='x')
    plt.plot(r[0], label='y: Model')
    plt.plot(r[1], label='y: Pyha')
    plt.plot(r[2], label='y: RTL')
    plt.plot(r[2], label='y: GATE')

    plt.grid()
    plt.xlabel("Sample number")
    plt.ylabel("Value")
    plt.legend()
    plt.savefig('img/sim_tmp.png', bbox_inches='tight')
    plt.show()
