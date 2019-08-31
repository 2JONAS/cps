# -*- coding: utf-8 -*-
import pymongo
import math
import os
from gridfs import *
#import matplotlib.pyplot as plt
import bson
import numpy as np
import utils


def gettT(task_id):
    mongo = utils.Mongo(simulationInput='SimulationOutputData')
    data = mongo.query_taskid(task_id)
    fs = data['extraDocInGridFS']
    filename = fs['filename']
    fileId = fs['fileId']
    file_ = mongo.mydb.fs.files.find_one({
        'filename':filename,
        '_id':fileId
            })
    fs = GridFS(mongo.mydb)
    files = fs.find({'_id':fileId})
    #print('总数：', files.count())
    for ffle in files:
      #if ffle.filename.find('.xls') > 0:
        with open(ffle.filename, 'wb') as f1:
          f1.write(ffle.read())
    bson_file = open('TempFieldForStpro', 'rb')
    data = bson.decode_all(bson_file.read())
    data = data[0]
    head = data['SlabHeadFieldForSTPRO']
    body = data['SlabBodyFieldForSTPRO']
    tail = data['SlabTailFieldForSTPRO']
    curves = [head,body,tail]
    extract_curves = []
    
        
    for curve in curves:
        pts_x = curve['pts_x']
        pts_y = curve['pts_y']
        TimeCnt = curve['TimeCnt']
        T = curve['T']
        x_center = pts_x // 2
        y_center = pts_y // 2
        extract = []
        for x in range(x_center,len(T)-1,pts_x):
            extract.append(T[x][y_center:])
        extract = np.array(extract)
        extract_ = []
        for time in range(TimeCnt):
            extract_.append(np.resize(extract[time],11))
        #extract = extract.T
        extract = np.array(extract_).T.tolist()
        t = [i*0.25 for i in range(TimeCnt)]
        extract_curves.append([extract,t])
    
    t = extract_curves[0][1]
    output = []
    for i in extract_curves:
        for j in i[0]:
            output.append(j)
    return t,output
