from datetime import datetime
from SPM_Monitor import Nishant

def create_data_stream(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                yield line.strip()
    except FileNotFoundError:
        print(f"File not found: {file_path}")

file_path = 'F:/logs/logs/logs 3/SVMX_Logs/SPM2/SPM2_2.txt'

nishant = Nishant()
t_c = datetime.strptime('1990-01-01 00:00:00.0000', "%Y-%m-%d %H:%M:%S.%f")
t_p = datetime.strptime('1990-01-01 00:00:00.0000', "%Y-%m-%d %H:%M:%S.%f")
for data_point in create_data_stream(file_path):
    nishant.add_log(data_point)
    data_split = data_point.split("|")
    
    t_p = t_c
    t_c = datetime_object = datetime.strptime(data_split[0], "%Y-%m-%d %H:%M:%S.%f")
    log = data_split[-1]

    if (log.find("OpenContactlessReaderResponse")!=-1 or
        log.find("OpenChipCardReaderResponse")!=-1) and log.find('Success="false"')!=-1:
        nishant.CriticalFaliure_P0(log)
    elif data_split[0]=='coipia':
        nishant.Faliure_P1(log)
    elif log.find("DisableKeypadResponse")!=-1 and log.find('Success="false"')!=-1:
        nishant.Faliure_P2(log)
    elif t_p>=t_c:
        nishant.Faliure_P3(log)
    elif log.find("SPM2 Free Disk Space in Bytes")!=-1 and log.find('Success="false"')!=-1:
        nishant.Faliure_P4(log)
