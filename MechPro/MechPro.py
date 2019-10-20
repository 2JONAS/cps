# -*- coding: utf-8 -*-

import os
import time
import utils
from utils import exceptProcess
import sys
import numpy as np
import json
import re
module_code = '601'

class MechPro(object):
    def __init__(self,mongodb,messenger,exceptProcess,task_id):
        self.mongodb = mongodb
        self.messenger = messenger
        self.exceptProcess = exceptProcess
        self.task_id = task_id
        self.model_id = '601'
        self.root_dir = os.getcwd()
        self.progress = 0
    def run(self):
        
        self.param_pre()
        self.position = self.data_pre()
        self.out = self.calculate(self.position)
        self.insert_data()
    def param_pre(self):
        # a,k1,k2,k3,k4,k5,s,j1,j2,j3,j4,j5,j6,j7,j8
        #a  基数
        #k 为5个相的参数 
        #s 为尺寸参数
        #j 为成分的参数
        # 成一个列向量
        # param1是搭接
        param = [1 for i in range(15)]
        self.param1 = np.matrix(param).T
        self.param2 = np.matrix(param).T
        pass
    def calculate(self,position):
        out1 = position[0]*self.param1
        out2 = position[1]*self.param2
        out = [out1[0,0],out2[0,0]]
        return out
    def data_pre(self):
        self.data = exceptProcess.saferun(self.mongodb.query_taskid,[self.task_id],'mongodb_data_get_error')
        position = self.data['input_data']
        position = self.data['input_data']
        
        position1 = [1] +  \
        [position['SorbiteSpacing'][0]] + \
        [position['SorbiteSize'][0]]+\
        [position['Fe'][0]] + \
        [position['Sorbite'][0]] + \
        [position['Cementite'][0]] + \
        [position['size']] + \
        position['component']
        #print(len(position['component']))
        #position2 = positfdion['component']+[position['SorbiteSpacing'][1]]+[position['SorbiteSize'][1]]+[position['size']]
        position2 = [1] + \
        [position['SorbiteSpacing'][1]] + \
        [position['SorbiteSize'][1]]+\
        [position['Fe'][1]] + \
        [position['Sorbite'][1]] + \
        [position['Cementite'][1]] + \
        [position['size']] + \
        position['component']
        position1 = np.matrix(position1)
        position2 = np.matrix(position2)
        return [position1,position2]
    def insert_data(self):
        #print("insert data")
        try:
            self.data.pop("input_data")
        except:
            pass
        self.data["output_data"] = self.out    
        exceptProcess.saferun(self.mongodb.out_insert_dict,[self.data],'insert_error')
        self.progress = 1
        self.messenger.info_write(self.progress)
