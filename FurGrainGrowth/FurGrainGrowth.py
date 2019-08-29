# -*- coding: utf-8 -*-


import sys
import utils
from utils import exceptProcess
from FurGrainGrowthAddition import gettT

module_code = '304'



if len(sys.argv) > 1:
    task_id = sys.argv[1]
    messenger = utils.MessageFeedback(task_id,module_code)
    exceptProcess.messenger = messenger  
    mongodb = exceptProcess.saferun(utils.Mongo,[],'other')
    data = exceptProcess.saferun(mongodb.query_taskid,[task_id],'mongodb_data_get_error')
    #data = mongodb.query_taskid(task_id)
    
    
    positions = data["input_data"]

    if positions['DefaultCase'] == 0:
        distribution = ['0','0.25']
        out_positions = []
        for index in range(1):
            dict_ = {}                
            f_module_1_out = utils.grainGrowth(positions['t'][index][1:],positions['T'][index][1:],positions['Q_param'][index][:])
            f_module_1_out_map = utils.axisMap()
            dict_['size'] = f_module_1_out
            dict_['distribution'] = distribution
            out_positions.append(dict_)
            #messenger.info_write(index/len(positions))
        data.pop("input_data")
        data["output_data"] = out_positions
        exceptProcess.saferun(mongodb.out_insert_dict,[data],'insert_error')
        messenger.info_write(1)
        #messenger.del_line()
    elif positions['DefaultCase'] == 1:
        distribution = ['0','0.25']
        d = []
        out_positions = []
        dict_ = {}
        task_id = positions['TempTime_id']
        print(task_id)
        t,T = gettT(task_id)
        f_module_1_out = []
        f_module_1_out_map= []
        #Q_param = positions[0][0]
        
        for point in range(len(positions['Q_param'])):
            L = [] # Í·ÖÐÎ²
            for head_index in range(len(positions['Q_param'][point])):
                #f_module_1_out_map.append(utils.axisMap())

                d.append(distribution)
                L.append(utils.grainGrowth(t[1:],T[head_index*11+point][1:],positions['Q_param'][point][head_index][:]))
                if int((head_index*11+point/33)*100) < 100:
                    messenger.info_write(head_index*11+point/33)
            f_module_1_out.append(L)
        dict_['size'] = f_module_1_out
        dict_['TempTime_id'] = task_id
        dict_['distribution'] = d
        data.pop("input_data")
        data["output_data"] = dict_
        exceptProcess.saferun(mongodb.out_insert_dict,[data],'insert_error')
        messenger.info_write(1)
    else:
        exceptProcess.error_run('default_case_error')
else:
    print('missing task_id')
    #return 0