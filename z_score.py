# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 20:25:44 2019

@author: Xzw

E-mail: diligencexu@gmail.com
"""

import pandas as pd
import numpy as np
import seaborn as sns
sns.set(style="ticks", color_codes=True)
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix 
import matplotlib.pyplot as plt 

# 混淆矩阵
def cm_plot(y, yp):
  cm = confusion_matrix(y, yp)     
  plt.matshow(cm, cmap=plt.cm.YlGn) 
  plt.colorbar()   
  for x in range(len(cm)): 
    for y in range(len(cm)):
      plt.annotate(cm[x,y], xy=(x, y), horizontalalignment='center', verticalalignment='center')  
  plt.ylabel('True label') 
  plt.xlabel('Predicted label') 
  return plt


fina_data_2015 = pd.read_csv('./2015_data.csv')
fina_data_2016 = pd.read_csv('./2016_data.csv')
fina_data_2017 = pd.read_csv('./2017_data.csv')
fina_data_2018 = pd.read_csv('./2018_data.csv')
fina_list = [fina_data_2015, fina_data_2016, fina_data_2017, ]  # fina_data_2018]

# 利润表数据
income_data_2015 = pd.read_csv('./2015_income_data.csv')
income_data_2016 = pd.read_csv('./2016_income_data.csv')
income_data_2017 = pd.read_csv('./2017_income_data.csv')
income_data_2018 = pd.read_csv('./2018_income_data.csv')
income_list = [income_data_2015, income_data_2016, income_data_2017, ]  # income_data_2018]

# 现金流量表数据
cashflow_data_2015 = pd.read_csv('./2015_cashflow_data.csv')
cashflow_data_2016 = pd.read_csv('./2016_cashflow_data.csv')
cashflow_data_2017 = pd.read_csv('./2017_cashflow_data.csv')
cashflow_data_2018 = pd.read_csv('./2018_cashflow_data.csv')
cashflow_list = [cashflow_data_2015, cashflow_data_2016, cashflow_data_2017, ]  # cashflow_data_2018]

# 资产负债表数据
balancesheet_data_2015 = pd.read_csv('./2015_balancesheet_data.csv')
balancesheet_data_2016 = pd.read_csv('./2016_balancesheet_data.csv')
balancesheet_data_2017 = pd.read_csv('./2017_balancesheet_data.csv')
balancesheet_data_2018 = pd.read_csv('./2018_balancesheet_data.csv')
balancesheet_list = [balancesheet_data_2015, balancesheet_data_2016,
                     balancesheet_data_2017, ]  # balancesheet_data_2018]


# 去掉重复记录
for i in fina_list:
    i.drop_duplicates(['ts_code'], keep='last', inplace=True)
    
for i in income_list:
    i.drop_duplicates(['ts_code'], keep='last', inplace=True)
    
for i in cashflow_list:
    i.drop_duplicates(['ts_code'], keep='last', inplace=True)
    
for i in balancesheet_list:
    i.drop_duplicates(['ts_code'], keep='last', inplace=True)
    

# 合并同类数据
fina_data = pd.concat(fina_list, ignore_index=True)
income_data = pd.concat(income_list, ignore_index=True)
cashflow_data = pd.concat(cashflow_list, ignore_index=True)
balancesheet_data = pd.concat(balancesheet_list, ignore_index=True)


# 删除无关数列
balancesheet_data.drop(['ann_date', 'f_ann_date', 'end_date'], axis=1, inplace=True)
income_data.drop(['ts_code', 'ann_date', 'f_ann_date', 'end_date', 'ebit', 'ebitda'], axis=1, inplace=True)
fina_data.drop(['ts_code', 'ann_date', 'end_date'], axis=1, inplace=True)
cashflow_data.drop(['ts_code', 'ann_date', 'f_ann_date', 'end_date'], axis=1, inplace=True)

# 合并三年数据
data = pd.concat([balancesheet_data, fina_data, income_data, cashflow_data], axis=1)

# 添加是否为财务危机公司label
label = pd.DataFrame(([0] * 88 + [1] * 88) * 3, columns=['label'])
data = pd.concat([data, label], axis=1)


total_assets = data['total_assets'] # 资产总额
working_capital = data['working_capital'] # 营运资本
retained_earnings = data['retained_earnings'] # 留存收益
ebit = data['ebit'] # 息税前利润
total_hldr_eqy_inc_min_int = data['total_hldr_eqy_inc_min_int'] # 股东权益合计
total_liab = data['total_liab'] # 负债总额
assets_turn = data['assets_turn'] # 总资产周转率

x1 = working_capital / total_assets
x2 = retained_earnings / total_assets
x3 = ebit / total_assets
x4 = total_hldr_eqy_inc_min_int / total_liab
x5 = assets_turn

data['z-score'] = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 0.999 * x5
bankruptcy_threshold = 2.98
z_score_pred = data['z-score'] < bankruptcy_threshold
data['z-score_pred'] = z_score_pred

data_2017 = data[:176]
data_2016 = data[176:176 * 2].reset_index(drop=True)
data_2015 = data[176 * 2:176 * 3].reset_index(drop=True)

cm_plot(data_2017['label'], data_2017['z-score_pred'])
acc_2017 = accuracy_score(data_2017['label'], data_2017['z-score_pred'])

cm_plot(data_2016['label'], data_2016['z-score_pred'])
acc_2016 = accuracy_score(data_2016['label'], data_2016['z-score_pred'])

cm_plot(data_2015['label'], data_2015['z-score_pred'])
acc_2015 = accuracy_score(data_2015['label'], data_2015['z-score_pred'])