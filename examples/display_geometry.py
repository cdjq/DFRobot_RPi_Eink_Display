# -*- coding:utf-8 -*-
"""!
  @file display_geometry.py
  @brief display basic geometry, such as line, rectangle, triangle, circle and pixel：
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @License     The MIT License (MIT)
  @author      fengli(li.feng@dfrobot.com)
  @maintainer  NephogramX(longjian.xu@dfrobot.com)
  @version     V1.0
  @date        2023.2.20
  @url         https://github.com/DFRobot/DFRobot_RPi_Eink_Display
"""
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # set system path to top

from DFRobot_RPi_Eink_Display import DFRobot_RPi_Eink_Display

# peripheral params
RASPBERRY_SPI_BUS = 0
RASPBERRY_SPI_DEV = 0
RASPBERRY_PIN_CS = 27
RASPBERRY_PIN_CD = 17
RASPBERRY_PIN_BUSY = 4
RASPBERRY_PIN_RST = 26

eink_display = DFRobot_RPi_Eink_Display(RASPBERRY_SPI_BUS, RASPBERRY_SPI_DEV, RASPBERRY_PIN_CS, RASPBERRY_PIN_CD,
                                        RASPBERRY_PIN_BUSY, RASPBERRY_PIN_RST)  # create eink_display object


def main():
    # clear screen and set line width to 3
    eink_display.begin()
    eink_display.clear_screen()
    # eink_display.set_line_width(3)
    time.sleep(1)
    eink_display.read_id()

    for i in range(10, 50):
        eink_display.pixel(10, i * 2, eink_display.BLACK)

    eink_display.flush(eink_display.PART)
    eink_display.line(20, 20, 20, 100, eink_display.BLACK)
    eink_display.flush(eink_display.PART)
    eink_display.line(40, 20, 60, 100, eink_display.BLACK)
    eink_display.flush(eink_display.PART)
    eink_display.line(60, 20, 40, 100, eink_display.BLACK)
    eink_display.flush(eink_display.PART)
    eink_display.hollow_rect(80, 20, 40, 80, eink_display.BLACK)
    eink_display.flush(eink_display.PART)
    eink_display.filled_rect(90, 30, 20, 60, eink_display.BLACK)
    eink_display.flush(eink_display.PART)
    eink_display.hollow_circle(150, 30, 20, eink_display.BLACK)
    eink_display.flush(eink_display.PART)
    eink_display.filled_circle(150, 30, 15, eink_display.BLACK)
    eink_display.flush(eink_display.PART)
    eink_display.hollow_rounded_rectangle(130, 60, 40, 40, 10, eink_display.BLACK)
    eink_display.flush(eink_display.PART)
    eink_display.filled_rounded_rectangle(140, 70, 20, 20, 5, eink_display.BLACK)
    eink_display.flush(eink_display.PART)
    eink_display.hollow_triangle(210, 20, 190, 100, 230, 100, eink_display.BLACK)
    eink_display.flush(eink_display.PART)
    eink_display.filled_triangle(210, 40, 200, 90, 220, 90, eink_display.BLACK)
    eink_display.flush(eink_display.PART)


if __name__ == "__main__":
    main()
