import csv
import pandas as pd
import math

# 指定实验月份
experimental_month = '3'
# 指定受验者序号
examinee = 'Weight_A.csv'
# 指定输出文件的名字
file_name = 'nDCG_A.xlsx'

# 指定已有的CSV文件路径
input_file = '/Users/wangsihan/Downloads/system_data/remember2_weight/[replace_me1]/[replace_me2]'
# 指定新的rememberCSV文件路径
output_file_remember = '/Users/wangsihan/Downloads/system_data/nDCG/remember/[replace_me3]'
# 指定新的happyCSV文件路径
output_file_important = '/Users/wangsihan/Downloads/system_data/nDCG/important/[replace_me4]'
# 指定新的happyCSV文件路径
output_file_happy = '/Users/wangsihan/Downloads/system_data/nDCG/happy/[replace_me5]'

# 找到第一个要替换的位置的起始和结束索引
start_index1 = input_file.index("[replace_me1]")
end_index1 = start_index1 + len("[replace_me1]")

# 找到第二个要替换的位置的起始和结束索引
start_index2 = input_file.index("[replace_me2]")
end_index2 = start_index2 + len("[replace_me2]")

# 找到第三个要替换的位置的起始和结束索引
start_index3 = output_file_remember.index("[replace_me3]")
end_index3 = start_index3 + len("[replace_me3]")

# 找到第四个要替换的位置的起始和结束索引
start_index4 = output_file_important.index("[replace_me4]")
end_index4 = start_index4 + len("[replace_me4]")

# 找到第五个要替换的位置的起始和结束索引
start_index5 = output_file_happy.index("[replace_me5]")
end_index5 = start_index5 + len("[replace_me5]")

# 将替换内容插入指定的地址中
input_file = (input_file[:start_index1] + experimental_month +
              input_file[end_index1:start_index2] + examinee)
output_file_remember = (output_file_remember[:start_index3] + file_name)
output_file_important = (output_file_important[:start_index4] + file_name)
output_file_happy = (output_file_happy[:start_index4] + file_name)

# CSV文件已存在且不为空，读取现有数据并在后面加入新的列数据
existing_data = []
with open(input_file, mode='r') as file:
    reader = csv.DictReader(file)
    existing_data = list(reader)

# 整理原始数据类型
# 保存原始数据到变量 df_new
df_new = pd.read_csv(input_file)

# 将 end_day 列转换为日期类型
df_new['end_day'] = pd.to_datetime(df_new['end_day'])

# 保留日期，不要时间部分
df_new['end_day'] = df_new['end_day'].dt.date


# 定义函数 calculate，计算逆序
def calculate_nDCG(df, sort_column, event_output_columns, sheet_name_input):
    if isinstance(sort_column, list) and len(sort_column) == 3:
        # 按照指定列的数据大小重新排列
        df_sorted = df.sort_values(by=sort_column, ascending=[False, False, False])

    elif isinstance(sort_column, list) and len(sort_column) == 2:
        # 按照指定列的数据大小重新排列
        df_sorted = df.sort_values(by=sort_column, ascending=[False, False])

    else:
        # 按照指定列的数据大小重新排列
        df_sorted = df.sort_values(by=sort_column, ascending=False)

    # 提取指定列的数据，并只提取前10行数据（如果有的话），否则提取全部数据
    df_result = df_sorted[event_output_columns].head(10)

    # 指定要写入的工作表名
    df_result.to_excel(writer, sheet_name=sheet_name_input, index=False)


# 定义函数 opposite_calculate，计算正序
def opposite_calculate_nDCG(df, sort_column, event_output_columns, sheet_name_input):
    if isinstance(sort_column, list) and len(sort_column) == 3:
        # 按照指定列的数据大小重新排列
        df_sorted = df.sort_values(by=sort_column, ascending=[True, False, False])

    elif isinstance(sort_column, list) and len(sort_column) == 2:
        # 按照指定列的数据大小重新排列
        df_sorted = df.sort_values(by=sort_column, ascending=[True, False])

    else:
        # 按照指定列的数据大小重新排列
        df_sorted = df.sort_values(by=sort_column, ascending=True)

    # 提取指定列的数据，并只提取前10行数据（如果有的话），否则提取全部数据
    df_result = df_sorted[event_output_columns].head(10)

    # 指定要写入的工作表名
    df_result.to_excel(writer, sheet_name=sheet_name_input, index=False)



