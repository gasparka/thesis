from pyha.common.const import Const
from pyha.common.sfix import Sfix, resize, fixed_truncate
from pyha.common.hwsim import HW
import numpy as np
from pyha.simulation.simulation_interface import debug_assert_sim_match, SIM_GATE, plot_assert_sim_match, SIM_MODEL


class MAC_comb(HW):
    def __init__(self):
        self.coef = 123

    def main(self, x, sum_in):
        mul = self.coef * x
        y = sum_in + mul
        return y

    def model_main(self, sample_in, sum_in):
        muls = np.array(sample_in) * self.coef
        sums = muls + sum_in
        return sums


def test_comb():
    from pyha.simulation.simulation_interface import assert_sim_match, SIM_HW_MODEL, SIM_RTL
    dut = MAC_comb()
    inputs = [1, 2, 3, 4, 5, 6, 7, 8]
    si = [0] * len(inputs)

    r = debug_assert_sim_match(dut, None, inputs, si,
                     simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_GATE],
                     rtol=1e-4,
                     dir_path='/home/gaspar/git/thesis/playground')

    print(r)



class MAC(HW):
    def __init__(self):
        self.coef = 123
        self.mul = 0
        self.acc = 0

        self._delay = 2

    def main(self, a, sum_in):

        self.next.mul = self.coef * a
        self.next.acc = sum_in + self.mul
        return self.acc

    def model_main(self, sample_in, sum_in):
        import numpy as np

        muls = sample_in * self.coef
        sums = muls + sum_in
        return sums

def test_basic():
    from pyha.simulation.simulation_interface import assert_sim_match, SIM_HW_MODEL, SIM_RTL
    dut = MAC()
    inputs = [1, 2, 3, 4, 5, 6, 7, 8]
    si = [0] * len(inputs)

    r = debug_assert_sim_match(dut, None, inputs, si,
                     simulations=[SIM_MODEL, SIM_HW_MODEL],
                     rtol=1e-4,
                     dir_path='/home/gaspar/git/thesis/playground')

    print(r)

if __name__ == '__main__':
    test_basic()
