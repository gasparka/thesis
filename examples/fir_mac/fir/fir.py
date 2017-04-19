from pyha.common.const import Const
from pyha.common.hwsim import HW
from pyha.common.sfix import Sfix, fixed_truncate, fixed_wrap
from pyha.common.util import plot_freqz
from pyha.simulation.simulation_interface import debug_assert_sim_match, SIM_HW_MODEL, SIM_RTL

from scipy import signal
import numpy as np
import numpy as np
from pyha.simulation.simulation_interface import debug_assert_sim_match, SIM_GATE, plot_assert_sim_match, SIM_MODEL, \
    SIM_HW_MODEL, SIM_RTL
import matplotlib.pyplot as plt


class MAC(HW):
    def __init__(self, coef):
        self.coef = Sfix(coef, 0, -17)
        self.acc = Sfix(left=1, round_style=fixed_truncate, overflow_style=fixed_wrap)

        self._delay = 1

    def main(self, a, sum_in):
        mul = self.coef * a
        self.next.acc = mul + sum_in
        return self.acc

    def model_main(self, a):
        import numpy as np

        muls = np.array(a) * self.coef
        return np.cumsum(muls)


class FIR_atom(HW):
    def __init__(self, taps):
        self.taps = taps

        # registers
        self.mac = [MAC(x) for x in reversed(self.taps)]
        self.y = Sfix(0, 0, -17, round_style=fixed_truncate)

        # constants
        self._delay = 2

    def filter(self, x):
        sum_in = Sfix(0.0, 1, -34)
        for mav in self.mac:
            sum_in = mav.main(x, sum_in)

        return sum_in

    def main(self, x):
        fir_out = self.filter(x)

        self.next.y = fir_out
        return self.y

    def model_main(self, x):
        return signal.lfilter(self.taps, [1.0], x)


def test_demo():
    # design filter
    b = signal.remez(4, [0, 0.1, 0.3, 0.5], [1, 0])

    w, h = signal.freqz(b)

    plt.figure(figsize=(8, 2))
    plt.title('Frequency response')

    plt.plot(w / np.pi, 20 * np.log10(abs(h)))
    plt.ylabel('Amplitude [dB]')
    plt.xlabel('Normalized frequency')

    plt.grid()
    plt.savefig('img/fir_freqz.png', bbox_inches='tight')
    plt.show()

    dut = FIR_atom(b)
    x = np.random.uniform(-1, 1, 64)

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_RTL, SIM_GATE],
                               dir_path='/home/gaspar/git/thesis/playground')

    plt.figure(figsize=(8, 2))
    plt.plot(x, label='Raw input')
    plt.plot(r[0], label='Model')
    plt.plot(r[1], label='Python simulation')
    plt.plot(r[2], label='RTL simulation')
    plt.plot(r[3], label='Quartus GATE simulation')

    plt.grid()
    plt.xlabel("Sample number")
    plt.ylabel("Value")
    plt.legend()
    plt.savefig('img/fir_sim.png', bbox_inches='tight')
    plt.show()
