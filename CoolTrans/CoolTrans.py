import os
import time
import module_3.module_3_process  as module_3_process
import utils
from utils import exceptProcess
import sys
import numpy as np
import psutil
import json
import re

module_code = '502'
previous_code = '501'
class COOTRANS(object):
    def __init__(self,mongodb,messenger,exceptProcess,FileManagement,task_id):
        self.mongodb = mongodb
        self.messenger = messenger
        self.exceptProcess = exceptProcess
        self.task_id = task_id
        self.num_per_border = 11
        self.model_id = '502'
        self.root_dir = os.getcwd()
        self.file_group = FileManagement(os.path.join(self.root_dir,'module_3'))
        self.time_now = str(time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(time.time())))
        self.progress = 0
    def dafaultcase(self):
        self.data = exceptProcess.saferun(self.mongodb.query_taskid,[self.task_id],'mongodb_data_get_error')
        return self.data['input_data']['DefaultCase']
    def run(self):
        self.DefaultCase = self.dafaultcase()
        self.data.pop('_id')
        if self.DefaultCase == 0:
            self.run_single()
            self.num_per_border = 1
        else:
            self.run_multi()
    def run_single(self):
        self.progress = 0.1
        self.messenger.info_write(self.progress)
        position = self.single_data_pre()
        self.out = self.run4thermo_calc(position,self.time_now)
        self.insert_data()
    def run_multi(self):
        self.messenger.info_write(0.01)
        self.out = []
        positions = self.multi_data_pre()
        for i in range(self.num_per_border*2):
            position = positions[i]
            out = self.run4thermo_calc(position,self.time_now+'_'+str(i))
            self.out.append(out)
        self.insert_data()
        
    def calculate_V(self,position):
        begin = 0
        for index in range(1,len(position['T'][0])-2):
            if position['T'][0][index] < position['T'][0][index+1]:
                break
        end = index
        return abs(int((position['T'][0][end] - position['T'][0][begin])/(position['t'][0][end] - position['t'][0][begin])))
    
    def single_data_pre(self):
        
        position = self.data["input_data"]        
        position['C_wt'],position['Mn_wt'],position['Si_wt'] = position['component']
        position['V'] = self.calculate_V(position)
        #position['V'] = 10
        data_sheet = np.load('C-T1-cem.npy')
        position['T0']=975
        for index,line in enumerate(data_sheet):
            if float(line[0]) > float(position['C_wt']):
                break
        if float(position['C_wt'])>= float(data_sheet[-1][0]):
            index = len(data_sheet)
        position['T1'] = int(data_sheet[index-1][1])
        position['fer'] = data_sheet[index-1][2] == 'fer'
        return position
        
    def multi_data_pre(self):
        position = self.data["input_data"]
        position['C_wt'],position['Mn_wt'],position['Si_wt'] = position['component']
        position['T0']=975
        BORDER_T = np.array(position['BORDER_T'])
        CENTER_T = np.array(position['CENTER_T'])
        border_T = BORDER_T.T.tolist()
        center_T = CENTER_T.T.tolist()
        data_sheet = np.load('C-T1-cem.npy')
        position['T0']=975
        for index,line in enumerate(data_sheet):
            if float(line[0]) >= float(position['C_wt']):
                break
        if float(position['C_wt'])>= float(data_sheet[-1][0]):
            index = len(data_sheet)
        position['T1'] = int(data_sheet[index-1][1])
        position['fer'] = data_sheet[index-1][2] == 'fer'
        positions = []
        for i in border_T:
            dict_ = position.copy()
            dict_['T'] = [i]
            dict_['t'] = [position['BORDER_t']]
            dict_['V'] = self.calculate_V(dict_)
            #dict_['V'] = 10
            positions.append(dict_)
        for i in center_T:
            dict_ = position.copy()
            dict_['T'] = [i]
            dict_['t'] = [position['CENTER_t']]
            dict_['V'] = self.calculate_V(dict_)
            #dict_['V'] = 10
            positions.append(dict_)
        return positions
    def insert_data(self):
        try:
            self.data.pop("input_data")
        except:
            pass
        self.data["output_data"] = self.out    
        exceptProcess.saferun(self.mongodb.out_insert_dict,[self.data],'insert_error')
        self.progress = 1
        self.messenger.info_write(self.progress)
        
    def run4thermo_calc(self,position,file_prefix='',):
        in_file = os.path.join(self.file_group.module_dir,'Site-frac-steel1.tcm')
        out_file_path =file_prefix 
        out_file_dir = os.path.join(self.file_group.module_run_dir,out_file_path)
        os.makedirs(out_file_dir)
        out_file = os.path.join(out_file_dir,'Site-frac-steel1.tcm')
        module_3_process.change_data_in_cm(in_file,out_file,position)
        os.chdir(out_file_dir)
        time.sleep(0.3)
        os.popen(out_file)
        dead_wait = 1
        for i in range(100):
            time.sleep(2)
            if 'Site-fra-steel1.txt' in os.listdir(out_file_dir):
                dead_wait = 0
                break
        if dead_wait == 1:
            print('creat first txt error')
        module_3_process.taskkill()
        
        self.progress = self.progress + 0.25 / self.num_per_border / 2
        self.messenger.info_write(self.progress)
        
        txt1_file = os.path.join(out_file_dir,'Site-fra-steel1.txt') 
        module_3_process.steel1_read_data_from_txt1(txt1_file,position)
        in_file = os.path.join(self.file_group.module_dir,'Pearlite-steel1.dcm')
        out_file = os.path.join(out_file_dir,'Pearlite-steel1.dcm')
        module_3_process.change_data_in_cm(in_file,out_file,position)
        time.sleep(0.3)
        os.popen(out_file)
        ##最大等40s
        dead_wait = 1
        for i in range(100):
            time.sleep(2)
            ##5个文件都创建后才能读取txt
            if 'Pearlite-steel1.txt' in os.listdir(out_file_dir) :
                
                dead_wait = 0
                break
        if dead_wait == 1:
            print('create second file error')
        module_3_process.taskkill()
        txt2_file = os.path.join(out_file_dir,'Pearlite-steel1.txt')
        module_3_process.steel1_read_data_from_txt2(txt2_file,position)
        self.progress = self.progress + 0.25 / self.num_per_border / 2
        self.messenger.info_write(self.progress)
        
        
        spacing_of_sorbite = position['txt2_value']
        soxhlet_size = float(spacing_of_sorbite[0]) * 18
        r = module_3_process.ferrite_solubility(position,self.file_group.module_dir,self.file_group.module_run_dir,out_file_dir) #铁素体固溶度
        self.progress = self.progress + 0.25 / self.num_per_border / 2    
        self.messenger.info_write(self.progress)
        fsc = module_3_process.calcu_fsc(position,self.file_group.module_dir,self.file_group.module_run_dir,out_file_dir)
        phase_composition = fsc + [r]
        out = {'spacing_of_sorbite':[str(round(float(spacing_of_sorbite[0]),3))],'soxhlet_size':round(soxhlet_size, 3),'phase_composition':phase_composition,'C':r[0],'MN':r[1],'SI':r[2],'V':str(round(float(position['V']),3)),'T1':str(round(float(position['T1']),3))}
        return out