class UnionMechPro(MechPro):
    def __init__(self,*arg, **kwarg):
        super(UnionMechPro,self).__init__(*arg, **kwarg)
        self.union = self.union_check()
        self.previous_code_1 = '502'
        self.previous_code_2 = '403'
    def union_check(self):
        return self.task_id[0] == '0'
    def fault_data_pre(self):
        position = self.data['input_data']
        position = self.data['input_data']
        
        position1 = [1] +  \
        [position['SorbiteSpacing'][0]] + \
        [position['SorbiteSize'][0]]+\
        [position['Fe'][0]] + \
        [position['Sorbite'][0]] + \
        [position['Cementite'][0]] + \
        [position['size']] + \
        position['component']
        #print(len(position['component']))
        #position2 = positfdion['component']+[position['SorbiteSpacing'][1]]+[position['SorbiteSize'][1]]+[position['size']]
        position2 = [1] + \
        [position['SorbiteSpacing'][1]] + \
        [position['SorbiteSize'][1]]+\
        [position['Fe'][1]] + \
        [position['Sorbite'][1]] + \
        [position['Cementite'][1]] + \
        [position['size']] + \
        position['component']
        position1 = np.matrix(position1)
        position2 = np.matrix(position2)
        return [position1,position2]
    def run(self):
        self.messenger.info_write(1)
        self.param_pre()
        if self.union:
            self.data = dict(
                task_id = self.task_id,
                modelName = "MechPro",
                modelCode = "601"
            )
            self.out = []
            self.data['input_data'] = self.get_union_input_data()
            
            try:
                a = f['x']
                cooltran_id = self.get_cooltran_id()
                print("0")
                rollmicro_id = self.get_rollmicro_id()
                print("1")
                cooltran_data = self.get_cooltran_data(cooltran_id)
                print("2")
                position['size'] = self.get_size(rollmicro_id)
                print("3")
            except:
                self.position = self.fault_data_pre()
                self.out = self.calculate(self.position)
                self.insert_data()
                return
            for i in range(11):
                
                #position = self.data['input_data']
                try:
                    
                    position['SorbiteSpacing'] =[ cooltran_data[i]['spacing_of_sorbite'][0],cooltran_data[i+11]['spacing_of_sorbite'][0]]
                    position['SorbiteSize'] = [cooltran_data[i]['soxhlet_size'],cooltran_data[i+11]['soxhlet_size']]
                    position['Fe'] = [cooltran_data[i]['phase_composition'][0],cooltran_data[i+11]['phase_composition'][0]]
                    position['Sorbite'] = [cooltran_data[i]['phase_composition'][1],cooltran_data[i+11]['phase_composition'][1]]
                    position['Cementite'] = [cooltran_data[i]['phase_composition'][2],cooltran_data[i+11]['phase_composition'][2]]
                except:                    
                    pass
                
                #position['component'] = [cooltran_data
                
                
                position1 = [1] +  \
                [position['SorbiteSpacing'][0]] + \
                [position['SorbiteSize'][0]]+\
                [position['Fe'][0]] + \
                [position['Sorbite'][0]] + \
                [position['Cementite'][0]] + \
                [position['size']] + \
                position['component']
                #print(len(position['component']))
                #position2 = positfdion['component']+[position['SorbiteSpacing'][1]]+[position['SorbiteSize'][1]]+[position['size']]
                position2 = [1] + \
                [position['SorbiteSpacing'][1]] + \
                [position['SorbiteSize'][1]]+\
                [position['Fe'][1]] + \
                [position['Sorbite'][1]] + \
                [position['Cementite'][1]] + \
                [position['size']] + \
                position['component']
                position1 = np.matrix(position1)
                position2 = np.matrix(position2)
                #return [position1,position2]
                #print(position1,position2)
                self.out.append(self.calculate([position1,position2]))
            self.insert_data()
        else:            
            self.position = self.data_pre()
            self.out = self.calculate(self.position)
            self.insert_data()
    def get_cooltran_data(self,cooltran_id):
        mongo = utils.Mongo(simulationInput='SimulationOutputData')
        data = mongo.query_taskid(task_id)
        output_data = data['output_data']
        if len(output_data) != 22:
            raise Exception("the cooltran data len is not equal 22")
    def get_size(self,rollmicro_id):
        try:
            mongo = utils.Mongo(simulationInput='SimulationOutputData')
            data = mongo.query_taskid(task_id)
            output_data = data['output_data']
            return output_data["size"]
        except:
            return 10

    def get_cooltran_id(self):
        try:
            inqure_id = '_'.join(self.task_id.split('_')[:-1])+'_'
            m = utils.Mongo()
            id_list = []
            for u in m.simulationOutput.find({'task_id': re.compile(inqure_id),'modelCode':self.previous_code_1}):
                id_list.append(u['task_id'])
            if len(id_list) == 0:
                #self.exceptProcess.error_run('mongodb_data_get_error')
                raise Exception("previous mongodb was not found")
            def sort_key(item):
                return int(item.split('_')[-1])
            id_list.sort(key=sort_key, reverse=True)
            return id_list[0]
        except:
            return 0
    def get_rollmicro_id(self):
        try:
            inqure_id = '_'.join(self.task_id.split('_')[:-1])+'_'
            m = utils.Mongo()
            id_list = []
            for u in m.simulationOutput.find({'task_id': re.compile(inqure_id),'modelCode':self.previous_code_2}):
                id_list.append(u['task_id'])
            if len(id_list) == 0:
                #self.exceptProcess.error_run('mongodb_data_get_error')
                raise Exception("previous mongodb was not found")
            def sort_key(item):
                return int(item.split('_')[-1])
            id_list.sort(key=sort_key, reverse=True)
            return id_list[0]
        except:
            return 0
    def get_union_input_data(self):
        with open('union_input_data.json') as f:
            load_dict = json.load(f)
        return load_dict



if len(sys.argv) > 1:
    task_id = sys.argv[1]
    messenger = utils.MessageFeedback(task_id,module_code,'MechPro.info')
    exceptProcess.messenger = messenger  
    mongodb = exceptProcess.saferun(utils.Mongo,[],'other')
    A = UnionMechPro(mongodb,messenger,exceptProcess,task_id)
    A.run()
else:
    print('missing task_id')
    #return 0

