# -*- coding:utf-8 -*-
"""!
  @file display_cleanup.py
  @brief 清空显示内容
  @n 实验现象：该程序可以清除墨水屏的显示内容，使屏幕恢复到最初状态
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @License     The MIT License (MIT)
  @author      fengli(li.feng@dfrobot.com)
  @version     V3.0
  @date        2023.2.20
  @url         https://github.com/DFRobot/DFRobot_RPi_Eink_Display
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # set system path to top

from DFRobot_RPi_Eink_Display import DFRobot_RPi_Eink_Display

# peripheral params
RASPBERRY_SPI_BUS = 0
RASPBERRY_SPI_DEV = 0
RASPBERRY_PIN_CS = 27
RASPBERRY_PIN_CD = 17
RASPBERRY_PIN_BUSY = 4
RASPBERRY_PIN_RST = 26

eink_display = DFRobot_RPi_Eink_Display(RASPBERRY_SPI_BUS, RASPBERRY_SPI_DEV, RASPBERRY_PIN_CS,
                                        RASPBERRY_PIN_CD, RASPBERRY_PIN_BUSY,
                                        RASPBERRY_PIN_RST)  # create E-ink display object


def main():
    eink_display.begin()
    eink_display.clear_screen()


if __name__ == "__main__":
    main()