import pytest
from pyha.simulation.simulation_interface import assert_sim_match
import numpy as np
from examples.dc_removal.model import DCRemoval
import matplotlib.pyplot as plt


def test_basic():
    x = [0.5] * 16 + [-0.5] * 16

    dut = DCRemoval(8)
    assert_sim_match(dut, None, x)

def test_quad4_len32():
    x = [0.5] * 64 + [-0.5] * 64

    dut = DCRemoval(32)
    assert_sim_match(dut, None, x, dir_path='/home/gaspar/git/thesis/examples/dc_removal/conversion')


def test_saturation():
    pytest.xfail('Fails as numbers go out of [-1,1] range')
    x = [1.] * 16 + [-1.] * 16
    expected = [0.984375, 0.953125, 0.90625, 0.84375, 0.765625, 0.671875,
                0.5625, 0.4375, 0.328125, 0.234375, 0.15625, 0.09375,
                0.046875, 0.015625, 0., 0., -1.96875, -1.90625,
                -1.8125, -1.6875, -1.53125, -1.34375, -1.125, -0.875,
                -0.65625, -0.46875, -0.3125, -0.1875, -0.09375, -0.03125,
                0., 0.]

    dut = DCRemoval(8)

    assert_sim_match(dut, expected, x)





