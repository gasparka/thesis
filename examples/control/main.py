from pyha.common.const import Const
from pyha.common.sfix import Sfix, resize, fixed_truncate
from pyha.common.hwsim import HW
import numpy as np
from pyha.simulation.simulation_interface import debug_assert_sim_match, SIM_GATE, plot_assert_sim_match, SIM_MODEL, \
    SIM_HW_MODEL, SIM_RTL
import matplotlib.pyplot as plt


class If(HW):

    def main(self, x, condition):
        if condition == 0:
            y = x + 3
        else:
            y = x + 1

        return y

    def model_main(self, xl, conditionl):
        yl = [x + 1 if c else x + 3 for x, c in zip(xl, conditionl)]
        return yl


def test_comb():
    dut = If()
    x = [1, 2, 2, 3, 3, 1, 1]
    condition = [0, 1, 2, 3, 0, 1, 2]

    r = debug_assert_sim_match(dut, None, x, condition,
                               simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_RTL, SIM_GATE],
                               dir_path='/home/gaspar/git/thesis/playground')

    plt.figure(figsize=(8, 2))
    plt.plot(x, label='x')
    plt.plot(r[0], label='y: Model')
    plt.plot(r[1], label='y: Pyha')
    plt.plot(r[2], label='y: RTL')
    plt.plot(r[2], label='y: GATE')
    plt.legend(loc='upper right')

    plt.grid()
    plt.xlabel("Sample number")
    plt.ylabel("Value")
    plt.savefig('img/add_sim.png', bbox_inches='tight')
    plt.show()

    print(r)


class For(HW):
    def main(self, x):
        y = x
        for i in range(4):  # iterate from 0 to 3
            y = y + i

        return y

    def model_main(self, xl):
        return []



def test_for():
    dut = For()
    x = [1, 2, 2, 3, 3, 1, 1]
    condition = [0, 1, 2, 3, 0, 1, 2]

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_RTL],
                               dir_path='/home/gaspar/git/thesis/playground')

    plt.figure(figsize=(8, 2))
    plt.plot(x, label='x')
    plt.plot(r[0], label='y: Model')
    plt.plot(r[1], label='y: Pyha')
    plt.plot(r[2], label='y: RTL')
    plt.plot(r[2], label='y: GATE')
    plt.legend(loc='upper right')

    plt.grid()
    plt.xlabel("Sample number")
    plt.ylabel("Value")
    # plt.savefig('img/add_sim.png', bbox_inches='tight')
    plt.show()

    print(r)


class Functions(HW):
    def adder(self, x, b):
        y = x + b
        return y

    def main(self, x):
        y = self.adder(x, 1)
        return y

    def model_main(self, xl):
        return []



def test_functions():
    dut = Functions()
    x = [1, 2, 2, 3, 3, 1, 1]
    condition = [0, 1, 2, 3, 0, 1, 2]

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_RTL, SIM_GATE],
                               dir_path='/home/gaspar/git/thesis/playground')

    plt.figure(figsize=(8, 2))
    plt.plot(x, label='x')
    plt.plot(r[0], label='y: Model')
    plt.plot(r[1], label='y: Pyha')
    plt.plot(r[2], label='y: RTL')
    plt.plot(r[2], label='y: GATE')
    plt.legend(loc='upper right')

    plt.grid()
    plt.xlabel("Sample number")
    plt.ylabel("Value")
    plt.savefig('img/add_sim.png', bbox_inches='tight')
    plt.show()

    print(r)