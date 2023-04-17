# -*- coding:utf-8 -*-
"""!
  @file display_multiLingual.py
  @brief Font example 
  @n print with fonts file, Different files will have different display effects
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

import DFRobot_RPi_Eink_Display

fontFilePath = "./resources/wqydkzh.ttf"  # fonts file

# peripheral params
RASPBERRY_SPI_BUS = 0
RASPBERRY_SPI_DEV = 0
RASPBERRY_PIN_CS = 27
RASPBERRY_PIN_CD = 17
RASPBERRY_PIN_BUSY = 4
RASPBERRY_PIN_RST = 26

eink_display = DFRobot_RPi_Eink_Display.DFRobot_RPi_Eink_Display(RASPBERRY_SPI_BUS, RASPBERRY_SPI_DEV, RASPBERRY_PIN_CS,
                                                                 RASPBERRY_PIN_CD, RASPBERRY_PIN_BUSY, RASPBERRY_PIN_RST
                                                                 )  # create eink_display object


def main():
    # clear screen
    eink_display.begin()
    eink_display.clear_screen()

    # config extension fonts
    ft = DFRobot_RPi_Eink_Display.FreetypeHelper(fontFilePath)
    ft.set_dis_lower_limit(96)  # set display lower limit, adjust this to effect fonts color depth
    eink_display.set_ex_fonts(ft)  # init with fonts file
    eink_display.set_text_format(1, eink_display.BLACK, eink_display.WHITE, 2, 2)
    eink_display.set_ex_fonts_fmt(24, 24)  # set extension fonts width and height

    eink_display.set_text_cursor(10, 10)
    eink_display.print_str_ln("中国  北京")
    eink_display.flush(eink_display.PART)
    eink_display.print_str_ln("USA   Washington")
    eink_display.flush(eink_display.PART)
    eink_display.print_str_ln("日本  東京")
    eink_display.flush(eink_display.PART)
    eink_display.print_str_ln("韩国  서울")
    eink_display.flush(eink_display.PART)

    time.sleep(1)


if __name__ == "__main__":
    main()
