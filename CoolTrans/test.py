

 
import psutil
pids = psutil.pids()
for pid in pids:
    try:
        p = psutil.Process(pid)
        if 'javaw.exe' in p.name():
            print("pid-%d,pname-%s" %(pid,p.name()))
    except:
        print(0)