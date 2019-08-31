# -*- coding: utf-8 -*-


import sys
import utils
from utils import exceptProcess
from FurGrainGrowthAddition import gettT
import os
import json
import re
module_code = '304'
previous_code = '301'
class FurGrainGrowth(object):
    def __init__(self,mongodb,messenger,exceptProcess,FileManagement,task_id):
        self.mongodb = mongodb
        self.messenger = messenger
        self.exceptProcess = exceptProcess
        self.task_id = task_id
        self.model_id = '304'
        self.root_dir = os.getcwd()
        self.progress = 0
    def dafaultcase(self):
        self.data = exceptProcess.saferun(self.mongodb.query_taskid,[self.task_id],'mongodb_data_get_error')
        return self.data['input_data']['DefaultCase']
    def run(self):
        self.DefaultCase = self.dafaultcase()
        if self.DefaultCase == 0:
            self.run_single()
        else:
            self.run_multi()
    def run_single(self):
        positions = self.data["input_data"]
        distribution = ['0', '0.25']
        out_positions = []
        for index in range(1):
            dict_ = {}
            f_module_1_out = utils.grainGrowth(positions['t'][index][1:], positions['T'][index][1:],
                                               positions['Q_param'][index][:])
            f_module_1_out_map = utils.axisMap()
            dict_['size'] = f_module_1_out
            dict_['distribution'] = distribution
            out_positions.append(dict_)
            # messenger.info_write(index/len(positions))
        self.data.pop("input_data")
        self.data["output_data"] = out_positions
        self.exceptProcess.saferun(self.mongodb.out_insert_dict, [self.data], 'insert_error')
        self.messenger.info_write(1)
    def run_multi(self):
        positions = self.data["input_data"]
        distribution = ['0', '0.25']
        d = []
        out_positions = []
        dict_ = {}
        task_id = positions['TempTime_id']
        t, T = gettT(task_id)
        f_module_1_out = []
        f_module_1_out_map = []
        # Q_param = positions[0][0]

        for point in range(len(positions['Q_param'])):
            L = []  # ???¦Â
            for head_index in range(len(positions['Q_param'][point])):
                # f_module_1_out_map.append(utils.axisMap())

                d.append(distribution)
                L.append(utils.grainGrowth(t[1:], T[head_index * 11 + point][1:],
                                           positions['Q_param'][point][head_index][:]))
                if int((head_index * 11 + point / 33) * 100) < 100:
                    messenger.info_write(head_index * 11 + point / 33)
            f_module_1_out.append(L)
        dict_['size'] = f_module_1_out
        dict_['TempTime_id'] = task_id
        dict_['distribution'] = d
        self.data.pop("input_data")
        self.data["output_data"] = dict_
        self.exceptProcess.saferun(self.mongodb.out_insert_dict, [self.data], 'insert_error')
        self.messenger.info_write(1)
class UnionFurGrainGrowth(FurGrainGrowth):
    def __init__(self,*arg, **kwarg):
        super(UnionFurGrainGrowth,self).__init__(*arg, **kwarg)
        self.union = self.union_check()
    def union_check(self):
        return self.task_id[0] == '0'
    def dafaultcase(self):
        if self.union:
            self.data = exceptProcess.saferun(self.mongodb.query_taskid,[self.task_id],'mongodb_data_get_error')
            #
            self.data['input_data'] = self.get_union_input_data()
            TempTime_id = self.getTempTime_id()
            self.data['input_data']['TempTime_id'] = TempTime_id
            return True
        else:
            return super(UnionFurGrainGrowth,self).dafaultcase()
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
    def get_union_input_data(self):
        with open('union_input_data.json') as f:
            load_dict = json.load(f)
        return load_dict
if len(sys.argv) > 1:
    task_id = sys.argv[1]
    messenger = utils.MessageFeedback(task_id,module_code,'FurGrainGrowth.info')
    exceptProcess.messenger = messenger
    mongodb = exceptProcess.saferun(utils.Mongo,[],'other')
    A = UnionFurGrainGrowth(mongodb,messenger,exceptProcess,utils.FileManagement,task_id)
    A.run()
else:
    print('missing task_id')
