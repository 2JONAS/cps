import os
import time
import utils
from utils import exceptProcess
import sys
import numpy as np
import psutil
import RollMicroAddition as rmadd
import matplotlib.pyplot as plt
import json
import re
module_code = '403'
class ROOLMICRO(object):
    def __init__(self,mongodb,messenger,exceptProcess,FileManagement,task_id):
        self.mongodb = mongodb
        self.messenger = messenger
        self.exceptProcess = exceptProcess
        self.task_id = task_id
        self.model_id = '403'
        self.root_dir = os.getcwd()
        self.file_group = FileManagement(os.path.join(self.root_dir,'module_2'))
        self.time_now = str(time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(time.time())))
        self.progress = 0
        self.daoci = 9
    def dafaultcase(self):
        self.data = exceptProcess.saferun(self.mongodb.query_taskid,[self.task_id],'mongodb_data_get_error')
        return self.data['input_data']['DefaultCase']
    def run(self):
        self.DefaultCase = self.dafaultcase()
        if self.DefaultCase == 0:
            self.daoci = 26
            self.run_default()
        else:
            
            self.run_case()
        #self.run_default()
    def run_default(self):
        korn_files = ['J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results01\\Results01_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results02\\Results02_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results03\\Results03_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results04\\Results04_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results05\\Results05_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results06\\Results06_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results07\\Results07_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results08\\Results08_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results09\\Results09_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results10\\Results10_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results11\\Results11_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results12\\Results12_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results13\\Results13_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results14\\Results14_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results15\\Results15_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results16\\Results16_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results17\\Results17_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results18\\Results18_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results19\\Results19_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results20\\Results20_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results21\\Results21_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results22\\Results22_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results23\\Results23_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results24\\Results24_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results25\\Results25_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results26\\Results26_korn.mcr']
        self.get_out(korn_files)
        # insert data
        self.insert_data()
    def run_case(self):
        # self.progress = 0.1
        # self.messenger.info_write(self.progress)
        # input_data = self.case_data_pre()
        # out_file_dir = os.path.join(self.file_group.module_run_dir,self.time_now)
        # self.file_group.creat_run_dir(self.time_now)    
        # run micress
        # korn_files = self.run_micress(input_data,out_file_dir)
        # get out
        korn_files = ['J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results01\\Results01_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results02\\Results02_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results03\\Results03_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results04\\Results04_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results05\\Results05_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results06\\Results06_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results07\\Results07_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results08\\Results08_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results09\\Results09_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results10\\Results10_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results11\\Results11_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results12\\Results12_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results13\\Results13_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results14\\Results14_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results15\\Results15_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results16\\Results16_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results17\\Results17_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results18\\Results18_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results19\\Results19_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results20\\Results20_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results21\\Results21_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results22\\Results22_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results23\\Results23_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results24\\Results24_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results25\\Results25_korn.mcr', 'J:\\wangxin\\master\\RollMicro\\module_2\\run\\2019-09-04-16-30-17\\Results26\\Results26_korn.mcr']
        self.get_out(korn_files)
        # insert data
        self.insert_data()
    def get_out(self,korn_files):
        self.out = {}
        # get size
        # 建立实例，以最后一个result的路径
        k = rmadd.KORN(korn_files[-1],len(korn_files))
        print(korn_files[-1])
        # 抓取最后一个korn文件的最后一个vtk文件
        k.vtk_extract()
        # 将vtk文件转为numpy矩阵形式
        k.vtk2np()
        # 读取矩阵的尺寸数据
        self.out['size'] = k.np_count(k.img)
        # 获得图形数据
        images = []
        for index,korn_file in enumerate(korn_files):
            
            k = rmadd.KORN(korn_file,index+1)
            k.vtk_extract()
            k.vtk2np()
            images.append(k.img)
        I = []
        images_len = len(images) - 2
        images_gap = int(images_len / 6)
        I.append(images[0])
        index = 0
        for i in range(6):
            I.append(images[index])
            index = index + images_gap
        I.append(images[-1])
        images = I
        cwd = os.getcwd()
        image_files = []
        for index,image in enumerate(images):
            index = index + 1
            image_name = os.path.join(cwd,str(index)+'.png')
            plt.imsave(image_name,image)
            image_files.append(self.mongodb.image_save(image_name))
            
        self.out['images'] = image_files
        
    
    def default_data_pre(self):
        input_data =  self.data["input_data"]
        ## 暂时设计读取npy的数据
        input_data = []
        x = np.load('input_data.npy')
        for i in range(x.shape[-1]):
        #for i in range(1):
            input_data.append(x[:,i].tolist())
        return input_data
    def case_data_pre(self):
        input_data = self.data["input_data"]
        self.TaskGrainSize = input_data['TaskGrainSize'] 
        self.TempTimeId = input_data['TaskTempTime']
        self.YingLiId = input_data['TaskYingLi']
        self.Nine = False
        Temp,Time = self.get_TempTime()
        YingLi,YingBian = self.get_YingLi()
        
        input_data = []
        for index in range(min(len(Temp),len(YingLi))):
            input_data.append([Temp[index],YingLi[index],YingBian[index],Time[index]])
        if len(input_data) == 9:
            self.daoci = 9
        else:
            self.daoci = 26
        print('daoci',self.daoci)
        return input_data
    def get_TempTime(self):
        TempMongo = utils.Mongo(simulationInput='SimulationOutputData')
        temp_data = exceptProcess.saferun(TempMongo.query_taskid,[self.TempTimeId],'mongodb_data_get_error')
        temp_data = temp_data['temp_data']
        #print(temp_data)
        for key in temp_data:
            print(key)
        if 'ROLLTIME' in temp_data:
            self.Nine = False
        else:
            self.Nine = True
        Temp = []
        Time = []
        if self.Nine:
            for i in range(9):
                # 只取sapce time 的最后值
                Time.append(temp_data['SPACE_TIME'][9+i*10])
                for j in range(10):
                    sum = 0
                    sum = sum + temp_data['ROLL_TEMP'][i*10+j][0]
                 
                Temp.append(sum/10)

        else:
            for i in range(2):
                # 只取sapce time 的最后值
                Time.append(temp_data['SPACE_TIME'][9+i*10])
                for j in range(10):
                    sum = 0
                    sum = sum + temp_data['ROLL_TEMP'][i*10+j][0]
                 
                Temp.append(sum/10)
            for i in range(14):
                # 只取sapce time 的最后值
                Time.append(temp_data['SPACETIME'][9+i*10])
                for j in range(10):
                    sum = 0
                    sum = sum + temp_data['ROLLTEMP'][i*10+j][0]
                 
                Temp.append(sum/10)
            for i in range(10):
                # 只取sapce time 的最后值
                Time.append(temp_data['SPACETIME'][143+i*4])
                for j in range(2):
                    sum = 0
                    sum = sum + temp_data['ROLLTEMP'][140+i*4+2+j][0]
                 
                Temp.append(sum/10)
        last = 0
        for index,t in enumerate(Time):
            Time[index] = max(t - last,0)
            last = t
        return Temp,Time


    def get_YingLi(self):
        TempMongo = utils.Mongo(simulationInput='SimulationOutputData')
        temp_data = exceptProcess.saferun(TempMongo.query_taskid,[self.YingLiId],'mongodb_data_get_error')
        temp_data = temp_data['FORCESTRESSSTRAIN']
        YingLi = []
        YingBian = []
        for daoci in range(len(temp_data['NodeStrainY'])):
            sum_li = 0
            sum_bian = 0
            for time_point in range(52):
                sum_bian = sum_li + temp_data['NodeStrainY'][daoci][0][time_point]
                sum_li = sum_bian + temp_data['NodeStressY'][daoci][0][time_point]
            YingLi.append(sum_li/52)
            YingBian.append(sum_bian/52)
        return YingLi,YingBian
    def insert_data(self):
        self.data.pop("input_data")
        self.data["output_data"] = self.out    
        exceptProcess.saferun(self.mongodb.out_insert_dict,[self.data],'insert_error')
        self.progress = 1
        self.messenger.info_write(self.progress)
    def run_micress(self,input_data,out_file_dir):
        if self.daoci == 9:
            model_file =  [os.path.join(self.file_group.module_dir,'09_{0:02d}.txt'.format(i)) for i in range(1,10)]
        else:
            model_file =  [os.path.join(self.file_group.module_dir,'{0:02d}.txt'.format(i)) for i in range(1,27)]
        korn_files = []
        for index,txt_in in enumerate(input_data): 
            index = index + 1 
            input_dict = {'TEMP':txt_in[0],'STRESS':txt_in[1],'STRAIN':txt_in[2],'TIME':txt_in[3]}
            #if self.daoci == 9:
                
            print("index",index)
            out_file = os.path.join(out_file_dir,'run{0:02d}.mec'.format(index))
            rmadd.change_data_in_cm(model_file[index-1],out_file,input_dict)
            os.chdir(out_file_dir)
            os.system("start /wait cmd /c "+ 'run{0:02d}.mec'.format(index))
            #os.system('run{0:02d}.mec'.format(index))
            #print(out_file)
            #os.system('run{0:02d}.mec'.format(index))
            self.progress = self.progress + 1/len(input_data)*0.7
            if self.progress < 1:
                self.messenger.info_write(self.progress)
        
        
            result_dir =  os.path.join(out_file_dir,'Results{0:02d}'.format(index))
            korn_file = os.path.join(result_dir,'Results{0:02d}_korn.mcr'.format(index))
            korn_files.append(korn_file)
        os.chdir(self.file_group.root_dir)
        return korn_files
    def read_mirecress_korn(self,korn_file):
        
        korn_file_ = korn_file.split('\\')
        korn_file_[-1] = 'vtkfile'
        vtk_file = '\\'.join(korn_file_)
        rmadd.mcr(korn_file,vtk_file)
        root_dir = '\\'.join(korn_file_[:-1])
        file_list = os.listdir(root_dir)
        vtk_files = []
        for file in file_list:
            if file.split('.')[-1] == 'vtk':
                vtk_file = os.path.join(root_dir,file)
                vtk_files.append(vtk_file)
        return int(rmadd.vtk(vtk_files[-1])),root_dir

