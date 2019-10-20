# -*- coding: utf-8 -*-

import win32gui
import win32con
import os
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time
import numpy as np

def bigwindow():
        hld=win32gui.FindWindow(None,'Export window as dataset')
        #hld=win32gui.FindWindow(None,'Display MICRESS 7.1.2')
        button=win32gui.FindWindowEx(hld,None, "Button",None)
        win32gui.SendMessage(hld,win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)
        print('bigwindow')
def mcr(file_name,out_file_name):
    #file_name = 'Grain_Growth_Solute_Drag_phas.mcr'
    #file_name = os.path.join('mcr',file_name)
    #out_file_name = 'out8.txt'
    #out_file_name = os.path.join(os.getcwd(),out_file_name)
    os.popen(file_name)
    time.sleep(2)
    m = PyMouse()
    k = PyKeyboard()
    #m.move(500,500)
    #m.click(500,500)
    time.sleep(0.1)
    m.click(530,700)
    k.tap_key(k.tab_key)
    time.sleep(0.1)
    k.tap_key(k.tab_key)
    ##这里要下移150次
    for i in range(150):
        k.tap_key(k.down_key)
        time.sleep(0.001)
#    time.sleep(2)
#    time.sleep(3)
    k.tap_key(k.shift_key)
    #k.release_key(k.shift_key)
    k.tap_key('f')
    time.sleep(0.1)
    k.tap_key('d')
    
    time.sleep(10)
    bigwindow()
    
    k.tap_key(k.tab_key,3)
    for i in out_file_name:
        k.tap_key(i)
    k.tap_key(k.tab_key)
    k.tap_key(k.down_key,2)
    k.tap_key(k.tab_key,10)

    time.sleep(5)
    
    
    
    m.click(700,800)#最大化的时候对应的位置
    
    #m.click(520,380)
    
   
    #os.system('taskkill /f /im DPMICRESS_7.1.2_x64.exe')
    
    
    time.sleep(2)
    #m.click(756,800)#最大化的时候对应的位置
    os.system('taskkill /f /im DPMICRESS_7.1.2_x64.exe')
    
    #print(1)
 
def vtk(out_txt):
    img = []
    with open(out_txt,'r') as f:
        for index,line in enumerate(f.readlines()):
            if index>=13:
                line = line.strip()
                #print(line.split(' '))
                img.append(line.split(' '))
        img.pop()
    
    img = np.array(img,dtype=np.int32)
    #print(img.shape)
    img = img.reshape(300,300)
    mask = np.zeros(img.shape)
    height,width = img.shape
    map_dict = {1:0,2:2,3:3,4:4}
    for row in range(height):
        for col in range(width):
            l = []
            l.append(img[row,col])
            if col-1>=0:
                l.append(img[row,col-1])
            if row-1>=0:
                l.append(img[row-1,col])
            if col+1<width:
                l.append(img[row,col+1])
            if row+1<height:
                l.append(img[row+1,col])
            mask[row,col] = map_dict[len(set(l))]
    return caculate_maskVtk(mask)
    
def caculate_maskVtk(mask,line_sample = 500):
    height,width = mask.shape
    def calculate_line(imgCanny,line_index):
        num = 0
        line = imgCanny[line_index]
        flag = 1
        for point_index in range(width):
            if imgCanny[line_index][point_index] == 0:
                flag = 1
            if imgCanny[line_index][point_index] != 0 and flag == 1:
                num = num + imgCanny[line_index][point_index]
                flag = 0
            #print(num,imgCanny[line_index][point_index])
        return num
    d_sum = 0
    for i in range(line_sample):
        a = np.random.randint(0,height-1)
        d_sum = d_sum + calculate_line(mask,a)
    return d_sum/line_sample
def change_data_in_cm(in_file_path,out_file_path,data_base):
    
    write = []
    s = ''
    with open(in_file_path,"r") as f:    #设置文件对象
        for index,line in enumerate(f.readlines()):
            
            if '@' in line:
                char_index = 0
                new_line = line
                while char_index<len(line):
                    if line[char_index] == '@':
                        sub_index = char_index + 1
                        while line[sub_index] != '@':
                            sub_index = sub_index + 1 
                        key = line[char_index+1:sub_index]
                        new_line=new_line.replace('@'+key+'@',str(data_base[key]))
                        char_index = sub_index
                    char_index = char_index + 1
                line = new_line
            write.append(line)
        s = ''.join(write)
        #print(1,s)
        
    fp = open(out_file_path,'w')
    
    fp.write(s)
    fp.close()
    #print(s)# -*- coding: utf-8 -*-

