# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 08:23:44 2019

@author: Xzw

E-mail: diligencexu@gmail.com
"""

import pandas as pd
import numpy as np

def get_data():
    # 财务数据指标
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

    # 记录完整数据列
    tmp = fina_data.isnull().any()
    fina_full_col = [i for i in tmp.index if not tmp[i]]

    tmp = income_data.isnull().any()
    income_full_col = [i for i in tmp.index if not tmp[i]]

    tmp = cashflow_data.isnull().any()
    cashflow_full_col = [i for i in tmp.index if not tmp[i]]

    tmp = balancesheet_data.isnull().any()
    balancesheet_full_col = [i for i in tmp.index if not tmp[i]]

    # 必需数据列
    necessary_col = [
        'ts_code',
        # 财务数据指标
        'current_ratio',  # 流动比率
        'quick_ratio',  # 速动比率
        # 'invturn_days',# 存货周转天数
        # 'inv_turn',# 存货周转率
        # 'arturn_days',# 应收账款周转天数
        'ar_turn',  # 应收账款周转率
        'ca_turn',  # 流动资产周转率
        'fa_turn',  # 固定资产周转率
        'assets_turn',  # 总资产周转率
        'ebit',  # 息税前收益
        'netdebt',  # 净债务
        'tangible_asset',  # 有形资产
        'working_capital',  # 营运资本
        'retained_earnings',  # 留存收益
        'netprofit_margin',  # 销售净利率
        'grossprofit_margin',  # 销售毛利率
        'profit_to_gr',  # 净利润/营业总收入
        'saleexp_to_gr',  # 销售费用/营业总收入
        'adminexp_of_gr',  # 管理费用/营业总收入
        'finaexp_of_gr',  # 财务费用/营业总收入
        'gc_of_gr',  # 营业总成本/营业总收入
        'op_of_gr',  # 营业利润/营业总收入
        'ebit_of_gr',  # 息税前利润/营业总收入
        'roe',  # 净资产收益率
        'roe_waa',  # 加权平均净资产收益率
        'roa',  # 总资产报酬率
        'npta',  # 总资产净利润
        'debt_to_assets',  # 资产负债率
        'assets_to_eqt',  # 权益乘数
        'dp_assets_to_eqt',  # 权益乘数(杜邦分析)
        'ca_to_assets',  # 流动资产/总资产
        'nca_to_assets',  # 非流动资产/总资产
        'tbassets_to_totalassets',  # 有形资产/总资产
        'currentdebt_to_debt',  # 流动负债/负债合计
        'longdeb_to_debt',  # 非流动负债/负债合计
        'debt_to_eqt',  # 产权比率
        'tangibleasset_to_debt',  # 有形资产/负债合计
        'turn_days',  # 营业周期
        'roa_yearly',  # 年化总资产净利率
        'roa_dp',  # 总资产净利率(杜邦分析)
        'fixed_assets',  # 固定资产合计
        # 'profit_prefin_exp',# 扣除财务费用前营业利润
        # 'op_to_ebt',# 营业利润／利润总额
        'equity_yoy',  # 净资产同比增长率
        # 利润表数据
        'total_revenue',  # 营业总收入
        'revenue',  # 营业收入
        # 'int_income',# 利息收入
        'operate_profit',  # 营业利润
        'total_profit',  # 利润总额
        'income_tax',  # 所得税费用
        # 资产负债表数据
        'cap_rese',  # 资本公积金
        'undistr_porfit',  # 未分配利润
        'surplus_rese',  # 盈余公积金
        'notes_receiv',  # 应收票据
        'accounts_receiv',  # 应收账款
        'inventories',  # 存货
        'goodwill',  # 商誉
        'notes_payable',  # 应付票据
        'acct_payable',  # 应付账款
        'bond_payable',  # 应付债券
        # 现金流量表数据
        'net_profit',  # 净利润
        'finan_exp',  # 财务费用
        'c_inf_fr_operate_a',  # 经营活动现金流入小计
        'st_cash_out_act',  # 经营活动现金流出小计
        'n_cashflow_act',  # 经营活动产生的现金流量净额
        'stot_inflows_inv_act',  # 投资活动现金流入小计
        'stot_out_inv_act',  # 投资活动现金流出小计
        'n_cashflow_inv_act',  # 投资活动产生的现金流量净额
        'stot_cash_in_fnc_act',  # 筹资活动现金流入小计
        'stot_cashout_fnc_act',  # 筹资活动现金流出小计
        'n_cash_flows_fnc_act',  # 筹资活动产生的现金流量净额
    ]

    # 删除无关数列
    balancesheet_data.drop(['ann_date', 'f_ann_date', 'end_date'], axis=1, inplace=True)
    income_data.drop(['ts_code', 'ann_date', 'f_ann_date', 'end_date', 'ebit', 'ebitda'], axis=1, inplace=True)
    fina_data.drop(['ts_code', 'ann_date', 'end_date'], axis=1, inplace=True)
    cashflow_data.drop(['ts_code', 'ann_date', 'f_ann_date', 'end_date'], axis=1, inplace=True)

    # 合并三年数据
    data = pd.concat([balancesheet_data, fina_data, income_data, cashflow_data], axis=1)
    data = data[necessary_col]

    # 添加是否为财务危机公司label
    label = pd.DataFrame(([0] * 88 + [1] * 88) * 3, columns=['label'])
    data = pd.concat([data, label], axis=1)
    
    # 删除缺失数据过多的指标
    data.dropna(thresh=500, axis=1, inplace=True)
    keep_col = list(data.columns)
    
    # 缺失数据用均值填补
    for i in keep_col[1:]:
        data[i].fillna(data[i].mean(), inplace=True)
    
    return data, keep_col