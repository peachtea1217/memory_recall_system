import os
import glob
import pandas as pd
import math

# 设置输入文件的路径
folder_path = '/Users/wangsihan/Downloads/system_data/weight_normalization/3'
# 指定输出数据的xlxs文件
output_file_remember = '/Users/wangsihan/Downloads/system_data/nDCG/example.xlsx'


# 按照DCG的式子进行计算
def get_DCG(column_data):
    DCG_list = []
    for i in range(1, len(column_data) + 1):
        molecular = column_data[i - 1]
        denominator = math.log(i + 1, 2)
        DCG = molecular / denominator
        DCG_list.append(DCG)

    return DCG_list

def get_nDCG(DCG_list):
    # 计算每个序列的sum_DCG
    sum_DCG = sum(DCG_list)
    # 计算nDCG
    nDCG = sum_DCG / sum_IDCG_remember

    return nDCG


# 定义函数 calculate，计算正序
def calculate_DCG(df, target_column):
    if target_column == 'weight_person':
        sort_column = ['weight_person', 'person', 'number']
        # 按照指定列的数据大小重新排列
        df_sorted = df.sort_values(by=sort_column, ascending=[False, True, False])
    elif target_column == 'weight_place':
        sort_column = ['weight_place', 'place', 'number']
        # 按照指定列的数据大小重新排列
        df_sorted = df.sort_values(by=sort_column, ascending=[False, True, False])
    elif target_column == 'number':
        sort_column = 'number'
        # 按照指定列的数据大小重新排列
        df_sorted = df.sort_values(by=sort_column, ascending=[True])
    else:
        sort_column = [target_column, 'number']
        # 按照指定列的数据大小重新排列
        df_sorted = df.sort_values(by=sort_column, ascending=[False, False])

    # 提取指定列的数据，并只提取前10行数据（如果有的话），否则提取全部数据
    column_data = df_sorted['remember'].head(10)
    # 将数据化为list形式
    column_data_list_remember = column_data.values.tolist()
    # 计算DCG
    DCG = get_DCG(column_data_list_remember)
    return DCG


# 定义函数 opposite_calculate，计算逆序
def opposite_calculate_DCG(df, target_column):
    if target_column == 'weight_person':
        sort_column = ['weight_person', 'person', 'number']
        # 按照指定列的数据大小重新排列
        df_sorted = df.sort_values(by=sort_column, ascending=[True, True, False])
    elif target_column == 'weight_place':
        sort_column = ['weight_place', 'place', 'number']
        # 按照指定列的数据大小重新排列
        df_sorted = df.sort_values(by=sort_column, ascending=[True, True, False])
    elif target_column == 'number':
        sort_column = 'number'
        # 按照指定列的数据大小重新排列
        df_sorted = df.sort_values(by=sort_column, ascending=[False])
    else:
        sort_column = [target_column, 'number']
        # 按照指定列的数据大小重新排列
        df_sorted = df.sort_values(by=sort_column, ascending=[True, False])

    # 提取指定列的数据，并只提取前10行数据（如果有的话），否则提取全部数据
    column_data = df_sorted['remember'].head(10)
    # 将数据化为list形式
    column_data_list_remember = column_data.values.tolist()
    # 计算DCG
    DCG = get_DCG(column_data_list_remember)
    return DCG

if __name__ == '__main__':
    # 初始化两个个列表来存储每次的nDCG值
    nDCG_list_remember = []
    # 初始化两个字典来储存文件及其对应的nDCG值
    nDCG_dic_remember = {}


    # 获取所有 .csv 文件的列表
    files = glob.glob(os.path.join(folder_path, '*.csv'))
    # 对文件列表按照文件名进行排序
    files.sort()
    # 遍历排序后的文件列表
    for file in files:
        # 整理原始数据类型
        # 保存原始数据到变量 df
        df = pd.read_csv(file)

        # IDCG
        # 按照remember列的数据大小重新排列
        df_sorted_remember = df.sort_values(by='remember', ascending=False)
        # 提取指定列的数据，并只提取前10行数据（如果有的话），否则提取全部数据
        df_result_remember = df_sorted_remember['remember'].head(10)
        # 将数据化为list形式
        IDCG_value_remember = df_result_remember.values.tolist()
        IDCG = []
        for i in range(1, len(IDCG_value_remember) + 1):
            molecular = IDCG_value_remember[i - 1]
            denominator = math.log(i + 1, 2)
            DCG = molecular / denominator
            IDCG.append(DCG)
        sum_IDCG_remember = sum(IDCG)


        # 想要从csv文件中提取计算的列的名字
        target_columns = ['number', 'weight_duration', 'weight_seldom_visit', 'weight_distance', 'weight_freqmet',
                          'weight_recent_met', 'weight_photo', 'weight_sns', 'weight_place', 'weight_person',
                          'weight_event', 'weight_remember1', 'weight_remember2']


    #     for target_column in target_columns:
    #         # 按照指定列的数据大小正序排列，并计算对应DCG的值，得到一个DCG值的list
    #         DCG_asc = calculate_DCG(df, target_column)
    #         # 计算对应列的nDCG值
    #         nDCG_asc = get_nDCG(DCG_asc)
    #         # 将nDCG值添加到sum_DCG_values列表中
    #         nDCG_list_asc.append(nDCG_asc)
    #
    #         # 按照指定列的数据大小重新排列，并只提取前10行数据（如果有的话），否则提取全部数据
    #         DCG_desc = opposite_calculate_DCG(df, target_column)
    #         # 计算对应列的nDCG值
    #         nDCG_desc = get_nDCG(DCG_desc)
    #         # 将nDCG值添加到sum_DCG_values列表中
    #         nDCG_list_desc.append(nDCG_desc)
    #
    #     nDCG_dic_asc[file] = nDCG_list_asc
    #     nDCG_dic_desc[file] = nDCG_list_desc
    #
    # for key, value in nDCG_dic_asc.items():
    #     print(f"Key: {key}, Value: {value}")
    # print("")
    #
    # for key, value_list in nDCG_dic_asc.items():
    #     print(f"Key: {key}")
    #     for value in value_list:
    #         print(value)

        for target_column in target_columns:
            # 按照指定列的数据大小正序排列，并计算对应DCG的值，得到一个DCG值的list
            DCG_asc = calculate_DCG(df, target_column)
            # 计算对应列的nDCG值
            nDCG_asc = get_nDCG(DCG_asc)
            # 将nDCG值添加到sum_DCG_values列表中
            nDCG_list_remember.append(nDCG_asc)

            # 按照指定列的数据大小重新排列，并只提取前10行数据（如果有的话），否则提取全部数据
            DCG_desc = opposite_calculate_DCG(df, target_column)
            # 计算对应列的nDCG值
            nDCG_desc = get_nDCG(DCG_desc)
            # 将nDCG值添加到sum_DCG_values列表中
            nDCG_list_remember.append(nDCG_desc)


        nDCG_dic_remember[file] = nDCG_list_remember


    for key, value_list in nDCG_dic_remember.items():
        print(f"Key: {key}")
        for value in value_list:
            print(value)






