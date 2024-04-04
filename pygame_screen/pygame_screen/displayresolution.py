from enum import *

# Reference:
# https://en.wikipedia.org/wiki/List_of_common_resolutions
# https://emulation.gametechwiki.com/index.php/Resolution


class DisplayResolution(Enum):
    """Enum-class with display resolutions."""

    A2600 = (160, 192)
    DS = (256, 192)
    DVD_NTSC = (720, 576)
    DVD_PAL = (720, 480)
    FHD = (1920, 1080)
    GB = (160, 144)
    GBA = (240, 160)
    GG = (160, 144)
    GGC = (160, 144)
    NES = (256, 240)
    NHD = (640, 360)
    PSP = (480, 272)
    QHD = (960, 540)
    QVGA = (320, 240)
    SMS_192 = (256, 192)
    SMS_224 = (256, 224)
    SMS_240 = (256, 240)
    SVGA = (800, 600)
    VB = (384, 224)
    VGA = (640, 480)
    WVGA = (768, 480)
    WXGA = (1280, 720)
