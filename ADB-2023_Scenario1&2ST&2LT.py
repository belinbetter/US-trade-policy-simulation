# -*- coding:utf8 -*-
# @Author: XuFeng
# @Date  : 2024/6/3
# @Desc  : 2025/2/7

from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm


sector_number = 35
china = {'label': 'PRC', 'start': 246}
usa = {'label': 'USA', 'start': 1471}

middle_countries = {
    'brazil': {'label': 'BRA', 'start': 141},
    'indonesia': {'label': 'INO', 'start': 701},
    'mexico': {'label': 'MEX', 'start': 1016},
    'poland': {'label': 'POL', 'start': 1156},
    'turkey': {'label': 'TUR', 'start': 1401},
    'bangladesh': {'label': 'BAN', 'start': 1506},
    'malaysia': {'label': 'MAL', 'start': 1541},
    'thailand': {'label': 'THA', 'start': 1611},
    'vietnam': {'label': 'VIE', 'start': 1646}
}


def trade_transfer(data_path, drop_ratio, trans_type='Scenario1'):
    """
    中美贸易数据转换：
    :param data_path: 产业部门贸易矩阵文件路径
    :param drop_ratio:  中美贸易下降比率
    :param trans_type:  贸易转移类型
        Scenario1: 美国对中国采用传统贸易救济工具——反倾销反补贴
          中国向美国的出口量的下降比例（drop_ratio）的部分转移到借道国家，
          同时，美国缺失的进口缺失量转移到除中国以外的其他国家（除美国外）

        Scenario2: 美国对中国采用传统贸易救济工具——反倾销反补贴；同时也对中国采用新型贸易救济工具——反规避和第三国PMS
          中国向美国和借道国家的出口量的下降比例（drop_ratio）的部分转移到剩余国家（除中国外），
          同时，美国和借道国家的进口缺失量转移到除中国以外的其他国家（除本国外——A国的出口额转移不会变为增加内需）

        Scenario3: 美国对中国采用传统贸易救济工具——反倾销反补贴；同时也对中国采用新型贸易救济工具——反规避和第三国PMS
          中国向美国和借道国家的出口量的下降比例（drop_ratio）的部分转移到中国（内销），
          同时，美国和借道国家的进口缺失量（维持缺失）
    :return:
    """
    if trans_type not in  ['Scenario1', 'Scenario2', 'Scenario3']:
        raise ValueError("trans_type must be 'Scenario1', 'Scenario2' or 'Scenario3'")
    print("读取数据文件...")
    # 修改这里：从读取xlsx改为读取csv
    matrix = pd.read_csv(data_path, index_col=0, header=0)

    print(f"{trans_type} 计算...")
    # 获取 中-->美 的贸易数据矩阵
    cs = china['start']-1
    us = usa['start']-1
    ce = cs+sector_number
    ue = us+sector_number

    matrix_china_usa = matrix.iloc[cs:ce, us:ue].copy()
    # 中-->美 贸易下降
    matrix.iloc[cs:ce, us:ue] = matrix_china_usa*(1 - drop_ratio)
    # 中-->美  贸易等比调整到中间（借道）国家
    matrix_china_usa = matrix_china_usa * drop_ratio  # 贸易减少量
    matrix_drop = matrix_china_usa.copy()
    countries_reduce = {'USA': matrix_china_usa}
    if trans_type == 'Scenario2' or trans_type == 'Scenario3':
        for middle_country in middle_countries:
            ms = middle_countries[middle_country]['start']-1
            me = ms+sector_number
            temp = matrix.iloc[cs:ce, ms:me].copy()
            # 中-->借道国家贸易下降
            matrix.iloc[cs:ce, ms:me] = temp * (1-drop_ratio)
            temp_drop = temp * drop_ratio
            matrix_drop += temp_drop.values
            countries_reduce[middle_countries[middle_country]['label']] = temp_drop
    index_list = matrix.index.tolist()
    """更新中国贸易出口份额"""
    print("贸易出口额重分配...")
    for i in tqdm(range(1, sector_number+1)):
        # 获取 中 --> 借道国家的S_i部门贸易数据
        middle_industries = []
        if trans_type == 'Scenario1':
            for country in middle_countries:
                middle_industries.append(index_list.index(f"{middle_countries[country]['label']}S{i}"))
        elif trans_type == 'Scenario2':
            exclude_countries = [china['label'], usa['label']]
            for country in middle_countries.keys():
                exclude_countries.append(middle_countries[country]['label'])
            for il, index in enumerate(index_list):
                if f'S{i}' in index and index[:3] not in exclude_countries:
                    middle_industries.append(il)
        elif trans_type == 'Scenario3':
            middle_industries.append(index_list.index(f"{china['label']}S{i}"))
        # 获取中国全部部门向借道国家S_i部门的出口量
        export_i = matrix.iloc[cs:ce, middle_industries]
        # 对行求和并求占比（缺失值由于整行均为0导致，比例中将其置为0）
        export_i_sum = export_i.sum(axis=1)
        export_i_pre = export_i.div(export_i_sum, axis=0)
        export_i_pre.fillna(0, inplace=True)
        # 部门S_i的贸易转移量
        china_i = matrix_drop.iloc[:, [i-1]]
        # 分配到借道国家的贸易出口量
        to_export_i = np.multiply(china_i.to_numpy(), export_i_pre.to_numpy())
        # 更新向借道国家的贸易出口量
        matrix.iloc[cs:ce, middle_industries] += to_export_i

    """更新美国和借道国家贸易进口份额，由中国进口的份额转移到除中国以外的所有国家"""
    print("\n 贸易进口额重分配...")
    reduce_countries = []
    if trans_type == 'Scenario1':
        reduce_countries = [usa]
        rc = [usa['label']]
    elif trans_type == 'Scenario2':
        reduce_countries = [usa]
        rc = [usa['label']]
        for country in middle_countries.keys():
            reduce_countries.append(middle_countries[country])
            rc.append(middle_countries[country]['label'])
    elif trans_type == 'Scenario3':
        # 减少的进口不转移增加
        pass

    for reduce_country in reduce_countries:
        if trans_type == 'Scenario3':
            continue
        print(f" \n {reduce_country['label']} 进口减少量重分配...")
        for i in tqdm(range(1, sector_number + 1)):
            middle_industries = []
            for il, index in enumerate(index_list):
                if f'S{i}' in index and index[:3] != china['label'] and index[:3] not in rc:
                # if f'S{i}' in index and index[:3] != china['label'] and index[:3] != reduce_country['label']:
                    middle_industries.append(il)
            # 获取美国全部部门向其他国家S_i部门的进口量
            rc_start = reduce_country['start']-1
            rc_end = rc_start + sector_number
            import_i = matrix.iloc[middle_industries, rc_start:rc_end]
            # 对列求和并求占比（缺失值由于整列均为0导致，比例中将其置为0）
            import_i_sum = import_i.sum(axis=0)
            import_i_pre = import_i.div(import_i_sum, axis=1)
            import_i_pre.fillna(0, inplace=True)
            # 美国或借道国家全部部门向S_i部门进口的贸易转移量
            usa_i = countries_reduce[reduce_country['label']].iloc[[i-1], :]
            # 分配到各国S_i进口的贸易转移量
            to_import_i = np.multiply(usa_i.to_numpy(), import_i_pre.to_numpy())
            # 更新向各国S_i的贸易进口量
            matrix.iloc[middle_industries, rc_start:rc_end] += to_import_i
    # 保存结果
    print("保存结果...")
    # 修改这里：从保存为xlsx改为保存为csv
    matrix.to_csv(f'{Path(data_path).parents[0]}/{Path(data_path).stem}_{trans_type}_DropRatio{drop_ratio}.csv')


if __name__ == '__main__':
    # 修改这里：将文件路径改为csv文件
    data_file_path = r"D:\3.数据库\邻接矩阵\CSV\[GIVCN] ADB2025(E62) 63R35S CSV格式\2024.csv"
    for trans_type in ['Scenario1', 'Scenario2', 'Scenario3']:
        trade_transfer(data_file_path, 0.2, trans_type)