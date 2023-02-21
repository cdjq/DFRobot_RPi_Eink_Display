# -*- coding:utf-8 -*-
"""!
  @file display_printString.py
  @brief 在屏幕上显示字符，字符串。
  @n print with fonts file, Different files will have different display effects
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @License     The MIT License (MIT)
  @author      fengli(li.feng@dfrobot.com)
  @version     V3.0
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
epaper = DFRobot_RPi_Eink_Display.DFRobot_RPi_Eink_Display(RASPBERRY_SPI_BUS, RASPBERRY_SPI_DEV, RASPBERRY_PIN_CS,
                                                           RASPBERRY_PIN_CD, RASPBERRY_PIN_BUSY, RASPBERRY_PIN_RST
                                                           )  # create eink_display object


def main():
    # clear screen
    epaper.begin()
    epaper.clear_screen()

    # config extension fonts
    ft = DFRobot_RPi_Eink_Display.FreetypeHelper(fontFilePath)
    ft.set_dis_lower_limit(112)  # set display lower limit, adjust this to effect fonts color depth
    epaper.set_ex_fonts(ft)  # init with fonts file
    epaper.set_text_format(1, epaper.BLACK, epaper.WHITE, 1, 1)

    # print test
    epaper.set_ex_fonts_fmt(32, 32)  # set extension fonts width and height
    epaper.set_text_cursor(69, 0)
    epaper.print_str("DFRobot")
    epaper.flush(epaper.PART)
    time.sleep(1)

    epaper.set_ex_fonts_fmt(24, 24)  # set extension fonts width and height
    epaper.set_text_cursor(0, 32)
    epaper.print_str("品牌简介")
    epaper.flush(epaper.PART)
    time.sleep(1)

    epaper.set_ex_fonts_fmt(16, 16)  # set extension fonts width and height
    epaper.set_text_cursor(0, 60)
    epaper.print_str("    DFRobot是上海智位机器人股份有限公司旗下注册商标")
    epaper.flush(epaper.PART)
    time.sleep(1)

    for i in range(8):
        epaper.set_ex_fonts_fmt(16, 16)  # set extension fonts width and height
        epaper.set_text_cursor(0, 96)
        epaper.print_str("abcdefghijklmnopqrstuvwxyz")
        epaper.flush(epaper.PART)
        time.sleep(1)

        epaper.set_ex_fonts_fmt(16, 16)  # set extension fonts width and height
        epaper.set_text_cursor(0, 96)
        epaper.print_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        epaper.flush(epaper.PART)
        time.sleep(1)


if __name__ == "__main__":
    main()