#        return np.random.randint(7,13)
    def get_images(self,korn_files,temp_file_path):
        
        images = rmadd.mcr_images(korn_files,temp_file_path)
        images_len = len(images)
        images_len = images_len - 2
        images_gap = int(images_len/6)
        slice_image = []
        slice_image.append(images[0])
        index = 0
        for i in range(6):
            index = index + images_gap
            slice_image.append(images[index])
        slice_image.append(images[-1])
        return slice_image
        
    


class UnionROOLMICRO(ROOLMICRO):
    def __init__(self,*arg, **kwarg):
        super(UnionROOLMICRO,self).__init__(*arg, **kwarg)
        self.union = self.union_check()
        self.previous_code_1 = '401'
        self.previous_code_2 = '402'
    def union_check(self):
        return self.task_id[0] == '0'
    def dafaultcase(self):
        if self.union:
            self.data = exceptProcess.saferun(self.mongodb.query_taskid,[self.task_id],'mongodb_data_get_error')
            self.data['input_data'] = self.get_union_input_data()
            TaskTempTime_id = self.getTaskTempTime_id()
            TaskYingLi_id = self.getTaskYingLi_id()
            self.data['input_data']['TaskTempTime'] = TaskTempTime_id
            self.data['input_data']['TaskYingLi_id'] = TaskYingLi_id
            return True
        else:
            return 0
            return super(UnionROOLMICRO,self).dafaultcase()
    def getTaskYingLi_id(self):
        inqure_id = '_'.join(self.task_id.split('_')[:-1])+'_'
        m = utils.Mongo()
        id_list = []
        for u in m.simulationOutput.find({'task_id': re.compile(inqure_id),'modelCode':self.previous_code_2}):
            id_list.append(u['task_id'])
        if len(id_list) == 0:
            self.exceptProcess.error_run('mongodb_data_get_error')
            raise Exception("previous mongodb was not found")
        def sort_key(item):
            return int(item.split('_')[-1])
        id_list.sort(key=sort_key, reverse=True)
        #print(id_list[0])
        return id_list[0]
    def getTaskTempTime_id(self):

        inqure_id = '_'.join(self.task_id.split('_')[:-1])+'_'
        #print('inqure_id',inqure_id)
        m = utils.Mongo()
        id_list = []
        for u in m.simulationOutput.find({'task_id': re.compile(inqure_id),'modelCode':self.previous_code_1}):
            id_list.append(u['task_id'])
        if len(id_list) == 0:
            self.exceptProcess.error_run('mongodb_data_get_error')
            raise Exception("previous mongodb was not found")
        def sort_key(item):
            return int(item.split('_')[-1])
        id_list.sort(key=sort_key, reverse=True)
        #print(id_list[0])
        return id_list[0]
    def get_union_input_data(self):
        with open('union_input_data.json') as f:
            load_dict = json.load(f)
        return load_dict








if len(sys.argv) > 1:
    task_id = sys.argv[1]
    messenger = utils.MessageFeedback(task_id,module_code,'RollMicro.info')
    exceptProcess.messenger = messenger  
    mongodb = exceptProcess.saferun(utils.Mongo,[],'other')
    A = UnionROOLMICRO(mongodb,messenger,exceptProcess,utils.FileManagement,task_id)
    A.run()
    
    
else:
    print('missing task_id')
    #return 0




