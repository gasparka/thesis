from pyha.common.const import Const
from pyha.common.sfix import Sfix, resize, fixed_truncate
from pyha.common.hwsim import HW
import numpy as np
from pyha.simulation.simulation_interface import debug_assert_sim_match


class Name(HW):
    def __init__(self):
        self.instance_member = 0

    def main(self, b):
        ret0, ret1 = self.lol(b)
        # return ret0

    def lol(self, a):
        b = a
        return a, b


def test_basic():
    from pyha.simulation.simulation_interface import assert_sim_match, SIM_HW_MODEL, SIM_RTL
    dut = Name()
    inputs = [1, 2]

    assert_sim_match(dut, None, inputs,
                     simulations=[SIM_HW_MODEL, SIM_RTL],
                     rtol=1e-4,
                     dir_path='/home/gaspar/git/thesis/playground')


if __name__ == '__main__':
    test_basic()
