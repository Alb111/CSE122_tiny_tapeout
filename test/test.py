# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


def pack_inputs(left, right):
    """
    left  = 6-bit value
    right = 6-bit value

    ui_in[5:0]  = left
    ui_in[7:6]  = right[5:4]
    uio_in[3:0] = right[3:0]
    """
    ui  = (left & 0x3F) | ((right >> 4) << 6)
    uio = (right & 0x0F)
    return ui, uio


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # 100 kHz clock
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # -----------------------------
    # Test multiple cases
    # -----------------------------
    test_vectors = [
        (0, 0),
        (10, 20),
        (63, 63),
        (5, 7),
        (12, 3),
    ]

    for left, right in test_vectors:
        ui, uio = pack_inputs(left, right)

        # valid_i = uio[4]
        # ready_i = uio[5]
        uio |= (1 << 4)   # valid_i = 1
        uio |= (1 << 5)   # ready_i = 1

        dut.ui_in.value = ui
        dut.uio_in.value = uio

        await ClockCycles(dut.clk, 1)

        expected = (left + right) >> 1

        actual = dut.uo_out.value.integer

        dut._log.info(
            f"Left={left} Right={right} "
            f"Expected={expected} Got={actual}"
        )

        assert actual == expected, \
            f"Mismatch: expected {expected}, got {actual}"

    dut._log.info("All tests passed ✔")
