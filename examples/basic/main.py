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
        if a == 9:
            b = 0
        return a, b

    def model_main(self, xl):
        return []
        yl = [x + 1 if c else x + 3 for x, c in zip(xl, conditionl)]
        return yl


def test_if2():
    dut = Basic()
    x = [1, 2, 3, 4, 5, 6, 7]

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
