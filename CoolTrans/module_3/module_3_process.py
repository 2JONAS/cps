# -*- coding: utf-8 -*-



import os
import time
import numpy as np
import psutil

##填充tcm数据
def change_data_in_cm(in_file_path,out_file_path,data_base):
    
    write = []
    s = ''
    with open(in_file_path,"r") as f:    #设置文件对象
        for index,line in enumerate(f.readlines()):
            
            if '%' in line:
                char_index = 0
                new_line = line
                while char_index<len(line):
                    if line[char_index] == '%':
                        sub_index = char_index + 1
                        while line[sub_index] != '%':
                            sub_index = sub_index + 1 
                        key = line[char_index+1:sub_index]
                        new_line=new_line.replace('%'+key+'%',str(data_base[key]))
                        char_index = sub_index
                    char_index = char_index + 1
                line = new_line
            write.append(line)
        s = ''.join(write)
        #print(1,s)
        
    fp = open(out_file_path,'w')
    
    fp.write(s)
    fp.close()
    #print(s)
##从txt文件中读取计算后的MN Si等数据
def steel1_read_data_from_txt1(in_file_path,data_base):
    with open(in_file_path,"r") as f:
        flag = 0
        ##Sublattice是标志物是分界线
        for line in f.readlines():
            if 'Sublattice' not in line and flag ==0:
                continue
            else:
                flag = 1
            line = line.strip()
            line_list = line.strip(' ').split(' ')
            
            new_list = []
            for char in line_list:
                if '' == char:
                    continue
                else:
                    new_list.append(char)
            #print(new_list)
            l = ['MN','SI','C']
            for char in l:
                if char in new_list:
                    data_base[char] = new_list[new_list.index(char) + 1]
def steel1_read_data_from_txt2(in_file_path,data_base):
        with open(in_file_path,"r") as f:
            flag = 0
            whole = []
            for line in f.readlines():
                line=line.strip()
                line_list = line.strip(' ').split(' ')
                #line_list[-1] = line_list[-1][:-2]
                new_list = []
                for char in line_list:
                    if '' == char:
                        continue
                    else:
                        new_list.append(char)
                if 'M' in new_list and flag==0:
                    first_value = float(new_list[new_list.index('M')-1])
                    flag = 1
                whole.append(new_list)
                
            second_vaule = float(whole[-2][-1])
            #value = (first_value+second_vaule)/2 * pow(10,6)
            value = second_vaule  * pow(10,6)
            data_base['txt2_value'] = [str(value)]



##计算铁素体固溶度用
def steel1_read_data_from_output_1(in_file_path):
        result = []
        with open(in_file_path,"r") as f:
            
            whole = []
            for line in f.readlines():
                line=line.strip()
                if 'E-' in line and 'E+' in line:
                    line_list = line.strip(' ').split(' ')
                    #line_list[-1] = line_list[-1][:-2]
                   
                    for char in line_list:                    
                        
                        if 'E-' in char:
                            x = float(char)
                        if 'E+' in char:
                            y = float(char)
                    whole.append([x,y])
            
            for index,xy in enumerate(whole):
                if xy[0] > 8.2 * 1E-3 and index+1<len(whole)-1 and whole[index+1][0] < 8.2 * 1E-3 and xy[0] - whole[index+1][0]<1E-3:
                    if abs(xy[0]-8.2 * 1E-3) < abs(whole[index+1][0] - 8.2 * 1E-3):
                        result.append(whole[index][1])
                    else:
                        result.append(whole[index+1][1])
                    
            m = [] 
            
            for i in range(0,len(whole)):
                if whole[i][0] >= 7.5E-3 and whole[i][0] <= 9E-3:
                    m.append(i)
            
            #print(m)
            for i in range(0,len(m)):
                if m[i] + 1 != m[i+1]:
                    break_point = i
                    #print(break_point)
                    break
            #print(1111)
            first = m[0:break_point+1]
            second = m[break_point+1:]
            x = []
            y = []
            for i in first:
                x.append(whole[i][0])
                y.append(whole[i][1])
            a1,b1=Least_squares(x,y)
            x = []
            y = []
            for i in second:
                x.append(whole[i][0])
                y.append(whole[i][1])
            a2,b2=Least_squares(x,y)
            x0 = (b1-b2)/(a2-a1)
            y0 = a1*x0 + b1
            #print(x0,y0)
            result.append(float('%.1f' % y0))
            result.append(float('%.1f' % x0))
            return result
def Least_squares(x,y):
    N = len(x)
    x_ = sum(x)/N
    y_ = sum(y)/N
    m = np.zeros(1)
    n = np.zeros(1)
    k = np.zeros(1)
    p = np.zeros(1)
    for i in np.arange(0,N):
        k = (x[i]-x_)* (y[i]-y_)
        m += k
        p = np.square( x[i]-x_ )
        n = n + p
    a = m/n
    b = y_ - a* x_
    return a,b
