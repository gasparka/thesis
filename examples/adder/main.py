from pyha.common.const import Const
from pyha.common.sfix import Sfix, resize, fixed_truncate
from pyha.common.hwsim import HW
import numpy as np
from pyha.simulation.simulation_interface import debug_assert_sim_match, SIM_GATE, plot_assert_sim_match, SIM_MODEL, \
    SIM_HW_MODEL, SIM_RTL
import matplotlib.pyplot as plt


class Adders(HW):
    def __init__(self):
        self.coef = 9

    def main(self, x):

        acc = x
        for i in range(4):
            acc = acc + i

        return acc

    def model_main(self, sample_in, sum_in):
        muls = np.array(sample_in) * self.coef
        sums = muls + sum_in
        return sums


def test_comb():
    dut = Adders()
    x = [1, 2, 3, 4, 5, 6]

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_HW_MODEL, SIM_RTL, SIM_GATE],
                               dir_path='/home/gaspar/git/thesis/playground')

    plt.figure(figsize=(8, 3))
    plt.plot(r[0], label='Model')
    plt.plot(r[1], label='Python simulation')
    plt.plot(r[2], label='RTL simulation')
    plt.plot(r[3], label='Quartus GATE simulation')

    plt.grid()
    plt.xlabel("Sample number")
    plt.ylabel("Value")
    plt.legend()
    plt.savefig('img/comb_sim.png', bbox_inches='tight')
    plt.show()

    print(r)


class MAC_seq(HW):
    def __init__(self):
        self.coef = 9
        self.y = 0

        # self._delay = 1

    def main(self, x, sum_in):
        mul = self.coef * x
        self.next.y = sum_in + mul
        return self.y

    def model_main(self, sample_in, sum_in):
        muls = np.array(sample_in) * self.coef
        sums = muls + sum_in
        return sums


def test_seq():
    dut = MAC_seq()
    x = [1, 2, 3, 4, 5, 6]
    sum_in = [1, 11, -9, 2, -40, -4]

    r = debug_assert_sim_match(dut, None, x, sum_in,
                               simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_RTL, SIM_GATE],
                               dir_path='/home/gaspar/git/thesis/playground')

    plt.figure(figsize=(8, 3))
    plt.plot(r[0], label='Model')
    plt.plot(r[1], label='Python simulation')
    plt.plot(r[2], label='RTL simulation')
    plt.plot(r[3], label='Quartus GATE simulation')

    plt.grid()
    plt.xlabel("Sample number")
    plt.ylabel("Value")
    plt.legend()
    plt.savefig('img/seq_sim_delay.png', bbox_inches='tight')
    plt.show()

    print(r)

