# -*- coding: utf-8 -*
"""!
  @file DFRobot_RPi_Eink_Display.py
  @brief Defines the basic structure of the DFRobot_RPi_Eink_Display class, implements basic methods, and provides some development tools for convenience
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author      fengli(li.feng@dfrobot.com)
  @maintainer  NephogramX(longjian.xu@dfrobot.com)
  @version     V1.0
  @date        2023.2.20
  @url         https://github.com/DFRobot/DFRobot_RPi_Eink_Display
"""

import sys
import time
import spidev
import freetype
import RPi.GPIO as RPIGPIO

RPIGPIO.setmode(RPIGPIO.BCM)
RPIGPIO.setwarnings(False)

fonts_6_8 = {
    "fonts": {  # left to right, msb to bottom, lsb to top
        " ": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        "!": [0x00, 0x00, 0x5F, 0x00, 0x00, 0x00],
        "\"": [0x00, 0x07, 0x00, 0x07, 0x00, 0x00],
        "#": [0x14, 0x7F, 0x14, 0x7F, 0x14, 0x00],
        "$": [0x24, 0x2A, 0x7F, 0x2A, 0x12, 0x00],
        "%": [0x23, 0x13, 0x08, 0x64, 0x62, 0x00],
        "&": [0x36, 0x49, 0x56, 0x20, 0x50, 0x00],
        "'": [0x00, 0x08, 0x07, 0x03, 0x00, 0x00],
        "(": [0x00, 0x1C, 0x22, 0x41, 0x00, 0x00],
        ")": [0x00, 0x41, 0x22, 0x1C, 0x00, 0x00],
        "*": [0x24, 0x18, 0x7E, 0x18, 0x24, 0x00],
        "+": [0x08, 0x08, 0x3E, 0x08, 0x08, 0x00],
        ",": [0x00, 0x80, 0x70, 0x30, 0x00, 0x00],
        "-": [0x08, 0x08, 0x08, 0x08, 0x08, 0x00],
        ".": [0x00, 0x00, 0x60, 0x60, 0x00, 0x00],
        "/": [0x20, 0x10, 0x08, 0x04, 0x02, 0x00],
        "0": [0x3E, 0x41, 0x49, 0x41, 0x3E, 0x00],
        "1": [0x00, 0x42, 0x7F, 0x40, 0x00, 0x00],
        "2": [0x72, 0x49, 0x49, 0x49, 0x46, 0x00],
        "3": [0x21, 0x41, 0x49, 0x4D, 0x32, 0x00],
        "4": [0x18, 0x14, 0x12, 0x7F, 0x10, 0x00],
        "5": [0x27, 0x45, 0x45, 0x45, 0x38, 0x00],
        "6": [0x3C, 0x4A, 0x49, 0x49, 0x31, 0x00],
        "7": [0x41, 0x21, 0x11, 0x09, 0x07, 0x00],
        "8": [0x36, 0x49, 0x49, 0x49, 0x36, 0x00],
        "9": [0x46, 0x49, 0x49, 0x29, 0x16, 0x00],
        ":": [0x00, 0x00, 0x14, 0x00, 0x00, 0x00],
        ";": [0x00, 0x40, 0x34, 0x00, 0x00, 0x00],
        "<": [0x00, 0x08, 0x14, 0x22, 0x41, 0x00],
        "=": [0x14, 0x14, 0x14, 0x14, 0x14, 0x00],
        ">": [0x00, 0x41, 0x22, 0x14, 0x08, 0x00],
        "?": [0x02, 0x01, 0x59, 0x09, 0x06, 0x00],
        "@": [0x3E, 0x41, 0x5D, 0x59, 0x4E, 0x00],
        "A": [0x7C, 0x12, 0x11, 0x12, 0x7C, 0x00],
        "B": [0x7F, 0x49, 0x49, 0x49, 0x36, 0x00],
        "C": [0x3E, 0x41, 0x41, 0x41, 0x22, 0x00],
        "D": [0x7F, 0x41, 0x41, 0x41, 0x3E, 0x00],
        "E": [0x7F, 0x49, 0x49, 0x49, 0x41, 0x00],
        "F": [0x7F, 0x09, 0x09, 0x09, 0x01, 0x00],
        "G": [0x3E, 0x41, 0x41, 0x51, 0x73, 0x00],
        "H": [0x7F, 0x08, 0x08, 0x08, 0x7F, 0x00],
        "I": [0x00, 0x41, 0x7F, 0x41, 0x00, 0x00],
        "J": [0x20, 0x40, 0x41, 0x3F, 0x01, 0x00],
        "K": [0x7F, 0x08, 0x14, 0x22, 0x41, 0x00],
        "L": [0x7F, 0x40, 0x40, 0x40, 0x40, 0x00],
        "M": [0x7F, 0x02, 0x1C, 0x02, 0x7F, 0x00],
        "N": [0x7F, 0x04, 0x08, 0x10, 0x7F, 0x00],
        "O": [0x3E, 0x41, 0x41, 0x41, 0x3E, 0x00],
        "P": [0x7F, 0x09, 0x09, 0x09, 0x06, 0x00],
        "Q": [0x3E, 0x41, 0x51, 0x21, 0x5E, 0x00],
        "R": [0x7F, 0x09, 0x19, 0x29, 0x46, 0x00],
        "S": [0x26, 0x49, 0x49, 0x49, 0x32, 0x00],
        "T": [0x03, 0x01, 0x7F, 0x01, 0x03, 0x00],
        "U": [0x3F, 0x40, 0x40, 0x40, 0x3F, 0x00],
        "V": [0x1F, 0x20, 0x40, 0x20, 0x1F, 0x00],
        "W": [0x3F, 0x40, 0x38, 0x40, 0x3F, 0x00],
        "X": [0x63, 0x14, 0x08, 0x14, 0x63, 0x00],
        "Y": [0x03, 0x04, 0x78, 0x04, 0x03, 0x00],
        "Z": [0x61, 0x59, 0x49, 0x4D, 0x43, 0x00],
        "[": [0x00, 0x7F, 0x41, 0x41, 0x41, 0x00],
        "\\": [0x02, 0x04, 0x08, 0x10, 0x20, 0x00],
        "]": [0x00, 0x41, 0x41, 0x41, 0x7f, 0x00],
        "^": [0x04, 0x02, 0x01, 0x02, 0x04, 0x00],
        "_": [0x40, 0x40, 0x40, 0x40, 0x46, 0x00],
        "`": [0x00, 0x03, 0x07, 0x08, 0x00, 0x00],
        "a": [0x20, 0x54, 0x54, 0x78, 0x40, 0x00],
        "b": [0x7F, 0x28, 0x44, 0x44, 0x38, 0x00],
        "c": [0x38, 0x44, 0x44, 0x44, 0x28, 0x00],
        "d": [0x38, 0x44, 0x44, 0x28, 0x7F, 0x00],
        "e": [0x38, 0x54, 0x54, 0x54, 0x18, 0x00],
        "f": [0x00, 0x08, 0x7E, 0x09, 0x02, 0x00],
        "g": [0x38, 0xA4, 0xA4, 0x9C, 0x78, 0x00],
        "h": [0x7F, 0x08, 0x04, 0x04, 0x78, 0x00],
        "i": [0x00, 0x44, 0x7D, 0x40, 0x00, 0x00],
        "j": [0x20, 0x40, 0x40, 0x3D, 0x00, 0x00],
        "k": [0x7F, 0x10, 0x28, 0x44, 0x00, 0x00],
        "l": [0x00, 0x41, 0x7F, 0x40, 0x00, 0x00],
        "m": [0x7C, 0x04, 0x78, 0x04, 0x78, 0x00],
        "n": [0x7C, 0x08, 0x04, 0x04, 0x78, 0x00],
        "o": [0x38, 0x44, 0x44, 0x44, 0x38, 0x00],
        "p": [0xFC, 0x18, 0x24, 0x24, 0x18, 0x00],
        "q": [0x18, 0x24, 0x24, 0x18, 0xFC, 0x00],
        "r": [0x7C, 0x08, 0x04, 0x04, 0x08, 0x00],
        "s": [0x48, 0x54, 0x54, 0x54, 0x24, 0x00],
        "t": [0x04, 0x04, 0x3F, 0x44, 0x24, 0x00],
        "u": [0x3C, 0x40, 0x40, 0x20, 0x7C, 0x00],
        "v": [0x1C, 0x20, 0x40, 0x20, 0x1C, 0x00],
        "w": [0x3C, 0x40, 0x20, 0x40, 0x3C, 0x00],
        "x": [0x44, 0x28, 0x10, 0x28, 0x44, 0x00],
        "y": [0x4C, 0x90, 0x90, 0x90, 0x7C, 0x00],
        "z": [0x44, 0x64, 0x54, 0x4C, 0x44, 0x00],
        "{": [0x00, 0x08, 0x36, 0x41, 0x00, 0x00],
        "|": [0x00, 0x00, 0x77, 0x00, 0x00, 0x00],
        "}": [0x00, 0x41, 0x36, 0x08, 0x00, 0x00],
        "~": [0x02, 0x01, 0x02, 0x04, 0x02, 0x00]
    },
    "width": 6,
    "height": 8,
    "fmt": "LRMBLT"
}

