import os
import pandas as pd
from constant import  const
import  data_process as dp
import time,datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def order_process(to_file,data_name):
    to_files = to_file + data_name + '.csv'
    index = const.DATA_PART.index(data_name)
    data = pd.DataFrame(pd.read_csv(to_files, engine='python', error_bad_lines=False,
                                    names=const.MATCH_HEADER[index]))
    data.drop_duplicates(keep='first', inplace=True)
    print(data)

    return data

def get_field(data,field):
    lists = list(data[field].unique())
    print(lists)
    return  lists

def security_similarity():
    security_list = get_field(data,'securityId')




if __name__ == "__main__":
    # 函数调用方式
    # data_to_csv(const.FILE, const.CSV_PATH )
    data = order_process(const.CSV_PATH,'Order Insert Event')
    get_field(data,'securityId')
    # long_analysis('ordTime',const.START_TIME,const.END_TIME,const.RATE)

