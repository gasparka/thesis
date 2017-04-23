from pyha.common.hwsim import HW

from examples.moving_average.model import MovingAverage


class DCRemoval(HW):
    def __init__(self, window_len, cascades):
        self.mavg = [MovingAverage(window_len) for _ in range(cascades)]

        self._delay = self.mavg[0]._delay * cascades

    def main(self, x):
        tmp = x
        for mav in self.mavg:
            tmp = mav.main(tmp)

        y = x - tmp
        return y

    def model_main(self, xl):
        tmp = xl
        for mav in self.mavg:
            tmp = mav.model_main(tmp)

        y = xl - tmp
        return y
