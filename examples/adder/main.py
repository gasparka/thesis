from pyha.common.const import Const
from pyha.common.sfix import Sfix, resize, fixed_truncate
from pyha.common.hwsim import HW
import numpy as np
from pyha.simulation.simulation_interface import debug_assert_sim_match, SIM_GATE, plot_assert_sim_match, SIM_MODEL, \
    SIM_HW_MODEL, SIM_RTL
import matplotlib.pyplot as plt


class Basic(HW):
    def main(self, x):
        a = x + 1 + 3
        b = a * 314
        return a, b

    def model_main(self, xl):
        al = [x + 1 + 3 for x in xl]
        bl = [a + 2 for a in al]
        return al, bl


def test_comb():
    dut = Basic()
    x = [1, 2, 2, 3, 3, 1, 1]

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_RTL, SIM_GATE],
                               dir_path='/home/gaspar/git/thesis/playground')

    fig, axes = plt.subplots(2, 1, sharex=True, sharey=True, figsize=(8, 3.5))
    # add a big axes, hide frame
    fig.add_subplot(111, frameon=False)
    axes[0].plot(x, label='x')
    axes[0].plot(r[0][0], label='a: Model')
    axes[0].plot(r[1][0], label='a: Pyha')
    axes[0].plot(r[2][0], label='a: RTL')
    axes[0].plot(r[2][0], label='a: GATE')
    axes[0].legend(loc='upper right')
    axes[0].set_yticks([1, 3, 5, 7, 9])
    axes[0].grid()

    axes[1].plot(x, label='x')
    axes[1].plot(r[0][1], label='b: Model')
    axes[1].plot(r[1][1], label='b: Pyha')
    axes[1].plot(r[2][1], label='b: RTL')
    axes[1].plot(r[2][1], label='b: GATE')
    axes[1].legend(loc='upper right')
    axes[1].grid()

    # hide tick and tick label of the big axes
    plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
    plt.xlabel("Sample number")
    plt.ylabel("Amplitude")
    plt.yticks([1,2,3,4,5])
    plt.savefig('img/add_multi_sim.png', bbox_inches='tight')

    plt.show()

    print(r)


class Adder(HW):
    def main(self, x):
        y = x + 1
        return y

    def model_main(self, xl):
        yl = [x + 1 for x in xl]
        return yl


def test_adder():
    dut = Adder()
    x = [1, 2, 2, 3, 3, 1, 1]

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
    plt.savefig('img/add_sim.png', bbox_inches='tight')
    plt.show()

    print(r)


def test_add():
    x =      [1, 2, 2, 3, 3, 1, 1]
    expect = [2, 3, 3, 4, 4, 2, 2]

    dut = Adder()
    assert_simulation(dut, expect, x)