import os
import pandas as pd
from constant import  const
import numpy as np
import  data_process as dp
import time,datetime
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import numpy
import time
import matplotlib.pyplot as plt
import shoot as sh


color=['red','blue','white','black','green']

def kmeans_data(file_name):
    data_array = []

    data_reject = sh.order_process(file_name,'Business Reject Event')
    data_insert =  sh.order_process(file_name,'Order Insert Event')
    data_reject = data_reject[['invAcctId','securityId']]
    data_insert = data_insert[['invAcctId','securityId']]
    datas = pd.concat([data_insert,data_reject])
    datas = datas.reset_index(drop=True)
    invAcctIds = datas['invAcctId'].unique()
    securityIds = datas['securityId'].unique()

    for i in invAcctIds:
        data_invAcctId = datas[datas['invAcctId']==i]
        da = data_invAcctId.groupby('securityId').count().reset_index()
        securityId = list(da['securityId'])
        value = list(da['invAcctId'])
        dicts = dict(zip(securityId,value))
        data = pd.DataFrame([dicts])
        data['invAcctId'] = i
        data_array.append(data)

    data_ = pd.concat(data_array, axis=0)
    data_ = data_.set_index(["invAcctId"])
    data_ = data_.fillna(0)

    return data_

def drawing(data,k):
    for i in range(k):
        datas = data[data['labels']==i]


def kmeans(data):
    data['labels']=0
    distance = pd.DataFrame(index=range(1, 10), columns=['类内距离', '类间距离'])
    for k in range(1, 10):
        kmodel = KMeans(n_clusters=k)
        kmodel.fit(data)

        r1 = pd.Series(kmodel.labels_).value_counts()  # 统计各个类别的数目
        data['labels'] = kmodel.labels_

        r2 = pd.DataFrame(kmodel.cluster_centers_)  # 找出聚类中心
        centers = kmodel.cluster_centers_

        r = pd.concat([r2, r1], axis=1)  # 横向连接（0是纵向），得到聚类中心对应的类别下的数目
        r.columns = list(data.columns) + [u'类别数目']  # 重命名表头
        # colr = ['#E15759', '#4E79A7', '#76B7B2', '#F28E2B', 'blue', '#F45E2B', '#F67E2B']
        plt.figure(figsize=(10, 8))
        distance_in = 0
        distance_ot = 0
        for i in range(k):
            group = kmodel.labels_ == i
            members = data[group]

            for v in np.mat(members):
                distance_in += np.linalg.norm(v - kmodel.cluster_centers_[i])  # 默认为二范数,即欧式距离
            for j in range(k):
                if i < j:
                    distance_ot += np.linalg.norm(kmodel.cluster_centers_[i] - kmodel.cluster_centers_[j])
        distance.loc[k, '类内距离'] = distance_in
        distance.loc[k, '类间距离'] = distance_ot

        # plt.scatter(x=data.iloc[:0], y=data.index, c=data['labels'], s=50, cmap='rainbow')
        plt.scatter(centers[:, 0], centers[:, 1], c='k', marker='*', s=180)
        plt.show()

        print(data['labels'])
        print('完成聚类数为 {} 聚类！'.format(k))

    print(distance,data)


if __name__ == "__main__":
    # 函数调用方式
    # data_to_csv(const.FILE, const.CSV_PATH ) '''完成文件数据的特殊转换，具体生成方式见函数注释'''
    # shoot_analysis(10,const.TIME_LIMIT)      '''打版客户的分析，参数10：订单量或废单量大于10笔'''
    # long_analysis('ordTime',const.START_TIME,const.END_TIME,const.RATE) '''ordTime：订单时间作用字段；RATE：特定时间内订单占比 '''
    # data = kmeans_data(const.CSV_PATH)
    kmeans(data)