def steel1_read_data_from_output_2(in_file_path):
    #result = []
    with open(in_file_path,"r") as f:
        
        #whole = []
        lines = []
        for line in f.readlines():
            line = line.replace(' ','\n')
            line = line.strip()
            line = line.split('\n')
            for char in line:
                if char != '\n' and char != '':
                    lines.append(char)
        #print(lines)
        flag = 0
        for index,char in enumerate(lines):
        
            #print(char)
            if 'fractions' in char:
                #print('fractions')
                flag = 1                    
            if 'SI' ==  char and flag:
                SI = lines[index+1]
                
            if 'C' == char and flag:
                C = lines[index+1]
                break
            if 'MN' == char and flag:
                MN = lines[index+1]
        SI = str(round(float(SI)*100,3))
        C = str(round(float(C)*100,3))
        MN = str(round(float(MN)*100,3))
        return [C,MN,SI]
def run_second_tcm(input_dict,out_file_dir,module_3_model_steel1_dir):
    in_file = os.path.join(module_3_model_steel1_dir,'ferrite_solubility.tcm')
    out_file = os.path.join(out_file_dir,'ferrite_solubility.tcm')
    change_data_in_cm(in_file,out_file,input_dict)
    #print('begin')
    os.chdir(out_file_dir)
    os.popen(out_file)
    #print('end')
    
    dead_wait = 1
    for i in range(80):
        time.sleep(2)
        if 'output_2.txt' in os.listdir(out_file_dir):
            time.sleep(2)
            dead_wait = 0
            break
    if dead_wait == 1:
        print('creat second txt error')
    
    txt2_file = os.path.join(out_file_dir,'output_2.txt')
    return steel1_read_data_from_output_2(txt2_file)
def ferrite_solubility(input_dict,module_3_model_steel1_dir,module_3_run_dir,out_file_dir):
    
    return run_second_tcm(input_dict,out_file_dir,module_3_model_steel1_dir)
    

#计算铁素体，锁实体，渗碳体
def run_dcm(input_dict,model_path,run_path):
    #os.mkdir(run_path)
    out_file = os.path.join(run_path,model_path.split('\\')[-1])
    change_data_in_cm(model_path,out_file,input_dict)
    
    os.chdir(run_path)
    os.popen(out_file.split('\\')[-1])
    dead_wait = 1
    for i in range(500):
        time.sleep(2)
        if input_dict['output'] in os.listdir(run_path):
            time.sleep(2)
            dead_wait = 0
            break
    if dead_wait == 1:
        print('creat second txt error')
    taskkill()
    time.sleep(3)
    
    return input_dict['output']
#input:input_dict,run_path
#return one value
def read_output(in_file_path):
    with open(in_file_path,"r") as f:
            
            whole = []
            for line in f.readlines():
                line=line.strip()
                line_list = line.strip(' ').split(' ')
                #line_list[-1] = line_list[-1][:-2]
                new_list = []
                for char in line_list:
                    if '' == char:
                        continue
                    else:
                        new_list.append(char)
                
                whole.append(new_list)
#            w = whole[-2][-1]
#            w = float(w)
#            w = w * 6E6 * 100 / 第二个模块算出来的晶粒尺寸
            return whole[-2][-1]
#input_dict = {'C_wt':'0.82','Mn_wt':'0.52','Si_wt':'0.2','V':'8','T0':'974.7','T1':'981','T2':'957','X0':'0.000191','grain_size ':'30'}
#for key in input_dict:
#    input_dict[key] = float(input_dict[key])
#计算铁素体，锁实体，渗碳体
def calcu_fsc(input_dict,module_3_model_steel1_dir,module_3_run_dir,out_file_dir):
    temp = (float(input_dict['T1']) - float(input_dict['T0']))/float(input_dict['V'])
    temp = str(temp)
    temp = temp.split('.')[0] + '.'+temp.split('.')[1][:3]
    input_dict['(T1-T0)/V'] = temp
    run_path = out_file_dir
    run_path = os.path.join(module_3_run_dir,run_path)
    if input_dict['fer']:
        input_dict['output'] = 'ferrite_fraction.txt'
        model_path = os.path.join(module_3_model_steel1_dir,'ferrite_fraction.dcm')
        
        ferrite_fraction = float(read_output(run_dcm(input_dict,model_path,run_path))) * 1E7 
        cementite_fraction = 0 
        soxhlet = 100 - ferrite_fraction
        ferrite_fraction = round(ferrite_fraction, 3)
        soxhlet = round(soxhlet, 3)
        return [str(ferrite_fraction),str(soxhlet),str(cementite_fraction)]
        #print(read_output(run_dcm(input_dict,model_path,run_path)),0)
    else:
        input_dict['output'] = 'cementite_fraction.txt'
        model_path = os.path.join(module_3_model_steel1_dir,'cementite_fraction.dcm')
        #print(read_output(run_dcm(input_dict,model_path,run_path)),0)
        cementite_fraction = float(read_output(run_dcm(input_dict,model_path,run_path))) *  1E7
        ferrite_fraction = 0 
        soxhlet = 100 - cementite_fraction
        ferrite_fraction = round(ferrite_fraction, 3)
        soxhlet = round(soxhlet,3)
        cementite_fraction = round(cementite_fraction,3)
        return [str(ferrite_fraction),str(soxhlet),str(cementite_fraction)]
    
def taskkill():
    pids = psutil.pids()
    try:
        for pid in pids:    
            p = psutil.Process(pid)
            if 'javaw.exe' in p.name():
                os.popen('taskkill /f /im javaw.exe')
                break
    except:
        os.popen('taskkill /f /im javaw.exe')
    time.sleep(5)
    
            

