from pyha.common.const import Const
from pyha.common.sfix import Sfix, resize, fixed_truncate
from pyha.common.hwsim import HW
import numpy as np
from pyha.simulation.simulation_interface import debug_assert_sim_match, SIM_GATE, plot_assert_sim_match, SIM_MODEL, \
    SIM_HW_MODEL, SIM_RTL
import matplotlib.pyplot as plt


class LastAcc(HW):
    def __init__(self):
        # registers
        self.shr = [0, 0, 0, 0]
        self.y = 0

        # module delay
        self._delay = 2

    def main(self, x):
        # add new element to shift register
        self.next.shr = [x] + self.shr[:-1]

        sum = 0
        for a in self.shr:
            sum = sum + a

        self.next.y = sum
        return self.y

    def model_main(self, xl):

        xl = [0, 0, 0] + xl
        y = []
        for i in range(len(xl)-3):
            s = sum(xl[i: i+4])
            y.append(s)

        return y


def test_lastacc():
    dut = LastAcc()
    x = [0, 1, 2, 3, 4, 3, 2, 1, 0]

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_RTL, SIM_GATE],
                               dir_path='/home/gaspar/git/thesis/playground')



    plt.figure(figsize=(8, 2))
    plt.stem(x, label='x', basefmt=" ")
    plt.plot(r[0], label='y: Model')
    plt.plot(r[1], label='y: Pyha')
    plt.plot(r[2], label='y: RTL')
    plt.plot(r[3], label='y: GATE')

    plt.grid()
    plt.xlabel("Sample number")
    plt.ylabel("Value")
    plt.legend()
    plt.savefig('img/sim_tmp.png', bbox_inches='tight')
    plt.show()

    print(r)

