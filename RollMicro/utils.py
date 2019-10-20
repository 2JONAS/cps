import pymongo
import math
import os
import time
from gridfs import *
class Mongo(object):
#    def __init__(self,myclient="mongodb://localhost:27017/",mydb="ustb",
#                 simulationInput='simulationInput',simulationOutput='simulationOutput'):
    def __init__(self,myclient="10.0.0.159:27017",mydb="ustb",
                 simulationInput='SimulationInputData',simulationOutput='SimulationOutputData'):
        self.myclient = pymongo.MongoClient(myclient)
        self.mydb = self.myclient[mydb]
        self.simulationInput = self.mydb[simulationInput]
        self.simulationOutput = self.mydb[simulationOutput]
    def query_taskid(self,task_id):
        myquery = {'task_id':task_id}
        mydoc = self.simulationInput.find(myquery)
        for x in mydoc:
            pass        
        return x
    def image_save(self,image_path):
        imgput = GridFS(self.mydb)
        datatmp = open(image_path, 'rb')
        image_path = image_path.split('/')[-1]
        f = image_path.split('.')
        insertimg=imgput.put(datatmp,content_type=f[-1],filename=image_path)
        
        datatmp.close()
        w = imgput.get(insertimg)
        dict_ = {}
        dict_['fileId'] = str(w._id)
        dict_['filename'] = w.filename
        dict_['length'] = w.length
        #dict_['bucketName'] = 'fs'
        dict_['otherInfo'] = None
        return dict_
    def out_insert_dict(self,dict_):
        self.simulationOutput.insert_one(dict_)
    def input_insert_dict(self,dict_):
        self.simulationInput.insert_one(dict_) 
        
class MessageFeedback():
    def __init__(self,TaskId,ModelId,file='test.info'):
        self.file = os.path.join(os.getcwd(),file)
        self.TaskId = str(TaskId)
        self.ModelId = str(ModelId)
        self.info_write(0)

    def info_write(self,SimulationProgress,ErrorNumber=0):
        f = open(self.file,'w+')
        line = [str(self.TaskId),str(self.ModelId),str(int(SimulationProgress*100)),str(ErrorNumber)]
        f.write(','.join(line))
        f.close()


    def del_line(self):
        f = open(self.file,'w+')
        line = ''
        f.write(line)
        f.close()
        
class FileManagement(object):
    def __init__(self,root_dir,module_dir='model',module_run_dir='run'):
        self.module_dir = os.path.join(root_dir,module_dir)        
        self.module_run_dir = os.path.join(root_dir,module_run_dir)
        self.root_dir = root_dir
        
        self.check_dir(root_dir)
        self.check_dir(module_dir)
        self.check_dir(module_run_dir)
    def check_dir(self,file_dir):
        if file_dir is not None:
            if not os.path.exists(file_dir):
                os.mkdir(file_dir)
                
    def creat_run_dir(self,dirname):
         os.mkdir(os.path.join(self.module_run_dir,dirname))
    
class exceptProcess(object):
    '''处理异常并将异常写入info文件，关闭程序
        只需要初始化一次，指定messenger对象
    '''
    messenger = None
    init_flag = 0
    error_dict = {'mongodb_data_get_error':'1',
              'data_type_error':'2',
              'curve_data_error':'3',
              'cooltrans_data_error':'4',
              'dead_wait_error':'5',
              'micress_open_error':'6',
              'thermo_calc_open_error':'7',
              'insert_error':'8',
              'default_case_error':'9',
              'other':'66',
              }
    def error_run(error_name):
        exceptProcess.messenger.info_write(0,exceptProcess.error_dict[error_name])
        time.sleep(5)
        exceptProcess.messenger.del_line()
        exit(error_name)
    def saferun(f,input_value,error_name):
        '''input_value必须是个list,如果就是一个单值用[]括起来
        f是函数名'''
        try:
            for i in range(len(input_value)):
                input_value[i].pop("_id")
        except:
            pass
        string = input_value.__str__()
        string = "f(" + string[1:-1] + ")"
        #print("string",string)
        try:
            #f()
            return eval(string)
        except Exception as e:
            
            exceptProcess.error_run(error_name)      
        
        
        
        
def grainGrowth(t,T,Q_param=[0.82,0.52,0.2]):
    if len(t) != len(T):
        exceptProcess.error_run('curve_data_error')
    k1 = 76500
    k2 = 0.2
    for index,i in enumerate(Q_param):
        Q_param[index] = float(i)
    #Q = 92000
    if len(Q_param) == 3:
        Q = 88820 + 3000 * Q_param[0] + 1000 * Q_param[1] + 1000 * Q_param[2]
    else:
        Q = 88820 + 3000 * Q_param[0] + 1000 * Q_param[1] + 1000 * Q_param[2] + 1000 * Q_param[3]
    R = 8.314
    d = []
    for i in range(len(t)):
        t[i] = float(t[i]) * 60
        T[i] = float(T[i]) + 273.15
    d.append(k1*math.exp(-Q/(R*T[0])*math.pow(t[0],k2))) 
    for i in range(1,len(t)):
        tstar = math.pow(d[i-1]/(k1*math.exp(-Q/(R*T[i]))),1/k2)
        d.append(k1*math.exp(-Q/(R*T[i]))*math.pow(tstar+t[i]-t[i-1],k2))
    return d[-1]
def axisMap(x_min=0,x_max=3.5,interval=0.0001):
    def calculation_y(x):
        if x == 0:
            return 0
        y1 = ((1/(2*math.pi))**0.5)/(0.5*x)
        y2 = 2*((math.log(x)**2))
        y=y1*math.exp(-y2)
        return y
    x = []
    y = []
    length = int((x_max-x_min)/interval)
    for i in range(length):
        x.append(x_min + i*interval)
        y.append(calculation_y(x[-1]))
    return (x,y)