fonts_8_16 = {
    "fonts": {  # top to bottom, msb left, lsb right
        " ": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        "!": [0x00, 0x00, 0x18, 0x3C, 0x3C, 0x3C, 0x18, 0x18, 0x18, 0x00, 0x18, 0x18, 0x00, 0x00, 0x00, 0x00],
        "\"": [0x00, 0x63, 0x63, 0x63, 0x22, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        "#": [0x00, 0x00, 0x00, 0x36, 0x36, 0x7F, 0x36, 0x36, 0x36, 0x7F, 0x36, 0x36, 0x00, 0x00, 0x00, 0x00],
        "$": [0x0C, 0x0C, 0x3E, 0x63, 0x61, 0x60, 0x3E, 0x03, 0x03, 0x43, 0x63, 0x3E, 0x0C, 0x0C, 0x00, 0x00],
        "%": [0x00, 0x00, 0x00, 0x00, 0x00, 0x61, 0x63, 0x06, 0x0C, 0x18, 0x33, 0x63, 0x00, 0x00, 0x00, 0x00],
        "&": [0x00, 0x00, 0x00, 0x1C, 0x36, 0x36, 0x1C, 0x3B, 0x6E, 0x66, 0x66, 0x3B, 0x00, 0x00, 0x00, 0x00],
        "'": [0x00, 0x30, 0x30, 0x30, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        "(": [0x00, 0x00, 0x0C, 0x18, 0x18, 0x30, 0x30, 0x30, 0x30, 0x18, 0x18, 0x0C, 0x00, 0x00, 0x00, 0x00],
        ")": [0x00, 0x00, 0x18, 0x0C, 0x0C, 0x06, 0x06, 0x06, 0x06, 0x0C, 0x0C, 0x18, 0x00, 0x00, 0x00, 0x00],
        "*": [0x00, 0x00, 0x00, 0x00, 0x42, 0x66, 0x3C, 0xFF, 0x3C, 0x66, 0x42, 0x00, 0x00, 0x00, 0x00, 0x00],
        "+": [0x00, 0x00, 0x00, 0x00, 0x18, 0x18, 0x18, 0xFF, 0x18, 0x18, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00],
        ",": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x18, 0x18, 0x30, 0x00, 0x00],
        "-": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        ".": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x18, 0x00, 0x00, 0x00, 0x00],
        "/": [0x00, 0x00, 0x01, 0x03, 0x07, 0x0E, 0x1C, 0x38, 0x70, 0xE0, 0xC0, 0x80, 0x00, 0x00, 0x00, 0x00],
        "0": [0x00, 0x00, 0x3E, 0x63, 0x63, 0x63, 0x6B, 0x6B, 0x63, 0x63, 0x63, 0x3E, 0x00, 0x00, 0x00, 0x00],
        "1": [0x00, 0x00, 0x0C, 0x1C, 0x3C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x3F, 0x00, 0x00, 0x00, 0x00],
        "2": [0x00, 0x00, 0x3E, 0x63, 0x03, 0x06, 0x0C, 0x18, 0x30, 0x61, 0x63, 0x7F, 0x00, 0x00, 0x00, 0x00],
        "3": [0x00, 0x00, 0x3E, 0x63, 0x03, 0x03, 0x1E, 0x03, 0x03, 0x03, 0x63, 0x3E, 0x00, 0x00, 0x00, 0x00],
        "4": [0x00, 0x00, 0x06, 0x0E, 0x1E, 0x36, 0x66, 0x66, 0x7F, 0x06, 0x06, 0x0F, 0x00, 0x00, 0x00, 0x00],
        "5": [0x00, 0x00, 0x7F, 0x60, 0x60, 0x60, 0x7E, 0x03, 0x03, 0x63, 0x73, 0x3E, 0x00, 0x00, 0x00, 0x00],
        "6": [0x00, 0x00, 0x1C, 0x30, 0x60, 0x60, 0x7E, 0x63, 0x63, 0x63, 0x63, 0x3E, 0x00, 0x00, 0x00, 0x00],
        "7": [0x00, 0x00, 0x7F, 0x63, 0x03, 0x06, 0x06, 0x0C, 0x0C, 0x18, 0x18, 0x18, 0x00, 0x00, 0x00, 0x00],
        "8": [0x00, 0x00, 0x3E, 0x63, 0x63, 0x63, 0x3E, 0x63, 0x63, 0x63, 0x63, 0x3E, 0x00, 0x00, 0x00, 0x00],
        "9": [0x00, 0x00, 0x3E, 0x63, 0x63, 0x63, 0x63, 0x3F, 0x03, 0x03, 0x06, 0x3C, 0x00, 0x00, 0x00, 0x00],
        ":": [0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x18, 0x00, 0x00, 0x00, 0x18, 0x18, 0x00, 0x00, 0x00, 0x00],
        ";": [0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x18, 0x00, 0x00, 0x00, 0x18, 0x18, 0x18, 0x30, 0x00, 0x00],
        "<": [0x00, 0x00, 0x00, 0x06, 0x0C, 0x18, 0x30, 0x60, 0x30, 0x18, 0x0C, 0x06, 0x00, 0x00, 0x00, 0x00],
        "=": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7E, 0x00, 0x00, 0x7E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        ">": [0x00, 0x00, 0x00, 0x60, 0x30, 0x18, 0x0C, 0x06, 0x0C, 0x18, 0x30, 0x60, 0x00, 0x00, 0x00, 0x00],
        "?": [0x00, 0x00, 0x3E, 0x63, 0x63, 0x06, 0x0C, 0x0C, 0x0C, 0x00, 0x0C, 0x0C, 0x00, 0x00, 0x00, 0x00],
        "@": [0x00, 0x00, 0x3E, 0x63, 0x63, 0x6F, 0x6B, 0x6B, 0x6E, 0x60, 0x60, 0x3E, 0x00, 0x00, 0x00, 0x00],
        "A": [0x00, 0x00, 0x08, 0x1C, 0x36, 0x63, 0x63, 0x63, 0x7F, 0x63, 0x63, 0x63, 0x00, 0x00, 0x00, 0x00],
        "B": [0x00, 0x00, 0x7E, 0x33, 0x33, 0x33, 0x3E, 0x33, 0x33, 0x33, 0x33, 0x7E, 0x00, 0x00, 0x00, 0x00],
        "C": [0x00, 0x00, 0x1E, 0x33, 0x61, 0x60, 0x60, 0x60, 0x60, 0x61, 0x33, 0x1E, 0x00, 0x00, 0x00, 0x00],
        "D": [0x00, 0x00, 0x7C, 0x36, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x36, 0x7C, 0x00, 0x00, 0x00, 0x00],
        "E": [0x00, 0x00, 0x7F, 0x33, 0x31, 0x34, 0x3C, 0x34, 0x30, 0x31, 0x33, 0x7F, 0x00, 0x00, 0x00, 0x00],
        "F": [0x00, 0x00, 0x7F, 0x33, 0x31, 0x34, 0x3C, 0x34, 0x30, 0x30, 0x30, 0x78, 0x00, 0x00, 0x00, 0x00],
        "G": [0x00, 0x00, 0x1E, 0x33, 0x61, 0x60, 0x60, 0x6F, 0x63, 0x63, 0x37, 0x1D, 0x00, 0x00, 0x00, 0x00],
        "H": [0x00, 0x00, 0x63, 0x63, 0x63, 0x63, 0x7F, 0x63, 0x63, 0x63, 0x63, 0x63, 0x00, 0x00, 0x00, 0x00],
        "I": [0x00, 0x00, 0x3C, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x3C, 0x00, 0x00, 0x00, 0x00],
        "J": [0x00, 0x00, 0x0F, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x66, 0x66, 0x3C, 0x00, 0x00, 0x00, 0x00],
        "K": [0x00, 0x00, 0x73, 0x33, 0x36, 0x36, 0x3C, 0x36, 0x36, 0x33, 0x33, 0x73, 0x00, 0x00, 0x00, 0x00],
        "L": [0x00, 0x00, 0x78, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x31, 0x33, 0x7F, 0x00, 0x00, 0x00, 0x00],
        "M": [0x00, 0x00, 0x63, 0x77, 0x7F, 0x6B, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x00, 0x00, 0x00, 0x00],
        "N": [0x00, 0x00, 0x63, 0x63, 0x73, 0x7B, 0x7F, 0x6F, 0x67, 0x63, 0x63, 0x63, 0x00, 0x00, 0x00, 0x00],
        "O": [0x00, 0x00, 0x1C, 0x36, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x36, 0x1C, 0x00, 0x00, 0x00, 0x00],
        "P": [0x00, 0x00, 0x7E, 0x33, 0x33, 0x33, 0x3E, 0x30, 0x30, 0x30, 0x30, 0x78, 0x00, 0x00, 0x00, 0x00],
        "Q": [0x00, 0x00, 0x3E, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x6B, 0x6F, 0x3E, 0x06, 0x07, 0x00, 0x00],
        "R": [0x00, 0x00, 0x7E, 0x33, 0x33, 0x33, 0x3E, 0x36, 0x36, 0x33, 0x33, 0x73, 0x00, 0x00, 0x00, 0x00],
        "S": [0x00, 0x00, 0x3E, 0x63, 0x63, 0x30, 0x1C, 0x06, 0x03, 0x63, 0x63, 0x3E, 0x00, 0x00, 0x00, 0x00],
        "T": [0x00, 0x00, 0xFF, 0xDB, 0x99, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x3C, 0x00, 0x00, 0x00, 0x00],
        "U": [0x00, 0x00, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x3E, 0x00, 0x00, 0x00, 0x00],
        "V": [0x00, 0x00, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x36, 0x1C, 0x08, 0x00, 0x00, 0x00, 0x00],
        "W": [0x00, 0x00, 0x63, 0x63, 0x63, 0x63, 0x63, 0x6B, 0x6B, 0x7F, 0x36, 0x36, 0x00, 0x00, 0x00, 0x00],
        "X": [0x00, 0x00, 0xC3, 0xC3, 0x66, 0x3C, 0x18, 0x18, 0x3C, 0x66, 0xC3, 0xC3, 0x00, 0x00, 0x00, 0x00],
        "Y": [0x00, 0x00, 0xC3, 0xC3, 0xC3, 0x66, 0x3C, 0x18, 0x18, 0x18, 0x18, 0x3C, 0x00, 0x00, 0x00, 0x00],
        "Z": [0x00, 0x00, 0x7F, 0x63, 0x43, 0x06, 0x0C, 0x18, 0x30, 0x61, 0x63, 0x7F, 0x00, 0x00, 0x00, 0x00],
        "[": [0x00, 0x00, 0x3C, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x3C, 0x00, 0x00, 0x00, 0x00],
        "\\": [0x00, 0x00, 0x80, 0xC0, 0xE0, 0x70, 0x38, 0x1C, 0x0E, 0x07, 0x03, 0x01, 0x00, 0x00, 0x00, 0x00],
        "]": [0x00, 0x00, 0x3C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x3C, 0x00, 0x00, 0x00, 0x00],
        "^": [0x08, 0x1C, 0x36, 0x63, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        "_": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00],
        "`": [0x18, 0x18, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        "a": [0x00, 0x00, 0x00, 0x00, 0x00, 0x3C, 0x46, 0x06, 0x3E, 0x66, 0x66, 0x3B, 0x00, 0x00, 0x00, 0x00],
        "b": [0x00, 0x00, 0x70, 0x30, 0x30, 0x3C, 0x36, 0x33, 0x33, 0x33, 0x33, 0x6E, 0x00, 0x00, 0x00, 0x00],
        "c": [0x00, 0x00, 0x00, 0x00, 0x00, 0x3E, 0x63, 0x60, 0x60, 0x60, 0x63, 0x3E, 0x00, 0x00, 0x00, 0x00],
        "d": [0x00, 0x00, 0x0E, 0x06, 0x06, 0x1E, 0x36, 0x66, 0x66, 0x66, 0x66, 0x3B, 0x00, 0x00, 0x00, 0x00],
        "e": [0x00, 0x00, 0x00, 0x00, 0x00, 0x3E, 0x63, 0x63, 0x7E, 0x60, 0x63, 0x3E, 0x00, 0x00, 0x00, 0x00],
        "f": [0x00, 0x00, 0x1C, 0x36, 0x32, 0x30, 0x7C, 0x30, 0x30, 0x30, 0x30, 0x78, 0x00, 0x00, 0x00, 0x00],
        "g": [0x00, 0x00, 0x00, 0x00, 0x00, 0x3B, 0x66, 0x66, 0x66, 0x66, 0x3E, 0x06, 0x66, 0x3C, 0x00, 0x00],
        "h": [0x00, 0x00, 0x70, 0x30, 0x30, 0x36, 0x3B, 0x33, 0x33, 0x33, 0x33, 0x73, 0x00, 0x00, 0x00, 0x00],
        "i": [0x00, 0x00, 0x0C, 0x0C, 0x00, 0x1C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x1E, 0x00, 0x00, 0x00, 0x00],
        "j": [0x00, 0x00, 0x06, 0x06, 0x00, 0x0E, 0x06, 0x06, 0x06, 0x06, 0x06, 0x66, 0x66, 0x3C, 0x00, 0x00],
        "k": [0x00, 0x00, 0x70, 0x30, 0x30, 0x33, 0x33, 0x36, 0x3C, 0x36, 0x33, 0x73, 0x00, 0x00, 0x00, 0x00],
        "l": [0x00, 0x00, 0x1C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x1E, 0x00, 0x00, 0x00, 0x00],
        "m": [0x00, 0x00, 0x00, 0x00, 0x00, 0x6E, 0x7F, 0x6B, 0x6B, 0x6B, 0x6B, 0x6B, 0x00, 0x00, 0x00, 0x00],
        "n": [0x00, 0x00, 0x00, 0x00, 0x00, 0x6E, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x00, 0x00, 0x00, 0x00],
        "o": [0x00, 0x00, 0x00, 0x00, 0x00, 0x3E, 0x63, 0x63, 0x63, 0x63, 0x63, 0x3E, 0x00, 0x00, 0x00, 0x00],
        "p": [0x00, 0x00, 0x00, 0x00, 0x00, 0x6E, 0x33, 0x33, 0x33, 0x33, 0x3E, 0x30, 0x30, 0x78, 0x00, 0x00],
        "q": [0x00, 0x00, 0x00, 0x00, 0x00, 0x3B, 0x66, 0x66, 0x66, 0x66, 0x3E, 0x06, 0x06, 0x0F, 0x00, 0x00],
        "r": [0x00, 0x00, 0x00, 0x00, 0x00, 0x6E, 0x3B, 0x33, 0x30, 0x30, 0x30, 0x78, 0x00, 0x00, 0x00, 0x00],
        "s": [0x00, 0x00, 0x00, 0x00, 0x00, 0x3E, 0x63, 0x38, 0x0E, 0x03, 0x63, 0x3E, 0x00, 0x00, 0x00, 0x00],
        "t": [0x00, 0x00, 0x08, 0x18, 0x18, 0x7E, 0x18, 0x18, 0x18, 0x18, 0x1B, 0x0E, 0x00, 0x00, 0x00, 0x00],
        "u": [0x00, 0x00, 0x00, 0x00, 0x00, 0x66, 0x66, 0x66, 0x66, 0x66, 0x66, 0x3B, 0x00, 0x00, 0x00, 0x00],
        "v": [0x00, 0x00, 0x00, 0x00, 0x00, 0x63, 0x63, 0x36, 0x36, 0x1C, 0x1C, 0x08, 0x00, 0x00, 0x00, 0x00],
        "w": [0x00, 0x00, 0x00, 0x00, 0x00, 0x63, 0x63, 0x63, 0x6B, 0x6B, 0x7F, 0x36, 0x00, 0x00, 0x00, 0x00],
        "x": [0x00, 0x00, 0x00, 0x00, 0x00, 0x63, 0x36, 0x1C, 0x1C, 0x1C, 0x36, 0x63, 0x00, 0x00, 0x00, 0x00],
        "y": [0x00, 0x00, 0x00, 0x00, 0x00, 0x63, 0x63, 0x63, 0x63, 0x63, 0x3F, 0x03, 0x06, 0x3C, 0x00, 0x00],
        "z": [0x00, 0x00, 0x00, 0x00, 0x00, 0x7F, 0x66, 0x0C, 0x18, 0x30, 0x63, 0x7F, 0x00, 0x00, 0x00, 0x00],
        "{": [0x00, 0x00, 0x0E, 0x18, 0x18, 0x18, 0x70, 0x18, 0x18, 0x18, 0x18, 0x0E, 0x00, 0x00, 0x00, 0x00],
        "|": [0x00, 0x00, 0x18, 0x18, 0x18, 0x18, 0x18, 0x00, 0x18, 0x18, 0x18, 0x18, 0x18, 0x00, 0x00, 0x00],
        "}": [0x00, 0x00, 0x70, 0x18, 0x18, 0x18, 0x0E, 0x18, 0x18, 0x18, 0x18, 0x70, 0x00, 0x00, 0x00, 0x00],
        "~": [0x00, 0x00, 0x3B, 0x6E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    },
    "width": 8,
    "height": 16,
    "fmt": "TBMLLR"
}


class SPI:
    MODE_1 = 1
    MODE_2 = 2
    MODE_3 = 3
    MODE_4 = 4

    def __init__(self, bus, dev, speed = 3900000, mode = MODE_4):
        self._bus = spidev.SpiDev()
        self._bus.open(0, 0)
        self._bus.no_cs = True
        self._bus.max_speed_hz = speed
        self._bus.threewire = True

    def transfer(self, buf):
        if len(buf):
            return self._bus.writebytes(buf)
        return []

    def read_data(self, cmd):
        return self._bus.readbytes(cmd)
        # return  0


class GPIO:
    HIGH = RPIGPIO.HIGH
    LOW = RPIGPIO.LOW

    OUT = RPIGPIO.OUT
    IN = RPIGPIO.IN

    RISING = RPIGPIO.RISING
    FALLING = RPIGPIO.FALLING
    BOTH = RPIGPIO.BOTH

    def __init__(self, pin, mode, default_out=HIGH):
        self._pin = pin
        self._f_int = None
        self._int_done = True
        self._int_mode = None
        if mode == self.OUT:
            RPIGPIO.setup(pin, mode)
            if default_out == self.HIGH:
                RPIGPIO.output(pin, default_out)
            else:
                RPIGPIO.output(pin, self.LOW)
        else:
            RPIGPIO.setup(pin, self.IN, pull_up_down=RPIGPIO.PUD_UP)

    def set_out(self, level):
        if level:
            RPIGPIO.output(self._pin, self.HIGH)
        else:
            RPIGPIO.output(self._pin, self.LOW)

    def _int_cb(self, status):
        if self._int_done:
            self._int_done = False
            time.sleep(0.02)
            if self._int_mode == self.BOTH:
                self._f_int()
            elif self._int_mode == self.RISING and self.read() == self.HIGH:
                self._f_int()
            elif self._int_mode == self.FALLING and self.read() == self.LOW:
                self._f_int()
            self._int_done = True

    def set_interrupt(self, mode, cb):
        if mode != self.RISING and mode != self.FALLING and mode != self.BOTH:
            return
        self._int_mode = mode
        RPIGPIO.add_event_detect(self._pin, mode, self._int_cb)
        self._f_int = cb

    def read(self):
        return RPIGPIO.input(self._pin)

    def cleanup(self):
        RPIGPIO.cleanup()


class Fonts:

    def __init__(self):
        self._fonts_enabled = False
        self._fonts = {}
        self._fonts_width = 0
        self._fonts_height = 0
        self._fonts_fmt = ""

        self._extension_fonts_enabled = False
        self._extension_fonts_width = 0
        self._extension_fonts_height = 0

        self._default_fonts_enabled = True

    def set_fonts(self, fonts):
        """!
          @brief Set ASCII font format 
          @param fonts font type
        """
        self._fonts_enabled = True
        self._fonts = fonts["fonts"]
        self._fonts_width = fonts["width"]
        self._fonts_height = fonts["height"]
        self._fonts_fmt = fonts["fmt"]

        self._extension_fonts_width = fonts["width"] * 2
        self._extension_fonts_height = fonts["height"] * 2

    def set_ex_fonts(self, obj):
        """!
          @brief init with fonts file
          @param obj Font file 
        """
        self._extension_fonts_enabled = True
        self._extension_fonts = obj
        self._default_fonts_enabled = False

    def set_enable_default_fonts(self, opt):
        """!
          @brief Enable or disable mode fonts
          @param opt True/False
        """
        if opt:
            self._default_fonts_enabled = True
        else:
            self._default_fonts_enabled = False

    def set_ex_fonts_fmt(self, width, height):
        """!
          @brief Set the format of the extended font
          @param width Font width
          @param height Font height
        """
        if self._extension_fonts_enabled:
            self._extension_fonts.set_fmt(width, height)
            self._extension_fonts_width = width
            self._extension_fonts_height = height

    def get_one_character(self, char_ascii):
        """!
          @brief Get the font data of a character
          @param char_ascii ASCII code of the character
          @return rslt List of character
          @return w Character width
          @return h  Character height
          @return fmt Font format
        """
        w = 0
        h = 0
        fmt = "UNKNOW"
        rslt = []
        done = False
        if self._fonts_enabled and self._default_fonts_enabled:
            try:
                rslt = self._fonts[char_ascii]
                w = self._fonts_width
                h = self._fonts_height
                fmt = self._fonts_fmt
                done = True
            except:
                pass
        if self._extension_fonts_enabled and done == False:
            try:
                (rslt, w, h, fmt) = self._extension_fonts.get_one(char_ascii)
                done = True
            except:
                print("try get unicode fonts failed: %s" % char_ascii)
        return rslt, w, h, fmt


class FreetypeHelper:

    def __init__(self, file_path):
        self._face = freetype.Face(file_path)
        self._width = 0
        self._height = 0
        self._fade = 96

    def set_fmt(self, width, height):
        """!
          @brief Set the font width and height
          @param width Font width
          @param height Font height
        """
        self._width = int(width)
        self._height = int(height)
        self._face.set_pixel_sizes(width, height)

    def set_dis_lower_limit(self, limit):
        """!
          @brief Set the color depth limit of the font
          @param limit Depth
        """
        self._fade = limit

    def get_one(self, ch):
        """!
          @brief Get the font data of a character
          @param ch ASCII code of the character
          @return rslt List of character
          @return w Character width
          @return h Character height
          @return fmt Font format
        """
        self._face.load_char(ch)
        bitmap = self._face.glyph.bitmap
        origin_y = self._face.glyph.bitmap_top
        width = bitmap.width
        height = bitmap.rows
        buffer = bitmap.buffer
        rslt = []

        if height > self._height:
            buffer = buffer[0: width * self._height]
            height = self._height
        if width > self._width:
            for i in range(height):
                rslt += buffer[i * width: i * width + self._width]
            width = self._width
            buffer = rslt
            rslt = []
        if (ord(" ") <= ord(ch) <= ord("~")) or width <= (self._width // 2):
            rslt = [0] * (((self._width - 1) // 16 + 1) * self._height + 1)
            left = (self._width // 2 - width) // 2
            line_data_len = (self._width - 1) // 16 + 1
        else:
            rslt = [0] * (((self._width - 1) // 8 + 1) * self._height + 1)
            left = (self._width - width) // 2
            line_data_len = (self._width - 1) // 8 + 1
        if left < 0:
            left = 0
        top = ((self._height * 8 + 5) // 10 - origin_y) * line_data_len
        if top < 0:
            top = 0
        for i in range(height):
            for j in range(width):
                if buffer[i * width + j] > self._fade:
                    try:
                        rslt[i * line_data_len + (j + left) // 8 + top] |= 0x80 >> ((j + left) % 8)
                    except:
                        print(
                            "freetype_helper get one err: width: %d, height: %d, top: %d, left: %d, rslt_len: %d, origin_y: %d" % (
                                width, height, top, left, len(rslt), origin_y))
                        raise "err"
                    # rslt[i * line_data_len + (j + left) // 8 + top] |= 0x80 >> ((j + left) % 8)
        if (ord(" ") <= ord(ch) <= ord("~")) or width < (self._width // 2):
            return rslt, self._width // 2, self._height, "TBMLLR"
        else:
            return rslt, self._width, self._height, "TBMLLR"


class DFRobot_Display():

    WHITE24 = 0xffffff
    SILVER24 = 0xc0c0c0
    GRAY24 = 0x808080
    BLACK24 = 0x000000
    RED24 = 0xff0000
    MAROON24 = 0x800000
    YELLOW24 = 0xffff00
    OLIVE24 = 0x808000
    GREEN24 = 0x00ff00
    DARKGREEN24 = 0x008000
    CYAN24 = 0x00ffff
    BLUE24 = 0x0000ff
    NAVY24 = 0x000080
    FUCHSIA24 = 0xff00ff
    PURPLE24 = 0x800080
    TEAL24 = 0x008080

    WHITE16 = 0xffff
    SILVER16 = 0xc618
    GRAY16 = 0x8400
    BLACK16 = 0x0000
    RED16 = 0xf800
    MAROON16 = 0x8000
    YELLOW16 = 0xffe0
    OLIVE16 = 0x8400
    GREEN16 = 0x07e0
    DARKGREEN16 = 0x0400
    CYAN16 = 0x07ff
    BLUE16 = 0x001f
    NAVY16 = 0x0010
    FUCHSIA16 = 0xf81f
    PURPLE16 = 0x8010
    TEAL16 = 0x0410

    WHITE = WHITE16
    SILVER = SILVER16
    GRAY = GRAY16
    BLACK = BLACK16
    RED = RED16
    MAROON = MAROON16
    YELLOW = YELLOW16
    OLIVE = OLIVE16
    GREEN = GREEN16
    DARKGREEN = DARKGREEN16
    CYAN = CYAN16
    BLUE = BLUE16
    NAVY = NAVY16
    FUCHSIA = FUCHSIA16
    PURPLE = PURPLE16
    TEAL = TEAL16

    POSITIVE = 1
    REVERSE = -1

    BITMAP_TBMLLR = "TBMLLR"
    BITMAP_TBMRLL = "TBMRLL"
    BITMAP_BTMLLR = "BTMLLR"
    BITMAP_BTMRLL = "BTMRLL"
    BITMAP_LRMTLB = "LRMTLB"
    BITMAP_LRMBLT = "LRMBLT"
    BITMAP_RLMTLB = "RLMTLB"
    BIMTAP_RLMBLT = "RLMBLT"
    BITMAP_UNKNOW = "UNKNOW"

    def __init__(self, w, h):
        print("DFRobot_Display init " + str(w) + " " + str(h))
        self._width = w
        self._height = h

        self._line_width = 1
        self._bitmap_size = 1
        self._bitmap_fmt = ""
        self._bmp_fmt = self.BITMAP_TBMLLR

        self._fonts = Fonts()
        self._text_size = 1
        self._text_color = self.BLACK
        self._text_background = self.WHITE
        self._text_cursor_x = 0
        self._text_cursor_y = 0
        self._text_interval_row = 0
        self._text_interval_col = 0

    def set_line_width(self, w):
        """!
          @brief Set the width of a line segment
        """
        if w < 0:
            return
        self._line_width = w

    def set_text_format(self, size, color, background, interval_row=2, interval_col=0):
        """!
          @brief Set the format of text
          @param size Font size
          @param color Font color
          @param background Background color of the font
          @param interval_row Spacing between rows of text
          @param interval_col Spacing between columns of text
        """
        self._text_color = color
        self._text_interval_row = interval_row
        self._text_interval_col = interval_col
        self._text_background = background
        if size < 0:
            return
        self._text_size = size

    def set_text_cursor(self, x, y):
        """!
          @brief Set the cursor position
          @param x x-coordinate
          @param y y-coordinate
        """
        self._text_cursor_x = int(x)
        self._text_cursor_y = int(y)

    def set_bitmap_size(self, size):
        """!
          @brief Set the bitmap size
          @param size Bitmap size
        """
        if size < 0:
            return
        self._bitmap_size = size

    def set_bitmap_fmt(self, fmt):
        """!
          @brief Set bitmap display format
          @param fmt Format configuration
        """
        self._bmp_fmt = fmt

    def set_ex_fonts(self, obj):
        """!
          @brief Set font
          @param obj font
        """
        self._fonts.set_ex_fonts(obj)

    def set_ex_fonts_fmt(self, width, height):
        """!
          @brief Set the width and height of the font
          @param width Font width
          @param height Font height
        """
        self._fonts.set_ex_fonts_fmt(width, height)

    def set_enable_default_fonts(self, opt):
        """!
          @brief Set the default font
          @param opt Font type
        """
        self._fonts.set_enable_default_fonts(opt)

    def pixel(self, x, y, color):
        """!
          @brief Draw a point on the screen at (x,y) coordinate
          @param x  x-axis coordinate
          @param y  y-axis coordinate 
          @param color Color
        """
        pass

    def write_one_char(self, ch):
        """!
          @brief Display a character on the screen
          @param ch ASCII code of the character
        """
        pass

    def print_str(self, s):
        """!
          @brief Display a string on the screen
          @param s String
        """
        try:
            s = str(s)
        except:
            return
        if sys.version_info.major == 2:
            s = s.decode("utf-8")
        for i in s:
            self.write_one_char(i)

    def print_str_ln(self, s):
        """!
          @brief Display a string on the screen and move to the next line
          @param s String 
        """
        self.print_str(s)
        self.write_one_char("\n")

    def clear(self, color):
        """!
          @brief Clear screen 
          @param color  Color
        """
        self.filled_rect(0, 0, self._width, self._height, color)
        self._text_cursor_x = 0
        self._text_cursor_y = 0

    def vertical_line(self, x, y, h, color):
        """!
          @brief Draw a vertical line
          @param x x-axis coordinate
          @param y y-axis coordinate
          @param h Line length
          @param color  Color
        """
        x = int(x)
        y = int(y)
        h = int(h)
        direction = self._get_direction(h)
        x -= self._line_width // 2
        h = self._ternary_expression(h > 0, h, -h)
        for i in range(self._ternary_expression(h > 0, h, - h)):
            xx = x
            for j in range(self._line_width):
                self.pixel(xx, y, color)
                xx += 1
            y += direction

    def horizontal_line(self, x, y, w, color):
        """!
          @brief Draw a horizontal line
          @param x x-axis coordinate
          @param y y-axis coordinate
          @param w line length
          @param color Color
        """
        x = int(x)
        y = int(y)
        w = int(w)
        direction = self._get_direction(w)
        y -= self._line_width // 2
        for i in range(self._ternary_expression(w > 0, w, - w)):
            yy = y
            for j in range(self._line_width):
                self.pixel(x, yy, color)
                yy += 1
            x += direction

    def line(self, x, y, x1, y1, color):
        """!
          @brief Draw a straight line
          @param x starting x-axis coordinate of the line
          @param y starting y-axis coordinate of the line
          @param x1 ending x-axis coordinate of the line
          @param y1 ending y-axis coordinate of the line
          @param color Color
        """
        x = int(x)
        y = int(y)
        x1 = int(x1)
        y1 = int(y1)
        if x == x1:
            self.vertical_line(x, y, y1 - y, color)
            return
        if y == y1:
            self.horizontal_line(x, y, x1 - x, color)
            return
        dx = abs(x1 - x)
        dy = abs(y1 - y)
        dir_x = self._ternary_expression(x < x1, 1, -1)
        dir_y = self._ternary_expression(y < y1, 1, -1)
        if dx > dy:
            err = dx / 2
            for i in range(dx):
                self.horizontal_line(x, y, 1, color)
                x += dir_x
                err -= dy
                if err < 0:
                    err += dx
                    y += dir_y
            self.horizontal_line(x1, y1, 1, color)
        else:
            err = dy / 2
            for i in range(dy):
                self.vertical_line(x, y, 1, color)
                y += dir_y
                err -= dx
                if err < 0:
                    err += dy
                    x += dir_x
            self.vertical_line(x1, y1, 1, color)

    def hollow_triangle(self, x, y, x1, y1, x2, y2, color):
        """!
          @brief Draw a hollow triangle
          @param x x-coordinate of the first point of the triangle
          @param y y-coordinate of the first point of the triangle
          @param x1 x-coordinate of the second point of the triangle
          @param y1 y-coordinate of the second point of the triangle
          @param x2 x-coordinate of the third point of the triangle
          @param y2 y-coordinate of the third point of the triangle
          @param color Color
        """
        self.line(x, y, x1, y1, color)
        self.line(x1, y1, x2, y2, color)
        self.line(x2, y2, x, y, color)

    def filled_triangle(self, x, y, x1, y1, x2, y2, color):
        """!
          @brief Draw a filled triangle
          @param x x-coordinate of the first point of the triangle
          @param y y-coordinate of the first point of the triangle
          @param x1 x-coordinate of the second point of the triangle
          @param y1 y-coordinate of the second point of the triangle
          @param x2 x-coordinate of the third point of the triangle
          @param y2 y-coordinate of the third point of the triangle
          @param color Color
        """
        self.line(x, y, x1, y1, color)
        self.line(x1, y1, x2, y2, color)
        self.line(x2, y2, x, y, color)
        x = int(x)
        y = int(y)
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        temp = self._line_width
        self._line_width = 1
        if x == x1 and x == x2:
            ymax = max([y, y1, y2])
            ymin = min([y, y1, y2])
            self.horizontal_line(x, ymin, ymax - ymin, color)
            self._line_width = temp
            return
        if y == y1 and y == y2:
            xmax = max([x, x1, x2])
            xmin = max([x, x1, x2])
            self.vertical_line(xmin, y, xmax - xmin, color)
            self._line_width = temp
            return

        direction = self.POSITIVE
        if y == y1 or y1 == y2 or y == y2:
            if y == y1:
                (x, x2) = (x2, x)
                (y, y2) = (y2, y)
            elif y == y2:
                (x, x1) = (x1, x)
                (y, y1) = (y1, y)
            if y > y1:
                direction = self.REVERSE
            if x1 > x2:
                (x1, x2) = (x2, x1)
                (y1, y2) = (y2, y1)
        else:
            if y > y1:
                (x, x1) = (x1, x)
                (y, y1) = (y1, y)
            if y > y2:
                (x, x2) = (x2, x)
                (y, y2) = (y2, y)
            if y1 > y2:
                (x1, x2) = (x2, x1)
                (y1, y2) = (y2, y1)

        dx1 = x1 - x
        dx2 = x2 - x
        dx3 = x2 - x1
        dy1 = y1 - y
        dy2 = y2 - y
        dy3 = y2 - y1
        if direction == self.POSITIVE:
            for i in range(dy1):
                self.horizontal_line(x + dx1 * i / dy1, y + i, (x + dx2 * i / dy2) - (x + dx1 * i / dy1) + 1, color)
            for i in range(dy3):
                self.horizontal_line(x1 + dx3 * i / dy3, y1 + i, (x + dx2 * (i + dy1) / dy2) - (x1 + dx3 * i / dy3) + 1,
                                     color)
        else:
            y = y1 + dy1
            dy1 = - dy1
            for i in range(dy1):
                self.horizontal_line(x + dx1 * i / dy1, y1 + dy1 - i, (x + dx2 * i / dy1) - (x + dx1 * i / dy1) + 1,
                                     color)
        self._line_width = temp

    def hollow_rect(self, x, y, w, h, color):
        """!
          @brief Draw a hollow rectangle
          @param x x-coordinate of the starting point of the rectangle
          @param y y-coordinate of the starting point of the rectangle
          @param w Rectangle width 
          @param h Rectangle height
          @param color Color
        """
        if w < 0:
            x += w
            w = -w
        if h < 0:
            y += h
            h = -h
        self.horizontal_line(x - self._line_width // 2, y, w + self._line_width, color)
        self.horizontal_line(x - self._line_width // 2, y + h, w + self._line_width, color)
        self.vertical_line(x, y - self._line_width // 2, h + self._line_width, color)
        self.vertical_line(x + w, y - self._line_width // 2, h + self._line_width, color)

    def filled_rect(self, x, y, w, h, color):
        """!
          @brief Draw a solid rectangle
          @param x x-coordinate of the starting point of the rectangle
          @param y y-coordinate of the starting point of the rectangle
          @param w Rectangle width 
          @param h Rectangle height
          @param color Color
        """
        temp = self._line_width
        self._line_width = 1
        if w < 0:
            x += w
            w = abs(w)
        for i in range(w):
            self.vertical_line(x + i, y, h, color)
        self._line_width = temp

    QUADRANT_1 = 1
    QUADRANT_2 = 2
    QUADRANT_3 = 4
    QUADRANT_4 = 8
    QUADRANT_ALL = 15

    def hollow_circle_helper(self, x, y, r, quadrant, color):
        """!
          @brief Helper function for drawing a hollow circle
          @param x X-coordinate of the center of the circle
          @param y Y-coordinate of the center of the circle
          @param r Radius of the circle
          @param quadrant Used to indicate which quadrant of the circle to draw
          @param color Color
        """
        x = int(x)
        y = int(y)
        r = abs(int(r))
        vx = 0
        vy = r
        dx = 1
        dy = -2 * r
        p = 1 - r
        if quadrant & self.QUADRANT_1:
            self.vertical_line(x + r, y, 1, color)
        if quadrant & self.QUADRANT_2:
            self.vertical_line(x, y - r, 1, color)
        if quadrant & self.QUADRANT_3:
            self.vertical_line(x - r, y, 1, color)
        if quadrant & self.QUADRANT_4:
            self.vertical_line(x, y + r, 1, color)

        half_line_width = self._line_width // 2
        while vx < vy:
            if p >= 0:
                vy -= 1
                dy += 2
                p += dy
            vx += 1
            dx += 2
            p += dx
            if quadrant & self.QUADRANT_1:
                self.filled_rect(x + vx - half_line_width, y - vy - half_line_width, self._line_width, self._line_width,
                                 color)  # quadrant 1
                self.filled_rect(x + vy - half_line_width, y - vx - half_line_width, self._line_width, self._line_width,
                                 color)  # quadrant 1
            if quadrant & self.QUADRANT_2:
                self.filled_rect(x - vx - half_line_width, y - vy - half_line_width, self._line_width, self._line_width,
                                 color)  # quadrant 2
                self.filled_rect(x - vy - half_line_width, y - vx - half_line_width, self._line_width, self._line_width,
                                 color)  # quadrant 2
            if quadrant & self.QUADRANT_3:
                self.filled_rect(x - vx - half_line_width, y + vy - half_line_width, self._line_width, self._line_width,
                                 color)  # quadrant 3
                self.filled_rect(x - vy - half_line_width, y + vx - half_line_width, self._line_width, self._line_width,
                                 color)  # quadrant 3
            if quadrant & self.QUADRANT_4:
                self.filled_rect(x + vx - half_line_width, y + vy - half_line_width, self._line_width, self._line_width,
                                 color)  # quadrant 4
                self.filled_rect(x + vy - half_line_width, y + vx - half_line_width, self._line_width, self._line_width,
                                 color)  # quadrant 4

    def hollow_circle(self, x, y, r, color):
        """!
          @brief Draw a hollow circle
          @param x X-coordinate of the center of the circle
          @param y Y-coordinate of the center of the circle
          @param r Radius of the circle
          @param color Color
        """
        self.hollow_circle_helper(x, y, r, self.QUADRANT_ALL, color)

    def filled_circle_helper(self, x, y, r, quadrant, color):
        """!
          @brief Helper function for drawing a solid circle
          @param x X-coordinate of the center of the circle
          @param y Y-coordinate of the center of the circle
          @param r Radius of the circle
          @param quadrant Used to indicate which quadrant of the circle to draw
          @param color Color
        """
        x = int(x)
        y = int(y)
        r = abs(int(r))
        temp = self._line_width
        self._line_width = 1
        vx = 0
        vy = r
        dx = 1
        dy = -2 * r
        p = 1 - r
        if quadrant & self.QUADRANT_1:
            self.horizontal_line(x, y, r + 1, color)
        if quadrant & self.QUADRANT_2:
            self.vertical_line(x, y, - r - 1, color)
        if quadrant & self.QUADRANT_3:
            self.horizontal_line(x, y, - r - 1, color)
        if quadrant & self.QUADRANT_4:
            self.vertical_line(x, y, r + 1, color)

        while vx < vy:
            if p >= 0:
                vy -= 1
                dy += 2
                p += dy
            vx += 1
            dx += 2
            p += dx
            if quadrant & self.QUADRANT_1:
                self.vertical_line(x + vx, y - vy, vy, color)  # quadrant 1
                self.vertical_line(x + vy, y - vx, vx, color)  # quadrant 1
            if quadrant & self.QUADRANT_2:
                self.vertical_line(x - vx, y - vy, vy, color)  # quadrant 2
                self.vertical_line(x - vy, y - vx, vx, color)  # quadrant 2
            if quadrant & self.QUADRANT_3:
                self.vertical_line(x - vx, y + vy, - vy, color)  # quadrant 3
                self.vertical_line(x - vy, y + vx, - vx, color)  # quadrant 3
            if quadrant & self.QUADRANT_4:
                self.vertical_line(x + vx, y + vy, - vy, color)  # quadrant 4
                self.vertical_line(x + vy, y + vx, - vx, color)  # quadrant 4
        self._line_width = temp

    def filled_circle(self, x, y, r, color):
        """!
          @brief Draw a solid circle
          @param x X-coordinate of the center of the circle
          @param y Y-coordinate of the center of the circle
          @param r Radius of the circle
          @param color Color
        """
        self.filled_circle_helper(x, y, r, self.QUADRANT_ALL, color)

    def hollow_rounded_rectangle(self, x, y, w, h, r, color):
        """!
          @brief Draw a hollow rounded rectangle
          @param x x-coordinate of the starting point of the rectangle
          @param y y-coordinate of the starting point of the rectangle
          @param w Rectangle width 
          @param h Rectangle height
          @param r Radius of the circle
          @param color Color
        """
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)
        r = abs(int(r))
        if w < 0:
            x += w
            w = abs(w)
        if h < 0:
            y += h
            h = abs(h)
        self.horizontal_line(x + r, y, w - 2 * r + 1, color)
        self.horizontal_line(x + r, y + h, w - 2 * r + 1, color)
        self.vertical_line(x, y + r, h - 2 * r + 1, color)
        self.vertical_line(x + w, y + r, h - 2 * r + 1, color)
        self.hollow_circle_helper(x + r, y + r, r, self.QUADRANT_2, color)
        self.hollow_circle_helper(x + w - r, y + r, r, self.QUADRANT_1, color)
        self.hollow_circle_helper(x + r, y + h - r, r, self.QUADRANT_3, color)
        self.hollow_circle_helper(x + w - r, y + h - r, r, self.QUADRANT_4, color)

    def filled_rounded_rectangle(self, x, y, w, h, r, color):
        """!
          @brief Draw a solid rounded rectangle
          @param x x-coordinate of the starting point of the rectangle
          @param y y-coordinate of the starting point of the rectangle
          @param w Rectangle width 
          @param h Rectangle height
          @param r Radius of the circle
          @param color Color
        """
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)
        r = abs(int(r))
        if w < 0:
            x += w
            w = abs(w)
        if h < 0:
            y += h
            h = abs(h)
        self.filled_rect(x + r, y, w - 2 * r, h, color)
        self.filled_rect(x, y + r, r, h - 2 * r, color)
        self.filled_rect(x + w - r, y + r, r, h - 2 * r, color)
        self.filled_circle_helper(x + r, y + r, r, self.QUADRANT_2, color)
        self.filled_circle_helper(x + w - r - 1, y + r, r, self.QUADRANT_1, color)
        self.filled_circle_helper(x + r, y + h - r - 1, r, self.QUADRANT_3, color)
        self.filled_circle_helper(x + w - r - 1, y + h - r - 1, r, self.QUADRANT_4, color)

    BITMAP_COMPRESSION_NO = 0
    BITMAP_COMPRESSION_RLE8 = 1
    BITMAP_COMPRESSION_RLE4 = 2
    BITMAP_COMPRESSION_FIELDS = 3

    def _bitmap_helper(self, increase_axis, static_axis, data, data_bit, exchange, color, background):
        for i in data:
            for j in range(8):
                if i & data_bit:
                    if exchange:
                        self.filled_rect(static_axis, increase_axis, self._bitmap_size, self._bitmap_size, color)
                    else:
                        self.filled_rect(increase_axis, static_axis, self._bitmap_size, self._bitmap_size, color)
                else:
                    if exchange:
                        self.filled_rect(static_axis, increase_axis, self._bitmap_size, self._bitmap_size, background)
                    else:
                        self.filled_rect(increase_axis, static_axis, self._bitmap_size, self._bitmap_size, background)
                increase_axis += self._bitmap_size
                if data_bit & 0x80:
                    i <<= 1
                else:
                    i >>= 1

    def bitmap(self, x, y, bitmap, w, h, color, background):
        """!
          @brief Draw a bitmap
          @param x Starting x-coordinate of the bitmap
          @param y Starting y-coordinate of the bitmap
          @param bitmap  Bitmap array
          @param w Bitmap width 
          @param h Bitmap height 
          @param color Bitmap color 
          @param background Bitmap background color 
        """
        if w < 0 or h < 0:
            return
        x = abs(int(x))
        y = abs(int(y))

        if self._bmp_fmt == self.BITMAP_TBMLLR:
            one_line_data_len = (w - 1) // 8 + 1
            for i in range(h):
                y_mask = y + i * self._bitmap_size
                self._bitmap_helper(x, y_mask, bitmap[i * one_line_data_len: one_line_data_len * (i + 1)], 0x80, False, color,
                                    background)
        elif self._bmp_fmt == self.BITMAP_TBMRLL:
            one_line_data_len = (w - 1) // 8 + 1
            for i in range(h):
                y_mask = y + i * self._bitmap_size
                self._bitmap_helper(x, y_mask, bitmap[i * one_line_data_len: one_line_data_len * (i + 1)], 0x01, False, color,
                                    background)
        elif self._bmp_fmt == self.BITMAP_BTMLLR:
            one_line_data_len = (w - 1) // 8 + 1
            for i in range(h):
                y_mask = y + h * self._bitmap_size - i * self._bitmap_size
                self._bitmap_helper(x, y_mask, bitmap[i * one_line_data_len: one_line_data_len * (i + 1)], 0x80, False, color,
                                    background)
        elif self._bmp_fmt == self.BITMAP_BTMRLL:
            one_line_data_len = (w - 1) // 8 + 1
            for i in range(h):
                y_mask = y + h * self._bitmap_size - i * self._bitmap_size
                self._bitmap_helper(x, y_mask, bitmap[i * one_line_data_len: one_line_data_len * (i + 1)], 0x01, False, color,
                                    background)
        elif self._bmp_fmt == self.BITMAP_LRMTLB:
            one_line_data_len = (h - 1) // 8 + 1
            for i in range(w):
                x_mask = x + i * self._bitmap_size
                self._bitmap_helper(y, x_mask, bitmap[i * one_line_data_len: one_line_data_len * (i + 1)], 0x80, True, color,
                                    background)
        elif self._bmp_fmt == self.BITMAP_LRMBLT:
            one_line_data_len = (h - 1) // 8 + 1
            for i in range(w):
                x_mask = x + i * self._bitmap_size
                self._bitmap_helper(y, x_mask, bitmap[i * one_line_data_len: one_line_data_len * (i + 1)], 0x01, True, color,
                                    background)
        elif self._bmp_fmt == self.BITMAP_RLMTLB:
            one_line_data_len = (h - 1) // 8 + 1
            for i in range(w):
                x_mask = x + w * self._bitmap_size - i * self._bitmap_size
                self._bitmap_helper(y, x_mask, bitmap[i * one_line_data_len: one_line_data_len * (i + 1)], 0x80, True, color,
                                    background)
        elif self._bmp_fmt == self.BIMTAP_RLMBLT:
            one_line_data_len = (h - 1) // 8 + 1
            for i in range(w):
                x_mask = x + w * self._bitmap_size - i * self._bitmap_size
                self._bitmap_helper(y, x_mask, bitmap[i * one_line_data_len: one_line_data_len * (i + 1)], 0x01, True, color,
                                    background)

    def bitmap_file(self, x, y, path):
        """!
          @brief Draw a bitmap
          @param x Starting x-coordinate of the bitmap
          @param y Starting y-coordinate of the bitmap
          @param path  Bitmap file path 
        """
        try:
            f = open(path, "rb")
        except:
            print("open file error")
            return
        c = bytearray(f.read())
        f.close()
        if c[0] != 0x42 and c[1] != 0x4d:
            print("file error")
            print(c[0])
            print(c[1])
            return
        dib_offset = self._bytes_to_number(c[10:14])
        width = self._bytes_to_number(c[18:22])
        height = self._bytes_to_number(c[22:26])
        color_bits = self._bytes_to_number(c[28:30])
        compression = self._bytes_to_number(c[30:32])
        # print("w: %d, h: %d, color_bits: %d" %(width, height, color_bits))

        if color_bits == 24:
            width3 = width * 3
            for i in range(height):
                self.start_draw_bitmap_file(x, y + height - i)
                buf = []
                left = dib_offset + i * width3
                i = 0
                while i < width3:
                    buf.append(c[left + i + 2])
                    buf.append(c[left + i + 1])
                    buf.append(c[left + i + 0])
                    i += 3
                self.bitmap_file_helper(buf)
            self.end_draw_bitmap_file()

        elif color_bits == 1:
            quads = self._get_quads(c, 2)
            addr = dib_offset
            if compression == self.BITMAP_COMPRESSION_NO:
                addr_count_complement = (width // 8 + 1) % 4
                if addr_count_complement != 0:
                    addr_count_complement = 4 - addr_count_complement
                for i in range(height):
                    w = width
                    addr_count = 0
                    self.start_draw_bitmap_file(x, y + height - i - 1)
                    buf = []
                    while w > 0:
                        d = c[addr + addr_count]
                        addr_count = addr_count + 1
                        j = 8
                        while w > 0 and j > 0:
                            j -= 1
                            quad = d & (0x01 << j)
                            if quad > 0:
                                quad = 1
                            buf.append(quads[quad][2])
                            buf.append(quads[quad][1])
                            buf.append(quads[quad][0])
                            w -= 1
                    self.bitmap_file_helper(buf)
                    addr_count += addr_count_complement
                    addr += addr_count
                self.end_draw_bitmap_file()
        else:
            print("dont support this bitmap file format yet")

    def write_one_char(self, c):
        """!
          @brief Dispaly a char on the screen 
          @param c char data 
        """
        if len(c) > 1:
            c = c[0]
        (l, width, height, fmt) = self._fonts.get_one_character(c)
        temp = self._bmp_fmt
        self._bmp_fmt = fmt
        ts = self._text_size
        if ord(c) == ord("\n"):
            self._text_cursor_x = 0
            self._text_cursor_y += height * ts + self._text_interval_col
        elif len(l):
            temp1 = self._bitmap_size
            self._bitmap_size = ts
            self._text_cursor_x += self._text_interval_row
            if self._text_cursor_x + ts * width > self._width:
                self.filled_rect(self._text_cursor_x, self._text_cursor_y, self._width - self._text_cursor_x,
                                 self._fonts._extension_fonts_height * ts + self._text_interval_col, self._text_background)
                self._text_cursor_x = self._text_interval_row
                self._text_cursor_y += ts * self._fonts._extension_fonts_height + self._text_interval_col
            self.filled_rect(self._text_cursor_x, self._text_cursor_y,
                             self._fonts._extension_fonts_width * ts + self._text_interval_row,
                             self._fonts._extension_fonts_height * ts + self._text_interval_col, self._text_background)
            self.bitmap(self._text_cursor_x, self._text_cursor_y, l, width, height, self._text_color, self._text_background)
            self._text_cursor_x += ts * width
            self._bitmap_size = temp1
        self._bmp_fmt = temp

    def _bytes_to_number(self, data):
        r = 0
        i = len(data)
        while i > 0:
            i -= 1
            r = r << 8 | data[i]
        return r

    def _get_quads(self, data, count):
        r = []
        for i in range(count):
            r.append(data[i * 4 + 54: i * 4 + 58])
        return r

    def _ternary_expression(self, condition, o1, o2):
        if condition:
            return o1
        return o2

    def _get_direction(self, value):
        if value >= 0:
            return 1
        return -1


class DFRobot_RPi_Eink_Display(DFRobot_Display):
    XDOT = 128
    YDOT = 250
    HEIGHT = 122
    WIDTH = 250
    GDEH0213B7_SERIES = 3
    GDEH0213B1 = 2
    FULL = True
    PART = False
    VERSION = GDEH0213B7_SERIES
    is_full = True

    def __init__(self, bus, dev, cs, cd, busy, rst):
        DFRobot_Display.__init__(self, self.WIDTH, self.HEIGHT)
        self._busy = GPIO(busy, GPIO.IN)
        self._spi = SPI(bus, dev)
        self._cs = GPIO(cs, GPIO.OUT)
        self._cd = GPIO(cd, GPIO.OUT)
        self._rst = GPIO(rst, GPIO.OUT)
        length = 4000
        self._display_buffer = bytearray(length)
        i = 0
        while i < length:
            self._display_buffer[i] = 0x00
            i = i + 1
        self._is_busy = False
        self._busy_exit_edge = GPIO.RISING
        self._fonts.set_fonts(fonts_6_8)
        self.set_ex_fonts_fmt(16, 16)

    def write_cmd_and_data(self, cmd, data=[]):
        # self._wait_busy_exit()
        self._cs.set_out(GPIO.LOW)
        self._cd.set_out(GPIO.LOW)
        self._spi.transfer([cmd])
        # if(cmd == 0x82) time.sleep(0.1)
        if len(data):
            self._cd.set_out(GPIO.HIGH)
            self._spi.transfer(data)
        self._cs.set_out(GPIO.HIGH)

    def write_data(self, data):
        # self._wait_busy_exit()
        self._cs.set_out(GPIO.LOW)
        self._cd.set_out(GPIO.HIGH)
        self._spi.transfer([data])
        self._cs.set_out(GPIO.HIGH)

    def set_busy_exit_edge(self, edge):
        if edge != GPIO.HIGH and edge != GPIO.LOW:
            return
        self._busy_edge = edge

    def begin(self):
        """!
          @brief Initialize and obtain the ID of the Raspberry Pi e-ink screen
        """
        version = self.read_id()
        if version[0] == 0x01:
            self.VERSION = self.GDEH0213B1
        else:
            self.VERSION = self.GDEH0213B7_SERIES

    def pixel(self, x, y, color):
        """!
          @brief Draw a point on the screen at (x,y) coordinate
          @param x x-axis coordinate
          @param y y-axis coordinate
          @param color  Color
        """
        if x < 0 or x >= self._width:
            return
        if y < 0 or y >= self._height:
            return
        x = int(x)
        y = int(y)
        m = int(x * 16 + (y + 1) / 8)
        sy = int((y + 1) % 8)
        if color == self.WHITE:
            if sy != 0:
                self._display_buffer[m] = self._display_buffer[m] | int(pow(2, 8 - sy))
            else:
                self._display_buffer[m - 1] = self._display_buffer[m - 1] | 1
        elif color == self.BLACK:
            if sy != 0:
                self._display_buffer[m] = self._display_buffer[m] & (0xff - int(pow(2, 8 - sy)))
            else:
                self._display_buffer[m - 1] = self._display_buffer[m - 1] & 0xfe

    def flush(self, mode):
        """!
          @brief Send the prepared screen image buffer to the e-ink screen for display
          @param mode: Display mode, FULL: full screen refresh, PART: partial refresh
        """
        if mode != self.FULL and mode != self.PART:
            return
        if self.is_full is True and mode == self.PART:
            self.set_part_ram()
            self.is_full = False
        if mode == self.FULL:
            self.is_full = True
        if mode == self.PART:
            self._dis_part(0, 249, 249, 128)
        else:
            self._dis_all()
            self._sleep()

    def start_draw_bitmap_file(self, x, y):
        """!
          @brief Draw a bitmap
          @param x Starting x-coordinate of the bitmap
          @param y Starting y-coordinate of the bitmap
        """
        self._bitmap_file_start_x = x
        self._bitmap_file_start_y = y

    def bitmap_file_helper(self, buf):
        """!
          @brief Move the bitmap data buffer to the screen image buffer according to the rules
          @param buf Bitmap data buffer to be sent
        """
        for i in range(len(buf) // 3):
            addr = i * 3
            if buf[addr] == 0x00 and buf[addr + 1] == 0x00 and buf[addr + 2] == 0x00:
                self.pixel(self._bitmap_file_start_x, self._bitmap_file_start_y, self.BLACK)
            else:
                self.pixel(self._bitmap_file_start_x, self._bitmap_file_start_y, self.WHITE)
            self._bitmap_file_start_x += 1

    def end_draw_bitmap_file(self):
        """!
          @brief Send out the prepared screen image buffer and display the bitmap on the e-ink 
        """
        # self.flush(self.PART)
        time.sleep(0.01)

    def clear_screen(self):
        """!
          @brief Clear the content displayed on the e-ink screen
        """
        self.clear(self.WHITE)
        self.flush(self.FULL)
        if self.VERSION == self.GDEH0213B7_SERIES:
            time.sleep(0.1)
        elif self.VERSION == self.GDEH0213B1:
            time.sleep(0.1)

    def set_version(self, version):
        """!
          @brief Manually set the version number of the screen
        """
        self.VERSION = version

    def read_id(self):
        """!
          @brief Get the ID of the e-ink screen
        """
        self.write_cmd_and_data(0x2f, [])
        return self.read_data(1)

    def read_busy(self):
        return self._busy.read()
        # time.sleep(0.1)

    def read_data(self, n):
        self._cs.set_out(GPIO.LOW)
        self._cd.set_out(GPIO.HIGH)
        data = self._spi.read_data(n)
        self._cs.set_out(GPIO.HIGH)
        return data

    def reset(self):
        self._rst.set_out(GPIO.LOW)
        time.sleep(0.01)
        self._rst.set_out(GPIO.HIGH)
        time.sleep(0.01)

    def set_busy_cb(self, cb):
        self._busy.set_interrupt(self._busy_exit_edge, cb)

    def _set_ram_data(self, x_start, x_end, y_start, y_start1, y_end, y_end1):
        self.write_cmd_and_data(0x44, [x_start, x_end])
        self.write_cmd_and_data(0x45, [y_start, y_start1, y_end, y_end1])

    def _set_ram_pointer(self, x, y, y1):
        self.write_cmd_and_data(0x4e, [x])
        self.write_cmd_and_data(0x4f, [y, y1])

    def _init(self, mode):
        self.reset()
        self._wait_busy_exit()
        self.write_cmd_and_data(0x12, [])
        self._wait_busy_exit()
        self.write_cmd_and_data(0x01, [0xf9, 0x00, 0x00])
        self.write_cmd_and_data(0x11, [0x01])
        self.write_cmd_and_data(0x44, [0x00, 0x0f])
        self.write_cmd_and_data(0x45, [0xf9, 0x00, 0x00, 0x00])
        self.write_cmd_and_data(0x3c, [0x05])
        self.write_cmd_and_data(0x21, [0x00, 0x80])
        self.write_cmd_and_data(0x18, [0x80])
        self.write_cmd_and_data(0x4e, [0x00])
        self.write_cmd_and_data(0x4f, [0xf9, 0x00])
        self._wait_busy_exit()
        self.write_cmd_and_data(0x0c, [0xf4, 0xf4, 0xf4, 0x0f])

    def _write_dis_ram(self, size_x, size_y):
        if size_x % 8 != 0:
            size_x = size_x + (8 - size_x % 8)
        size_x = size_x // 8

        self.write_cmd_and_data(0x24, self._display_buffer[0: size_x * size_y])

    def _sleep(self):
        self.write_cmd_and_data(0x10, [0x01])
        time.sleep(0.1)

    def _update_dis(self, mode):
        if mode == self.FULL:
            self.write_cmd_and_data(0x22, [0xc7])
        elif mode == self.PART:
            if self.VERSION == self.GDEH0213B7_SERIES:
                self.write_cmd_and_data(0x22, [0x0C])
            elif self.VERSION == self.GDEH0213B1:
                self.write_cmd_and_data(0x22, [0xc7])
        else:
            return
        self.write_cmd_and_data(0x20, [])

    def _wait_busy_exit(self):
        #temp = 0
        while self.read_busy():
            time.sleep(0.01)
            #temp = temp + 1
            #if (temp % 200) == 0:
            #    print("Wait Busy Exit")

    def _power_on(self):
        self.write_cmd_and_data(0x22, [0xC0])
        self.write_cmd_and_data(0x20, [])

    def _power_off(self):
        self.write_cmd_and_data(0x10, [0x01])
        time.sleep(0.1)

    def set_part_ram(self):
        # print("set part")
        self._init(self.PART)
        self.write_cmd_and_data(0x24, [])
        for i in range(0, 4000):
            self.write_data(0x00)
        self.write_cmd_and_data(0x26, [])
        for i in range(0, 4000):
            self.write_data(0x00)
        self._wait_busy_exit()
        self.write_cmd_and_data(0x37, [0x00, 0x40, 0x20, 0x10, 0x00, 0x00, 0x00, 0x00])
        self.write_cmd_and_data(0x22, [0xf4])
        self.write_cmd_and_data(0x20, [])
        self._wait_busy_exit()

        self.write_cmd_and_data(0x24, [])
        for i in range(0, 4000):
            self.write_data(0x00)
        self.write_cmd_and_data(0x26, [])
        for i in range(0, 4000):
            self.write_data(0x00)

    def _dis_part(self, x_start, y_start, width, height):
        x_start = x_start // 8
        x_end = x_start + height// 8 - 1

        y_start1 = 0
        y_start2 = y_start
        if y_start >= 256:
            y_start1 = y_start2 // 256
            y_start2 = y_start2 % 256
        
        y_end1 = 0
        y_end2 = y_start + width - 1
        if y_end2 >= 256:
            y_end1 = y_end2 // 256
            y_end2 = y_end2 % 256

        self.write_cmd_and_data(0x44, [x_start, x_end])
        self.write_cmd_and_data(0x45, [y_start2, y_start1, y_end2, y_end1])
        self.write_cmd_and_data(0x4E, [x_start])
        self.write_cmd_and_data(0x4F, [y_start2, y_start1])
        self.write_cmd_and_data(0x24, self._display_buffer[0:4000])
        self._wait_busy_exit()
        self.write_cmd_and_data(0x37, [0x00, 0x40, 0x20, 0x10, 0x00, 0x40, 0x00, 0x00])
        self.write_cmd_and_data(0x3C, [0x80])
        self.write_cmd_and_data(0x22, [0x3C])
        self.write_cmd_and_data(0x20, [])
        self._wait_busy_exit()

    def _dis_all(self):
        self._init(self.PART)
        self.write_cmd_and_data(0x24, self._display_buffer[0: 4000])
        self.write_cmd_and_data(0x26, [])
        for i in range(0, 4000):
            self.write_data(0x0)
        self.write_cmd_and_data(0x37, [0x00, 0x40, 0x20, 0x10, 0x00, 0x00, 0x00, 0x00])
        self.write_cmd_and_data(0x22, [0xf4])
        self.write_cmd_and_data(0x20, [])

    def __del__(self):
        self._busy.cleanup()