class UnionCoolTrans(COOTRANS):
    def __init__(self,*arg, **kwarg):
        super(UnionCoolTrans,self).__init__(*arg, **kwarg)
        self.union = self.union_check()
    def union_check(self):
        return self.task_id[0] == '0'
    def dafaultcase(self):
        if self.union:
            self.data = exceptProcess.saferun(self.mongodb.query_taskid,[self.task_id],'mongodb_data_get_error')
            #
            self.data['input_data'] = self.get_union_input_data()
            TempTime_id = self.getTempTime_id()
            border_center_data = self.get_center_border_data(TempTime_id)
            self.data['input_data']['CENTER_t'] = border_center_data['CENTER_Time']
            self.data['input_data']['CENTER_T'] = border_center_data['CENTER_Temp']
            self.data['input_data']['BORDER_t'] = border_center_data['BORDER_Time']
            self.data['input_data']['BORDER_T'] = border_center_data['BORDER_Temp']
            return True
        else:
            return super(UnionCoolTrans,self).dafaultcase()
    def getTempTime_id(self):
        inqure_id = '_'.join(self.task_id.split('_')[:-1])+'_'
        m = utils.Mongo()
        id_list = []
        for u in m.simulationOutput.find({'task_id': re.compile(inqure_id),'modelCode':previous_code}):
            id_list.append(u['task_id'])
        if len(id_list) == 0:
            self.exceptProcess.error_run('mongodb_data_get_error')
            raise Exception("previous mongodb was not found")
        def sort_key(item):
            return int(item.split('_')[-1])
        id_list.sort(key=sort_key, reverse=True)
        print(id_list[0])
        return id_list[0]
    def get_center_border_data(self,TempTime_id):
        mongo = utils.Mongo(simulationInput='SimulationOutputData')
        data = mongo.query_taskid(TempTime_id)
        data.pop('_id')
        if len(data['temp_data']['BORDER_Temp'][0]) != 11:
            print('change')
            data['temp_data']['BORDER_Temp'][0] = data['temp_data']['BORDER_Temp'][0][11:]
        
        return data['temp_data']
    def get_union_input_data(self):
        with open('union_input_data.json') as f:
            load_dict = json.load(f)
        return load_dict









if len(sys.argv) > 1:
    task_id = sys.argv[1]
    messenger = utils.MessageFeedback(task_id,module_code,'CoolTrans.info')
    exceptProcess.messenger = messenger  
    mongodb = exceptProcess.saferun(utils.Mongo,[],'other')
    A = UnionCoolTrans(mongodb,messenger,exceptProcess,utils.FileManagement,task_id)
    A.run()
else:
    print('missing task_id')
    #return 0





