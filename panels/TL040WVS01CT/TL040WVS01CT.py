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
# icn.test_mode = BIST_MODE.COLORBAR

icn.de_pol = True
icn.resolution = (480,480)
icn.horizontal_front_porch = 4
icn.horizontal_sync_width = 60
icn.horizontal_back_porch = 2
icn.vertical_front_porch = 7
icn.vertical_sync_width = 30
icn.vertical_back_porch = 9
icn.sync_event_delay = 128
icn.pd_ck_term_force = True
icn.pd_ck_hsrx_force = True
icn.out_rgb_swap = OUT_RGB_SWAP.RGB
icn.out_bit_swap = OUT_BIT_SWAP.MODE_666_5_0_to_5_0
icn.mipi_lane_num = MIPI_LANE_NUM.ONE_LANE
icn.pll_refsel = PLL_REF_SEL.MIPI_CLK
icn.pll_int_0 = 3 #PLL clock
icn.pll_out_divide_ratio = PLL_OUT_DIV_RATIO.DIV_2
icn.pll_ref_clk_divide_ratio = PLL_REF_CLK_DIV_RATIO.DIV_1
icn.pll_ref_clk_extra_divide = True
icn.mipi_force_0 = 0x20 #not documented, magic value from Linux driver
icn.pll_vco_isel = 0x20 #not documented, magic value from Linux driver
icn.clk_phase_sel = CLK_PHASE.PHASE_0
icn.pll_clkqen = True
icn.mipi_xor = True #not documented what it does, taken from config tool

icn.save_config()

# icn.soft_reset()
icn.dump_registers()
icn.print_errors()
icn.reset_errors()

