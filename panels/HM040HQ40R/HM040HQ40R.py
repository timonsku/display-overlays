# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Timon Skerutsch for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import sys
import os
import board
import busio
from adafruit_extended_bus import ExtendedI2C as I2C

# Pi5 DSI0
i2c = I2C(6)

# Pi5 DSI1
# i2c = I2C(4)

# Pi4<= DSI
# i2c = I2C(0)

from adafruit_icn6211 import *

# print("I2C devices found: ", [hex(i) for i in i2c.scan()])
icn = ICN6211(i2c)

# print(icn.device_id)
icn.test_mode = BIST_MODE.COLORBAR

icn.de_pol = True
icn.hs_pol = True
icn.vs_pol = True
icn.resolution = (480,800)
icn.horizontal_front_porch = 100
icn.horizontal_sync_width = 10
icn.horizontal_back_porch = 10
icn.vertical_front_porch = 10
icn.vertical_sync_width = 2
icn.vertical_back_porch = 20
icn.sync_event_delay = 128
icn.pd_ck_term_force = True
icn.pd_ck_hsrx_force = True
icn.out_rgb_swap = OUT_RGB_SWAP.RGB
icn.out_bit_swap = OUT_BIT_SWAP.MODE_666_7_2_to_0_5
icn.mipi_lane_num = MIPI_LANE_NUM.ONE_LANE
icn.pll_refsel = PLL_REF_SEL.MIPI_CLK

icn.pll_int_0 = 6 #PLL clock multiplier
icn.pll_out_divide_ratio = PLL_OUT_DIV_RATIO.DIV_8
icn.pll_ref_clk_divide_ratio = PLL_REF_CLK_DIV_RATIO.DIV_1
icn.pll_ref_clk_extra_divide = True
#icn.pll_cali_en = False
#icn.pll_cali_req = False

icn.mipi_force_0 = 0x20 #not documented, magic value from Linux driver
icn.pll_vco_isel = 0x20 #not documented, magic value from Linux driver
icn.clk_phase_sel = CLK_PHASE.PHASE_0
icn.pll_clkqen = True
icn.mipi_xor = True #not documented what it does, taken from config tool

icn.save_config()

icn.soft_reset()
icn.dump_registers()
icn.print_errors()
icn.reset_errors()

print(icn.pll_out_divide_ratio, icn.pll_ref_clk_divide_ratio, icn.pll_ref_clk_extra_divide)

all_registers = [0x00,0x01,0x02,0x03,0x08,0x09,0x10,0x11,0x14,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28,0x29,0x2a,0x31,0x32,0x33,0x34,0x35,0x36,0x51,0x56,0x63,0x64,0x65,0x66,0x67,0x68,0x69,0x6a,0x6b,0x7a,0x7b,0x7c,0x7d,0x80,0x81,0x84,0x85,0x86,0x87,0x90,0x91,0x92,0x94,0x95,0x96,0x97,0x99,0x9a,0xb5,0xb6]
_result = bytearray(1)
_reg = bytearray(1)
for reg in all_registers:
  _reg[0] = reg
  icn.i2c_device.write_then_readinto(_reg, _result)
  print("0x{:02x}, 0x{:02x},".format(_reg[0], _result[0]))