# 按照nDCG的式子进行计算
def get_DCG(target_sheet, target_column, dfs):
    column_data = dfs[target_sheet][target_column].values.tolist()
    DCG_list = []
    for i in range(1, len(column_data) + 1):
        molecular = column_data[i - 1]
        denominator = math.log(i + 1, 2)
        DCG = molecular / denominator
        DCG_list.append(DCG)

    return DCG_list


if __name__ == '__main__':
    # 列出三项顺序类型
    sequences = ['remember', 'happy', 'important']

    for sequence in sequences:
        if sequence == 'remember':
            # 時系列(1)
            # 指定要提取的列的索引
            columns_output_time_series = [0, 1, 3, 11]  # 第1，2，4, 12列
            # 读取原始CSV文件，并提取指定列的数据
            df = pd.read_csv(input_file, usecols=columns_output_time_series)
            # 提取前10行数据（如果有的话），否则提取全部数据
            df_time_series = df.head(10)
            # 创建一个ExcelWriter对象，指定要写入的文件名和工作表名
            writer = pd.ExcelWriter(output_file_remember, engine='xlsxwriter')
            df_time_series.to_excel(writer, sheet_name='時系列(1)', index=False)

            # 時系列逆順(2)
            df_time_series_conflict = df_time_series
            # 指定按照哪一列数据进行排序
            time_series_conflict_sort_column = 'number'  # 按照时间顺进行排序
            # 指定要输出的列
            time_series_conflict_output_columns = ['number', 'event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            time_series_conflict_sheet_name_input = '時系列逆順(2)'
            # 将数据写入表格
            calculate_nDCG(df_new, time_series_conflict_sort_column, time_series_conflict_output_columns,
                           time_series_conflict_sheet_name_input)

            # 持続時間(3)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_event_duration', 'number']  # 按照持続時間顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = '持続時間(3)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # 持続時間逆順(4)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_event_duration', 'number']  # 按照持続時間逆顺进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '持続時間逆順(4)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # あまり行かない(5)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_times_of_visited', 'number']  # 按照あまり行かない顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = 'あまり行かない(5)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # あまり行かない逆順(6)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_times_of_visited', 'number']  # 按照あまり行かない逆順进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = 'あまり行かない逆順(6)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 距離(7)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_distance', 'number']  # 按照距離顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = '距離(7)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # 距離逆順(8)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_distance', 'number']  # 按照距離逆顺进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '距離逆順(8)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # よくあった日数(9)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_person_metdays', 'number']  # 按照よくあった日数顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = 'よくあった日数(9)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # よくあった日数逆順(10)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_person_metdays', 'number']  # 按照よくあった日数逆顺进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = 'よくあった日数逆順(10)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 最近あった日数(11)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_number_of_days_since_last_since', 'number']  # 按照最近あった日数顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = '最近あった日数(11)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # 最近あった日数逆順(12)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_number_of_days_since_last_since', 'number']  # 按照最近あった日数逆順进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '最近あった日数逆順(12)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 写真の枚数(13)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_photos', 'number']  # 按照写真の枚数顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = '写真の枚数(13)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # 写真の枚数逆順(14)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_photos', 'number']  # 按照写真の枚数逆順进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '写真の枚数逆順(14)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # SNS(15)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_sns', 'number']  # 按照SNS顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = 'SNS(15)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # SNS逆順(16)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_sns', 'number']  # 按照SNS逆順进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = 'SNS逆順(16)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 場所順(17)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_place', 'place', 'end_day']  # 按照場所顺进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'place', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '場所順(17)'
            # 将数据写入表格
            calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 場所逆順(18)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_place', 'place', 'end_day']  # 按照場所逆顺进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'place', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '場所逆順(18)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 人物順(19)
            # 指定按照哪一列数据进行排序
            person_sort_column = ['weight_person', 'person', 'end_day']  # 按照人物顺进行排序
            # 指定要输出的列
            person_output_columns = ['event', 'end_day', 'person', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            person_sheet_name_input = '人物順(19)'
            # 将数据写入表格
            calculate_nDCG(df_new, person_sort_column, person_output_columns, person_sheet_name_input)

            # 人物逆順(20)
            # 指定按照哪一列数据进行排序
            person_sort_column = ['weight_person', 'person', 'end_day']  # 按照人物逆顺进行排序
            # 指定要输出的列
            person_output_columns = ['event', 'end_day', 'person', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            person_sheet_name_input = '人物逆順(20)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, person_sort_column, person_output_columns, person_sheet_name_input)

            # イベント順(21)
            # 指定按照哪一列数据进行排序
            event_sort_column = 'weight_event'  # 按照event顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = 'イベント順(21)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # イベント逆順(22)
            # 指定按照哪一列数据进行排序
            event_sort_column = 'weight_event'  # 按照event逆顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = 'イベント逆順(22)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # 「思い出したい」順(23)
            # 指定按照哪一列数据进行排序
            remember_sort_column = 'weight_remember'  # 按照思い出したい顺进行排序
            # 指定要输出的列
            remember_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            remember_sheet_name_input = '「思い出したい」順(23)'
            # 将数据写入表格
            calculate_nDCG(df_new, remember_sort_column, remember_output_columns, remember_sheet_name_input)

            # 「思い出したい」逆順(24)
            # 指定按照哪一列数据进行排序
            remember_sort_column = 'weight_remember'  # 按照思い出したい顺进行排序
            # 指定要输出的列
            remember_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            remember_sheet_name_input = '「思い出したい」逆順(24)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, remember_sort_column, remember_output_columns, remember_sheet_name_input)

            # 「思い出したい」順(new)(29)
            # 指定按照哪一列数据进行排序
            remember_sort_column = 'weight_remember(new)'  # 按照思い出したい顺(new)进行排序
            # 指定要输出的列
            remember_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            remember_sheet_name_input = '「思い出したい」順(new)(29)'
            # 将数据写入表格
            calculate_nDCG(df_new, remember_sort_column, remember_output_columns, remember_sheet_name_input)

            # 「思い出したい」逆順(new)(30)
            # 指定按照哪一列数据进行排序
            remember_sort_column = 'weight_remember(new)'  # 按照思い出したい顺(new)进行排序
            # 指定要输出的列
            remember_output_columns = ['event', 'end_day', 'remember']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            remember_sheet_name_input = '「思い出したい」逆順(new)(30)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, remember_sort_column, remember_output_columns, remember_sheet_name_input)

            # 保存并关闭ExcelWriter对象
            writer.save()

            # 计算nDCG
            # 读取之前保存的XLSX文件的工作表
            sheets_to_read_remember = ['時系列(1)', '時系列逆順(2)', '持続時間(3)', '持続時間逆順(4)', 'あまり行かない(5)',
                                       'あまり行かない逆順(6)', '距離(7)', '距離逆順(8)', 'よくあった日数(9)',
                                       'よくあった日数逆順(10)', '最近あった日数(11)', '最近あった日数逆順(12)', '写真の枚数(13)',
                                       '写真の枚数逆順(14)', 'SNS(15)', 'SNS逆順(16)', '場所順(17)', '場所逆順(18)',
                                       '人物順(19)', '人物逆順(20)', 'イベント順(21)', 'イベント逆順(22)',
                                       '「思い出したい」順(23)', '「思い出したい」逆順(24)',  '「思い出したい」順(new)(29)',
                                       '「思い出したい」逆順(new)(30)']
            dfs_remember = pd.read_excel(output_file_remember, sheet_name=sheets_to_read_remember)

            # IDCG
            # 读取原始CSV文件
            df = pd.read_csv(input_file)

            # 按照指定列的数据大小重新排列
            df_sorted_remember = df.sort_values(by='remember', ascending=False)

            # 提取指定列的数据，并只提取前10行数据（如果有的话），否则提取全部数据
            df_result_remember = df_sorted_remember['remember'].head(10)

            IDCG_value_remember = df_result_remember.values.tolist()
            IDCG = []
            for i in range(1, len(IDCG_value_remember) + 1):
                molecular = IDCG_value_remember[i - 1]
                denominator = math.log(i + 1, 2)
                DCG = molecular / denominator
                IDCG.append(DCG)
            sum_IDCG_remember = sum(IDCG)

            # 初始化一个列表来存储每次的nDCG值
            nDCG_values_remember = []

            # 循环保存工作表名字的列表，并计算总的DCG
            for sheet_name in sheets_to_read_remember:
                target_sheet = sheet_name
                target_column = sequence
                DCG = get_DCG(target_sheet, target_column, dfs_remember)
                # 计算每个序列的sum_DCG
                sum_DCG = sum(DCG)
                # 计算nDCG
                nDCG_result = sum_DCG / sum_IDCG_remember
                # 将sum_DCG值添加到sum_DCG_values列表中
                nDCG_values_remember.append(nDCG_result)

            print("remember")
            for item in nDCG_values_remember:
                print(item)

        if sequence == 'happy':
            # 時系列(1)
            # 指定要提取的列的索引
            columns_output_time_series = [0, 1, 3, 13]  # 第1，2，4, 14列
            # 读取原始CSV文件，并提取指定列的数据
            df = pd.read_csv(input_file, usecols=columns_output_time_series)
            # 提取前10行数据（如果有的话），否则提取全部数据
            df_time_series = df.head(10)
            # 创建一个ExcelWriter对象，指定要写入的文件名和工作表名
            writer = pd.ExcelWriter(output_file_happy, engine='xlsxwriter')
            df_time_series.to_excel(writer, sheet_name='時系列(1)', index=False)

            # 時系列逆順(2)
            df_time_series_conflict = df_time_series
            # 指定按照哪一列数据进行排序
            time_series_conflict_sort_column = 'number'  # 按照时间顺进行排序
            # 指定要输出的列
            time_series_conflict_output_columns = ['number', 'event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            time_series_conflict_sheet_name_input = '時系列逆順(2)'
            # 将数据写入表格
            calculate_nDCG(df_new, time_series_conflict_sort_column, time_series_conflict_output_columns,
                           time_series_conflict_sheet_name_input)

            # 持続時間(3)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_event_duration', 'number']  # 按照持続時間顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = '持続時間(3)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # 持続時間逆順(4)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_event_duration', 'number']  # 按照持続時間逆顺进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '持続時間逆順(4)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # あまり行かない(5)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_times_of_visited', 'number']  # 按照あまり行かない顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = 'あまり行かない(5)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # あまり行かない逆順(6)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_times_of_visited', 'number']  # 按照あまり行かない逆順进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = 'あまり行かない逆順(6)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 距離(7)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_distance', 'number']  # 按照距離顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = '距離(7)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # 距離逆順(8)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_distance', 'number']  # 按照距離逆顺进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '距離逆順(8)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # よくあった日数(9)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_person_metdays', 'number']  # 按照よくあった日数顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = 'よくあった日数(9)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # よくあった日数逆順(10)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_person_metdays', 'number']  # 按照よくあった日数逆顺进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = 'よくあった日数逆順(10)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 最近あった日数(11)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_number_of_days_since_last_since', 'number']  # 按照最近あった日数顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名

            # 指定要输出的工作表的名字
            event_sheet_name_input = '最近あった日数(11)'

            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # 最近あった日数逆順(12)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_number_of_days_since_last_since', 'number']  # 按照最近あった日数逆順进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '最近あった日数逆順(12)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 写真の枚数(13)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_photos', 'number']  # 按照写真の枚数顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = '写真の枚数(13)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # 写真の枚数逆順(14)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_photos', 'number']  # 按照写真の枚数逆順进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '写真の枚数逆順(14)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # SNS(15)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_sns', 'number']  # 按照SNS顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = 'SNS(15)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # SNS逆順(16)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_sns', 'number']  # 按照SNS逆順进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = 'SNS逆順(16)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 場所順(17)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_place', 'place', 'end_day']  # 按照場所顺进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'place', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '場所順(17)'
            # 将数据写入表格
            calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 場所逆順(18)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_place', 'place', 'end_day']  # 按照場所逆顺进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'place', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '場所逆順(18)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 人物順(19)
            # 指定按照哪一列数据进行排序
            person_sort_column = ['weight_person', 'person', 'end_day']  # 按照人物顺进行排序
            # 指定要输出的列
            person_output_columns = ['event', 'end_day', 'person', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            person_sheet_name_input = '人物順(19)'
            # 将数据写入表格
            calculate_nDCG(df_new, person_sort_column, person_output_columns, person_sheet_name_input)

            # 人物逆順(20)
            # 指定按照哪一列数据进行排序
            person_sort_column = ['weight_person', 'person', 'end_day']  # 按照人物逆顺进行排序
            # 指定要输出的列
            person_output_columns = ['event', 'end_day', 'person', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            person_sheet_name_input = '人物逆順(20)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, person_sort_column, person_output_columns, person_sheet_name_input)

            # イベント順(21)
            # 指定按照哪一列数据进行排序
            event_sort_column = 'weight_event'  # 按照event顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = 'イベント順(21)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # イベント逆順(22)
            # 指定按照哪一列数据进行排序
            event_sort_column = 'weight_event'  # 按照event逆顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = 'イベント逆順(22)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # 「幸せな気分」順(27)
            # 指定按照哪一列数据进行排序
            happy_sort_column = 'weight_happy'  # 按照幸せな気分顺进行排序
            # 指定要输出的列
            happy_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            happy_sheet_name_input = '「幸せな気分」順(25)'
            # 将数据写入表格
            calculate_nDCG(df_new, happy_sort_column, happy_output_columns, happy_sheet_name_input)

            # 「幸せな気分」逆順(28)
            # 指定按照哪一列数据进行排序
            happy_sort_column = 'weight_happy'  # 按照幸せな気分顺进行排序
            # 指定要输出的列
            happy_output_columns = ['event', 'end_day', 'happy']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            happy_sheet_name_input = '「幸せな気分」逆順(26)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, happy_sort_column, happy_output_columns, happy_sheet_name_input)


            # 保存并关闭ExcelWriter对象
            writer.save()

            # 计算nDCG
            # 读取之前保存的XLSX文件的工作表
            sheets_to_read_happy = ['時系列(1)', '時系列逆順(2)', '持続時間(3)', '持続時間逆順(4)', 'あまり行かない(5)',
                                    'あまり行かない逆順(6)', '距離(7)', '距離逆順(8)', 'よくあった日数(9)',
                                    'よくあった日数逆順(10)', '最近あった日数(11)', '最近あった日数逆順(12)', '写真の枚数(13)',
                                    '写真の枚数逆順(14)', 'SNS(15)', 'SNS逆順(16)', '場所順(17)', '場所逆順(18)',
                                    '人物順(19)',
                                    '人物逆順(20)', 'イベント順(21)', 'イベント逆順(22)', '「幸せな気分」順(25)',
                                    '「幸せな気分」逆順(26)']
            dfs_happy = pd.read_excel(output_file_happy, sheet_name=sheets_to_read_happy)

            # IDCG
            # 读取原始CSV文件
            df = pd.read_csv(input_file)

            # 按照指定列的数据大小重新排列
            df_sorted_happy = df.sort_values(by='happy', ascending=False)

            # 提取指定列的数据，并只提取前10行数据（如果有的话），否则提取全部数据
            df_result_happy = df_sorted_happy['happy'].head(10)

            IDCG_value_happy = df_result_happy.values.tolist()
            IDCG = []
            for i in range(1, len(IDCG_value_happy) + 1):
                molecular = IDCG_value_happy[i - 1]
                denominator = math.log(i + 1, 2)
                DCG = molecular / denominator
                IDCG.append(DCG)
            sum_IDCG_happy = sum(IDCG)


            # 初始化一个列表来存储每次的nDCG值
            nDCG_values_happy = []

            # 循环保存工作表名字的列表，并计算总的DCG
            for sheet_name in sheets_to_read_happy:
                target_sheet = sheet_name
                target_column = sequence
                DCG = get_DCG(target_sheet, target_column, dfs_happy)
                # 计算每个序列的sum_DCG
                sum_DCG = sum(DCG)
                # 计算nDCG
                nDCG_result = sum_DCG / sum_IDCG_happy
                # 将sum_DCG值添加到sum_DCG_values列表中
                nDCG_values_happy.append(nDCG_result)

            # print("happy")
            # for item in nDCG_values_happy:
            #     print(item)

        if sequence == 'important':
            # 時系列(1)
            # 指定要提取的列的索引
            columns_output_time_series = [0, 1, 3, 12]  # 第1，2，4, 13列
            # 读取原始CSV文件，并提取指定列的数据
            df = pd.read_csv(input_file, usecols=columns_output_time_series)
            # 提取前10行数据（如果有的话），否则提取全部数据
            df_time_series = df.head(10)
            # 创建一个ExcelWriter对象，指定要写入的文件名和工作表名
            writer = pd.ExcelWriter(output_file_important, engine='xlsxwriter')
            df_time_series.to_excel(writer, sheet_name='時系列(1)', index=False)

            # 時系列逆順(2)
            df_time_series_conflict = df_time_series
            # 指定按照哪一列数据进行排序
            time_series_conflict_sort_column = 'number'  # 按照时间顺进行排序
            # 指定要输出的列
            time_series_conflict_output_columns = ['number', 'event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            time_series_conflict_sheet_name_input = '時系列逆順(2)'
            # 将数据写入表格
            calculate_nDCG(df_new, time_series_conflict_sort_column, time_series_conflict_output_columns,
                           time_series_conflict_sheet_name_input)

            # 持続時間(3)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_event_duration', 'number']  # 按照持続時間顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = '持続時間(3)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # 持続時間逆順(4)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_event_duration', 'number']  # 按照持続時間逆顺进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '持続時間逆順(4)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # あまり行かない(5)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_times_of_visited', 'number']  # 按照あまり行かない顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = 'あまり行かない(5)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # あまり行かない逆順(6)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_times_of_visited', 'number']  # 按照あまり行かない逆順进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = 'あまり行かない逆順(6)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 距離(7)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_distance', 'number']  # 按照距離顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = '距離(7)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # 距離逆順(8)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_distance', 'number']  # 按照距離逆顺进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '距離逆順(8)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # よくあった日数(9)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_person_metdays', 'number']  # 按照よくあった日数顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = 'よくあった日数(9)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # よくあった日数逆順(10)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_person_metdays', 'number']  # 按照よくあった日数逆顺进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = 'よくあった日数逆順(10)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 最近あった日数(11)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_number_of_days_since_last_since', 'number']  # 按照最近あった日数顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = '最近あった日数(11)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # 最近あった日数逆順(12)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_number_of_days_since_last_since', 'number']  # 按照最近あった日数逆順进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '最近あった日数逆順(12)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 写真の枚数(13)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_photos', 'number']  # 按照写真の枚数顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = '写真の枚数(13)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # 写真の枚数逆順(14)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_photos', 'number']  # 按照写真の枚数逆順进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '写真の枚数逆順(14)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # SNS(15)
            # 指定按照哪一列数据进行排序
            event_sort_column = ['weight_sns', 'number']  # 按照SNS顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = 'SNS(15)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # SNS逆順(16)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_sns', 'number']  # 按照SNS逆順进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = 'SNS逆順(16)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 場所順(17)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_place', 'place', 'end_day']  # 按照場所顺进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'place', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '場所順(17)'
            # 将数据写入表格
            calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 場所逆順(18)
            # 指定按照哪一列数据进行排序
            place_sort_column = ['weight_place', 'place', 'end_day']  # 按照場所逆顺进行排序
            # 指定要输出的列
            place_output_columns = ['event', 'end_day', 'place', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            place_sheet_name_input = '場所逆順(18)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, place_sort_column, place_output_columns, place_sheet_name_input)

            # 人物順(19)
            # 指定按照哪一列数据进行排序
            person_sort_column = ['weight_person', 'person', 'end_day']  # 按照人物顺进行排序
            # 指定要输出的列
            person_output_columns = ['event', 'end_day', 'person', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            person_sheet_name_input = '人物順(19)'
            # 将数据写入表格
            calculate_nDCG(df_new, person_sort_column, person_output_columns, person_sheet_name_input)

            # 人物逆順(20)
            # 指定按照哪一列数据进行排序
            person_sort_column = ['weight_person', 'person', 'end_day']  # 按照人物逆顺进行排序
            # 指定要输出的列
            person_output_columns = ['event', 'end_day', 'person', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            person_sheet_name_input = '人物逆順(20)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, person_sort_column, person_output_columns, person_sheet_name_input)

            # イベント順(21)
            # 指定按照哪一列数据进行排序
            event_sort_column = 'weight_event'  # 按照event顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = 'イベント順(21)'
            # 将数据写入表格
            calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # イベント逆順(22)
            # 指定按照哪一列数据进行排序
            event_sort_column = 'weight_event'  # 按照event逆顺进行排序
            # 指定要输出的列
            event_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            event_sheet_name_input = 'イベント逆順(22)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, event_sort_column, event_output_columns, event_sheet_name_input)

            # 「重要」順(27)
            # 指定按照哪一列数据进行排序
            important_sort_column = 'weight_important'  # 按照重要顺进行排序
            # 指定要输出的列
            important_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            important_sheet_name_input = '「重要」順(27)'
            # 将数据写入表格
            calculate_nDCG(df_new, important_sort_column, important_output_columns, important_sheet_name_input)

            # 「重要」逆順(28)
            # 指定按照哪一列数据进行排序
            important_sort_column = 'weight_important'  # 按照重要顺进行排序
            # 指定要输出的列
            important_output_columns = ['event', 'end_day', 'important']  # 替换为实际的列名
            # 指定要输出的工作表的名字
            important_sheet_name_input = '「重要」逆順(28)'
            # 将数据写入表格
            opposite_calculate_nDCG(df_new, important_sort_column, important_output_columns, important_sheet_name_input)

            # 保存并关闭ExcelWriter对象
            writer.save()

            # 计算nDCG
            # 读取之前保存的XLSX文件的工作表
            sheets_to_read_important = ['時系列(1)', '時系列逆順(2)', '持続時間(3)', '持続時間逆順(4)', 'あまり行かない(5)',
                                        'あまり行かない逆順(6)', '距離(7)', '距離逆順(8)', 'よくあった日数(9)',
                                        'よくあった日数逆順(10)', '最近あった日数(11)', '最近あった日数逆順(12)', '写真の枚数(13)',
                                        '写真の枚数逆順(14)', 'SNS(15)', 'SNS逆順(16)', '場所順(17)', '場所逆順(18)',
                                        '人物順(19)',
                                        '人物逆順(20)', 'イベント順(21)', 'イベント逆順(22)', '「重要」順(27)', '「重要」逆順(28)']

            dfs_important = pd.read_excel(output_file_important, sheet_name=sheets_to_read_important)

            # IDCG
            # 读取原始CSV文件
            df = pd.read_csv(input_file)

            # 按照指定列的数据大小重新排列
            df_sorted_important = df.sort_values(by='important', ascending=False)

            # 提取指定列的数据，并只提取前10行数据（如果有的话），否则提取全部数据
            df_result_important = df_sorted_important['important'].head(10)

            IDCG_value_important = df_result_important.values.tolist()
            IDCG = []
            for i in range(1, len(IDCG_value_important) + 1):
                molecular = IDCG_value_important[i - 1]
                denominator = math.log(i + 1, 2)
                DCG = molecular / denominator
                IDCG.append(DCG)
            sum_IDCG_important = sum(IDCG)

            # 初始化一个列表来存储每次的nDCG值
            nDCG_values_important = []

            # 循环保存工作表名字的列表，并计算总的DCG
            for sheet_name in sheets_to_read_important:
                target_sheet = sheet_name
                target_column = sequence
                DCG = get_DCG(target_sheet, target_column, dfs_important)
                # 计算每个序列的sum_DCG
                sum_DCG = sum(DCG)
                # 计算nDCG
                nDCG_result = sum_DCG / sum_IDCG_important
                # 将sum_DCG值添加到sum_DCG_values列表中
                nDCG_values_important.append(nDCG_result)

            # print("important")
            # for item in nDCG_values_important:
            #     print(item)
