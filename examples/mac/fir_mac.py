from pyha.common.const import Const
from pyha.common.sfix import Sfix, resize, fixed_truncate
from pyha.common.hwsim import HW
import numpy as np
from pyha.simulation.simulation_interface import debug_assert_sim_match, SIM_GATE, plot_assert_sim_match, SIM_MODEL


class Simple(HW):
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

        muls = np.array(sample_in) * self.coef
        sums = muls + sum_in
        return sums


def test_basic():
    from pyha.simulation.simulation_interface import assert_sim_match, SIM_HW_MODEL, SIM_RTL
    dut = Simple()
    inputs = [1, 2, 3, 4, 5, 6, 7, 8]
    si = [0] * len(inputs)

    r = debug_assert_sim_match(dut, None, inputs, si,
                     simulations=[SIM_MODEL, SIM_HW_MODEL],
                     rtol=1e-4,
                     dir_path='/home/gaspar/git/thesis/playground')

    print(r)

if __name__ == '__main__':
    test_basic()
