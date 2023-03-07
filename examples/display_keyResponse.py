# -*- coding:utf-8 -*-
"""!
  @file display_keyResponse.py
  @brief 按键keyA和keyB测试
  @n after clear screen, click keyA or keyB, you can see "A" or "B" printed on your device
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
import threading

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

# get gpio interface
GPIO = DFRobot_RPi_Eink_Display.GPIO
KEY_A = 21
KEY_B = 20

eink_display = DFRobot_RPi_Eink_Display.DFRobot_RPi_Eink_Display(RASPBERRY_SPI_BUS, RASPBERRY_SPI_DEV, RASPBERRY_PIN_CS,
                                                                 RASPBERRY_PIN_CD, RASPBERRY_PIN_BUSY,
                                                                 RASPBERRY_PIN_RST)  # create eink_display object

key_a_lock = threading.Lock()  # key A threading lock
key_b_lock = threading.Lock()  # key B threading lock
key_a_flag = False  # key A flag
key_b_flag = False  # key B flag

# key A callback
def key_a_call_back():
    global key_a_lock, key_a_flag
    key_a_lock.acquire()  # wait key A lock release
    key_a_flag = True
    key_a_lock.release()


# key B callback
def key_b_call_back():
    global key_b_lock, key_b_flag
    key_b_lock.acquire()  # wait key B lock release
    key_b_flag = True
    key_b_lock.release()


def main():
    global key_a_flag, key_b_flag, key_a_lock, key_b_lock

    # config extension fonts
    ft = DFRobot_RPi_Eink_Display.FreetypeHelper(fontFilePath)
    ft.set_dis_lower_limit(96)  # set display lower limit, adjust this to effect fonts color depth
    eink_display.set_ex_fonts(ft)  # init with fonts file
    eink_display.set_ex_fonts_fmt(32, 32)  # set extension fonts width and height

    # config keyA and keyB
    key_a = GPIO(KEY_A, GPIO.IN)  # set key to input
    key_b = GPIO(KEY_B, GPIO.IN)  # set key to input
    key_a.set_interrupt(GPIO.FALLING, key_a_call_back)  # set key interrupt callback
    key_b.set_interrupt(GPIO.FALLING, key_b_call_back)  # set key interrupt callback

    # clear screen
    eink_display.begin()
    eink_display.clear_screen()
    eink_display.set_text_format(1, eink_display.BLACK, eink_display.WHITE, 2,
                                 0)  # set text size, color, background, interval row, interval col

    key_count = 0

    # key test
    eink_display.print_str("key test")
    eink_display.flush(eink_display.PART)
    eink_display.set_text_cursor(0, 32)

    while True:
        if key_a_flag:
            key_a_lock.acquire()  # wait key A release
            key_a_flag = False
            key_a_lock.release()
            key_count += 1
            eink_display.print_str("A")
            eink_display.flush(eink_display.PART)
        if key_b_flag:
            key_b_lock.acquire()  # wait key B release
            key_b_flag = False
            key_b_lock.release()
            key_count += 1
            eink_display.print_str("B")
            eink_display.flush(eink_display.PART)
        if key_count >= 16:
            key_count = 0
            eink_display.clear(eink_display.WHITE)
            eink_display.set_text_cursor(0, 0)
            eink_display.print_str("key test")
            eink_display.flush(eink_display.PART)
            eink_display.set_text_cursor(0, 32)  # set text cursor to origin and clear

        time.sleep(0.01)


if __name__ == "__main__":
    main()
