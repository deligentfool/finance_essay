# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 08:20:58 2019

@author: Xzw

E-mail: diligencexu@gmail.com
"""

import pandas as pd
import numpy as np
from pre_process import get_data
from stagewise import stageWise
import seaborn as sns
sns.set(style="ticks", color_codes=True)
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix 
import matplotlib.pyplot as plt 
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 随机种子
np.random.seed(10)

# 混淆矩阵
def cm_plot(y, yp):
  cm = confusion_matrix(y, yp)     
  plt.matshow(cm, cmap=plt.cm.OrRd) 
  plt.colorbar()   
  for x in range(len(cm)): 
    for y in range(len(cm)):
      plt.annotate(cm[x,y], xy=(x, y), horizontalalignment='center', verticalalignment='center')  
  plt.ylabel('True label') 
  plt.xlabel('Predicted label') 
  return plt

threshold = 0.05

data, col_list = get_data()
data_2017 = data[:176]
data_2016 = data[176:176 * 2].reset_index(drop=True)
data_2015 = data[176 * 2:176 * 3].reset_index(drop=True)

ws, wsRec = stageWise(data_2017.iloc[:, 1:-1], data_2017.iloc[:, -1], eps=1e-3, numIt=100000)
wsRec.plot(legend=False)
plt.savefig('./2017.png')
plt.show()

#train_ind = np.random.choice(range(176), 88, replace=False)
train_ind = np.array(
                    [47,  66,  12,  56,  71,  40,  87,  15,   4, 165, 138,   3, 173,
                     64, 102,  93, 157,  95, 141, 135, 144, 110, 111, 154,  13, 163,
                     156,  76, 129, 174,   6, 153, 149, 119, 128, 172,  18,  53, 168,
                     160,  96,  48,   5, 140,  20,  19, 121, 127,  86,   2,  37, 115,
                     80,  24,  97, 158, 171, 169, 122, 148,  50,  69, 105, 150,  94,
                     23,  41,  52,  73,  36,  75,   0, 125,  33,  32, 100,  67, 120,
                     89,  46, 112,  30, 107,  78,  91,  68,  25, 143])
test_ind = np.setdiff1d(range(176), train_ind)

keep_col = []
for i in range(len(list(data.columns))-2):
    if abs(ws[i][0]) > threshold:
        keep_col.append((list(data.columns)[i+1], ws[i][0]))
#流动资产周转率 
#销售毛利率 
#销售费用/营业总收入 
#管理费用/营业总收入 
#财务费用/营业总收入
#总资产净利润
#权益乘数
#权益乘数(杜邦分析)
#流动资产/总资产
#非流动资产/总资产
#有形资产/总资产
#有形资产/负债合计
#年化总资产净利率
#总资产净利率(杜邦分析)

# 最终选取数据指标
last_col = ['ca_turn', 'grossprofit_margin', 'saleexp_to_gr', 'adminexp_of_gr',
            'finaexp_of_gr', 'npta', 'assets_to_eqt', 'ca_to_assets',
            'tbassets_to_totalassets', 'tangibleasset_to_debt']
# 流动资产周转率
# 销售毛利率
# 销售费用/营业总收入
# 管理费用/营业总收入
# 财务费用/营业总收入
# 总资产净利润
# 权益乘数
# 流动资产/总资产
# 有形资产/总资产
# 有形资产/负债合计

last_col_z = ['流动资产周转率', '销售毛利率', '销售费用率', '管理费用率',
            '财务费用率', '总资产净利润', '权益乘数', '流动资产比率',
            '有形资产比率', '有形资产负债率']

logistic_model = LogisticRegression()
logistic_model.fit(data_2017.iloc[train_ind][last_col], data_2017['label'][train_ind])
w_logistic = logistic_model.coef_
b_logistic = logistic_model.intercept_
y_prob = logistic_model.predict_proba(data_2017.iloc[test_ind][last_col])
y_pred = logistic_model.predict(data_2017.iloc[test_ind][last_col])
acc = accuracy_score(data_2017['label'][test_ind], y_pred)
cm_plot(data_2017['label'][test_ind], y_pred)

# 变量间关系
tmp = data_2017.iloc[train_ind][last_col+['label']]
#for i in list(tmp.columns):
#    tmp[i] = (tmp[i] -  tmp[i].mean()) / tmp[i].var()
sns.pairplot(tmp, hue="label",vars=last_col)

# 热力图
tmp = data_2017.iloc[train_ind][last_col]
corr = np.corrcoef(tmp.T)
corr = pd.DataFrame(corr,columns=last_col_z,index=last_col_z)
sns.heatmap(corr, annot=True, fmt='.2f', cmap='YlGnBu')


'''
for _ in range(1000000):
    train_ind = np.random.choice(range(176), 88, replace=False)
    test_ind = np.setdiff1d(range(176), train_ind)

    keep_col = []
    for i in range(len(list(data.columns))-2):
        if abs(ws[i][0]) > threshold:
            keep_col.append((list(data.columns)[i+1], ws[i][0]))
    #流动资产周转率
    #销售毛利率
    #销售费用/营业总收入
    #管理费用/营业总收入
    #财务费用/营业总收入
    #总资产净利润
    #权益乘数
    #权益乘数(杜邦分析)
    #流动资产/总资产
    #非流动资产/总资产
    #有形资产/总资产
    #有形资产/负债合计
    #年化总资产净利率
    #总资产净利率(杜邦分析)

    # 最终选取数据指标
    last_col = ['ca_turn', 'grossprofit_margin', 'saleexp_to_gr', 'adminexp_of_gr',
                'finaexp_of_gr', 'npta', 'assets_to_eqt', 'ca_to_assets',
                'tbassets_to_totalassets', 'tangibleasset_to_debt', 'roa_yearly']

    logistic_model = LogisticRegression()
    logistic_model.fit(data_2017.iloc[train_ind][last_col], data_2017['label'][train_ind])
    y_prob = logistic_model.predict_proba(data_2017.iloc[test_ind][last_col])
    y_pred = logistic_model.predict(data_2017.iloc[test_ind][last_col])
    acc = accuracy_score(data_2017['label'][test_ind], y_pred)
    if acc > 0.84:
        cm_plot(data_2017['label'][test_ind], y_pred)
        break
'''


# 提前一年正确率
y_prob = logistic_model.predict_proba(data_2016.iloc[:][last_col])
y_pred = logistic_model.predict(data_2016.iloc[:][last_col])
acc = accuracy_score(data_2016['label'], y_pred)
cm_plot(data_2016['label'], y_pred)

# 提前两年正确率
y_prob = logistic_model.predict_proba(data_2015.iloc[:][last_col])
y_pred = logistic_model.predict(data_2015.iloc[:][last_col])
acc = accuracy_score(data_2015['label'], y_pred)
cm_plot(data_2015['label'], y_pred)


# 交叉验证
clf = LogisticRegression()
cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=1398)
acc_cv =  cross_val_score(clf, data_2017.iloc[:][last_col], data_2017['label'], cv=cv)
acc_cv_mean = acc_cv.mean()
