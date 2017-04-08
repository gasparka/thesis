from pyha.common.const import Const
from pyha.common.sfix import Sfix, resize, fixed_truncate
from pyha.common.hwsim import HW
import numpy as np
from pyha.simulation.simulation_interface import debug_assert_sim_match, SIM_GATE, plot_assert_sim_match


class MAC(HW):
    def __init__(self, coef):
        self.coef = coef
        self.mul = 0
        self.acc = 0

    def main(self, a):
        self.next.mul = self.coef * a
        self.next.acc = self.acc + self.mul
        return self.acc


class ReuseStack(HW):
    def __init__(self):
        self.mac0 = MAC(123)
        self.mac1 = MAC(321)

    def main(self, a):
        out = self.mac0.main(a)
        out = self.mac1.main(out)
        return out


class ReuseParallel(HW):
    def __init__(self):
        self.mac0 = MAC(123)
        self.mac1 = MAC(321)

    def main(self, a):
        out0 = self.mac0.main(a)
        out1 = self.mac1.main(a)
        return out0, out1

def test_stack():
    from pyha.simulation.simulation_interface import assert_sim_match, SIM_HW_MODEL, SIM_RTL
    dut = ReuseStack()
    inputs = [1, 2, 3, 4, 5, 6, 7, 8]

    r = debug_assert_sim_match(dut, None, inputs,
                               simulations=[SIM_HW_MODEL, SIM_RTL, SIM_GATE],
                               rtol=1e-4,
                               dir_path='/home/gaspar/git/thesis/playground')

    print(r)


def test_parallel():
    from pyha.simulation.simulation_interface import assert_sim_match, SIM_HW_MODEL, SIM_RTL
    dut = ReuseParallel()
    inputs = [1, 2, 3, 4, 5, 6, 7, 8]

    r = debug_assert_sim_match(dut, None, inputs,
                               simulations=[SIM_HW_MODEL, SIM_RTL, SIM_GATE],
                               rtol=1e-4,
                               dir_path='/home/gaspar/git/thesis/playground')

    print(r)

