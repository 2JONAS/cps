import time
time.sleep(0)
import win32gui
import win32con
import win32api
import os
from pymouse import PyMouse
from pykeyboard import PyKeyboard

m = PyMouse()
k = PyKeyboard()
#m.move(530,700)

x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)   #获得屏幕分辨率X轴

y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)   #获得屏幕分辨率Y轴

x_ = 817
y_ = 1017
print(int(x_/1920*x),int(y_/1080*y))
m.move(int(x_/1920*x),int(y_/1080*y))