class KORN(object):
    # 处理一切korn后缀的文件
    # 主要相关处理有，vtk提取，vtk读取为numpy，和数值计算
    def __init__(self,filename,korn_index):
        self.file_name = filename
        self.korn_index = korn_index
        self.file_folder,self.default_folder = self.folder_set()
        
    def folder_set(self):

        file_name_split = self.file_name.split('\\')
        file_folder = '\\'.join(file_name_split[:-1])
        default_folder = '\\'.join(file_name_split[:-2])
        default_folder = os.path.join(default_folder,'{0:02d}'.format(self.korn_index))
        if not os.path.exists(default_folder):
            os.mkdir(default_folder)
        return file_folder,default_folder
    def vtk_extract(self):
        # return the last vtk file in one result
        out_file_name = os.path.join(self.default_folder,'vtk')
        os.popen(self.file_name)
        time.sleep(2)
        m = PyMouse()
        k = PyKeyboard()
        time.sleep(0.1)
        #m.click(500,500)
        #k.tap_key(k.shift_key)
        k.tap_key('f')
        time.sleep(0.1)
        k.tap_key('d')    
        time.sleep(5)
        self.bigwindow()    
        k.tap_key(k.tab_key,3)
        for i in out_file_name:
            k.tap_key(i)
        k.tap_key(k.tab_key)
        k.tap_key(k.down_key,2)#选择 vtk asici
        k.tap_key(k.tab_key,2)
        #不选择all
        #k.tap_key(k.right_key,1)# 选择 all
        k.tap_key(k.tab_key,8)
        time.sleep(3)
        #m.click(756,800)  
        m.click(822,1012)#最大化的时候对应的位置 
        #os.system('taskkill /f /im DPMICRESS_7.1.2_x64.exe')
        time.sleep(15)
        #m.click(756,800)#最大化的时候对应的位置
        os.system('taskkill /f /im DPMICRESS_7.1.2_x64.exe')
        time.sleep(3)
        print(self.default_folder)
        vtk_name = os.listdir(self.default_folder)[-1]

        self.vtk_path = os.path.join(self.default_folder,vtk_name)
        
       
    def bigwindow(self):
        hld=win32gui.FindWindow(None,'Export window as dataset')
        #hld=win32gui.FindWindow(None,'Display MICRESS 7.1.2')
        button=win32gui.FindWindowEx(hld,None, "Button",None)
        win32gui.SendMessage(hld,win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)
        print('bigwindow')
    def vtk2np(self):
        img = []
        with open(self.vtk_path,'r') as f:
            for index,line in enumerate(f.readlines()):
                if index>=13:
                    line = line.strip()
                    #print(line.split(' '))
                    img.append(line.split(' '))
            img.pop()
    
        img = np.array(img,dtype=np.int32)
        #print(img.shape)
        img = img.reshape(300,300)
        self.img = img
        
    def np_count(self,img):
        mask = np.zeros(img.shape)
        height,width = img.shape
        map_dict = {1:0,2:2,3:3,4:4}
        for row in range(height):
            for col in range(width):
                l = []
                l.append(img[row,col])
                if col-1>=0:
                    l.append(img[row,col-1])
                if row-1>=0:
                    l.append(img[row-1,col])
                if col+1<width:
                    l.append(img[row,col+1])
                if row+1<height:
                    l.append(img[row+1,col])
                mask[row,col] = map_dict[len(set(l))]
        return self.caculate_maskVtk(mask)
    def caculate_maskVtk(self,mask,line_sample = 500):
        height,width = mask.shape
        def calculate_line(imgCanny,line_index):
            num = 0
            line = imgCanny[line_index]
            flag = 1
            for point_index in range(width):
                if imgCanny[line_index][point_index] == 0:
                    flag = 1
                if imgCanny[line_index][point_index] != 0 and flag == 1:
                    num = num + imgCanny[line_index][point_index]
                    flag = 0
                #print(num,imgCanny[line_index][point_index])
            return num
        d_sum = 0
        for i in range(line_sample):
            a = np.random.randint(0,height-1)
            d_sum = d_sum + calculate_line(mask,a)
        return d_sum/line_sample