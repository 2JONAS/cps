# -*- coding: utf-8 -*-

import os
import time
import utils
from utils import exceptProcess
import sys
import numpy as np

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
        # a,k1,k2,k3,k4,k5,k6,k7,j1,j2,j3
        # 成一个列向量
        #param1是搭接
        self.param1 = np.matrix([1000,1,1,1,1,1,1,1,1,1,1,]).T
        self.param2 = np.matrix([1000,1,1,1,1,1,1,1,1,1,1,]).T
        pass
    def calculate(self,position):
        out1 = position[0]*self.param1
        out2 = position[1]*self.param2
        out = [out1[0,0],out2[0,0]]
        return out
    def data_pre(self):
        self.data = exceptProcess.saferun(self.mongodb.query_taskid,[self.task_id],'mongodb_data_get_error')
        position = self.data['input_data']
        position1 = position['component']+[position['SorbiteSpacing'][0]]+[position['SorbiteSize'][0]]+[position['size']]
        position2 = position['component']+[position['SorbiteSpacing'][1]]+[position['SorbiteSize'][1]]+[position['size']]
        position1 = np.matrix(position1)
        position2 = np.matrix(position2)
        return [position1,position2]
    def insert_data(self):
        self.data.pop("input_data")
        self.data["output_data"] = self.out    
        exceptProcess.saferun(self.mongodb.out_insert_dict,[self.data],'insert_error')
        self.progress = 1
        self.messenger.info_write(self.progress)




if len(sys.argv) > 1:
    task_id = sys.argv[1]
    messenger = utils.MessageFeedback(task_id,module_code,'MechPro.info')
    exceptProcess.messenger = messenger  
    mongodb = exceptProcess.saferun(utils.Mongo,[],'other')
    A = MechPro(mongodb,messenger,exceptProcess,task_id)
    A.run()
else:
    print('missing task_id')
    #return 0

