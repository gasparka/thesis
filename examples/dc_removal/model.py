from pyha.common.hwsim import HW
from pyha.common.sfix import Sfix
from pyha.simulation.simulation_interface import assert_sim_match, debug_assert_sim_match, plot_assert_sim_match

from examples.moving_average.model import MovingAverage


class DCRemoval(HW):
    def __init__(self, window_len, cascades):
        self.mavg = [MovingAverage(window_len) for _ in range(cascades)]
        self.y = Sfix(0, 0, -17)

        self._delay = 1 + self.mavg[0]._delay * cascades

    def main(self, x):
        tmp = x
        for mav in self.mavg:
            tmp = mav.main(tmp)

        self.next.y = x - tmp
        return self.y

    def model_main(self, xl):
        tmp = xl
        for mav in self.mavg:
            tmp = mav.model_main(tmp)

        y = xl - tmp
        return y


def test_quad4_len32():
    x = [0.5] * 64 + [-0.5] * 64

    dut = DCRemoval(256, 4)
    plot_assert_sim_match(dut, None, x,
                     dir_path='/home/gaspar/git/thesis/playground')


