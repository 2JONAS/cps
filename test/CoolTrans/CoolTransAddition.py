import os
import time
import module_3.module_3_process  as module_3_process
import utils
from utils import exceptProcess
import sys
import numpy as np

module_code = '502'



root_dir = os.getcwd()
class COOTRANS(object):
    pass

task_id = '5_1556417987936_00'
#task_id = '5_1556417189387_00'



class COOTRANS(object):
    def __init__(self,mongodb,messenger,exceptProcess,FileManagement,task_id):
        self.mongodb = mongodb
        self.messenger = messenger
        self.exceptProcess = exceptProcess
        self.task_id = task_id
        self.DefaultCase = self.dafaultcase()
        self.model_id = '502'
        self.root_dir = os.get_cwd()
        self.file_group = FileManagement(os.path.join(root_dir,'module_3'))
        self.num_per_border = 11
        self.time_now = str(time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(time.time())))
        
    def dafaultcase(self):
        self.data = exceptProcess.saferun(self.mongodb.query_taskid,[self.task_id],'mongodb_data_get_error')
        return self.data['position']['DefaultCase']
    def run(self):
        if self.DefaultCase == 0:
            self.run_single()
        else:
            self.run_multi()
    def run_single(self):
        self.messenger.info_write(0.1)
        position = self.single_data_pre()
        self.out = self.run4thermo_calc(position,self.time_now)
        self.insert_data()
    def run_multi(self):
        self.messenger.info_write(0.1)
        self.out = []
        positions = self.multi_data_pre()
        for i in range(self.num_per_border*2):
            position = positions[i]
            out = self.run4thermo_calc(position,self.time_now+'_'+str(i))
            self.out.append(out)
        self.insert_data()
        
        
    
    def single_data_pre(self):
        position = self.data["input_data"]
        position['C_wt'],position['Mn_wt'],position['Si_wt'] = position['component']
        position['V'] = abs(int((position['T'][-1] - position['T'][0])/(position['t'][-1] - position['t'][0])))
        
    def multi_data_pre(self):
        position = self.data["input_data"]
        position['C_wt'],position['Mn_wt'],position['Si_wt'] = position['component']
        
        BORDER_T = np.array(position['BORDER_T'])
        CENTER_T = np.array(position['CENTER_T'])
        border_T = BORDER_T.T.tolist()
        center_T = CENTER_T.T.tolist()
        positions = []
        for i in border_T:
            dict_ = position.copy()
            dict_['T'] = [i]
            dict_['t'] = [position['BORDER_t']]
            dict_['V'] = abs(int((dict_['T'][-1] - dict_['T'][0])/(dict_['t'][-1] - dict_['t'][0])))
            positions.append(dict_)
        for i in center_T:
            dict_ = position.copy()
            dict_['T'] = [i]
            dict_['t'] = [position['CENTER_t']]
            dict_['V'] = abs(int((dict_['T'][-1] - dict_['T'][0])/(dict_['t'][-1] - dict_['t'][0])))
            positions.append(dict_)
        return positions
    def insert_data(self):
        self.data.pop("input_data")
        self.data["output_data"] = self.out    
        exceptProcess.saferun(self.mongodb.out_insert_dict,[self.data],'insert_error')
        self.messenger.info_write(1)
        
    def run4thermo_calc(self,position,file_prefix='',):
        in_file = os.path.join(self.file_group.module_dir,'Site-frac-steel1.tcm')
        out_file_path =file_prefix 
        out_file_dir = os.path.join(self.file_group.module_run_dir,out_file_path)
        os.mkdir(out_file_dir)
        out_file = os.path.join(out_file_dir,'Site-frac-steel1.tcm')
        module_3_process.change_data_in_cm(in_file,out_file,position)
        os.chdir(out_file_dir)
        os.popen(out_file)
        dead_wait = 1
        for i in range(80):
            time.sleep(2)
            if len(os.listdir(out_file_dir)) == 2:
                dead_wait = 0
                break
        if dead_wait == 1:
            print('creat first txt error')
        os.system('taskkill /f /im javaw.exe')
        self.messenger.info_write(0.25/self.num_per_border)
        
        txt1_file = os.path.join(out_file_dir,'Site-fra-steel1.txt') 
        module_3_process.steel1_read_data_from_txt1(txt1_file,position)
        in_file = os.path.join(self.file_group.module_dir,'Pearlite-steel1.dcm')
        out_file = os.path.join(out_file_dir,'Pearlite-steel1.dcm')
        module_3_process.change_data_in_cm(in_file,out_file,position)
        os.popen(out_file)
        ##最大等40s
        dead_wait = 1
        for i in range(80):
            time.sleep(2)
            ##5个文件都创建后才能读取txt
            if len(os.listdir(out_file_dir)) > 4 :
                
                dead_wait = 0
                break
        if dead_wait == 1:
            print('create second file error')
        os.system('taskkill /f /im javaw.exe')
        txt2_file = os.path.join(out_file_dir,'Pearlite-steel1.txt')
        module_3_process.steel1_read_data_from_txt2(txt2_file,position)
        self.messenger.info_write(0.5/self.num_per_border)
        
        
        spacing_of_sorbite = position['txt2_value']
        soxhlet_size = float(spacing_of_sorbite[0]) * 18
        r = module_3_process.ferrite_solubility(position,self.file_group.module_dir,self.file_group.module_run_dir,out_file_dir) #铁素体固溶度
        self.messenger.info_write(0.75/self.num_per_border)
        fsc = module_3_process.calcu_fsc(position,self.file_group.module_dir,self.file_group.module_run_dir,out_file_dir)
        phase_composition = fsc + [r]
        out = {'spacing_of_sorbite':spacing_of_sorbite,'soxhlet_size':soxhlet_size,'phase_composition':phase_composition}
        return out


    
        