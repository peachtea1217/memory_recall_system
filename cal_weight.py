import csv
from datetime import date
import datetime
from get_haversine_distance import haversine_distance
from get_gps import get_gps
import os


# 入力データのCSVファイル
filename = '/Users/wangsihan/Downloads/system_data/person_data/wang/data_wang_test.csv'
home_name = "クローバー・グランデ昭和町"
filename_save = '/Users/wangsihan/Downloads/system_data/weight_normalization/3/Weight_wang.csv'

with open(filename, encoding="utf-8-sig") as f:
    # 创建csv文件读取器
    reader = csv.DictReader(f)
    # 输入一个列表，其中每项都是一个字典，键和值分别以
    # {'number': '1', 'event': 'アルバイト', 'start_day': '2022/10/1', 'end_day': '2022/10/1', 'start_time': '10:00',
    # 'end_time': '15:20', 'tag': 'バイト', 'person': 'なし', 'SNS': 'しなかった', 'place': '餃子の王将西田辺店', 'num_photo': '0', }形式储存
    total_list = [row for row in reader]

# 将SNS的值替换为1和0
for each_dic in total_list:
    if each_dic['SNS'] == 'しなかった':
        each_dic['SNS'] = 0
    else:
        each_dic['SNS'] = 1

# 将number,num_photo,remember,important,happy的值由字符串变为int型
for each_dic in total_list:
    each_dic['number'] = int(each_dic['number'])
    each_dic['num_photo'] = int(each_dic['num_photo'])
    each_dic['remember'] = int(each_dic['remember'])
    each_dic['important'] = int(each_dic['important'])
    each_dic['happy'] = int(each_dic['happy'])

# 持続時間

event_values_dic = {}  # 创建一个新的字典，用于存储所有"number"键的值
# 遍历文件，取出其中关于事件持续时间的四项
for each_dic in total_list:
    if "number" in each_dic:  # 如果这个人的字典中包含"number"键
        event_values_dic[each_dic['number']] = {
            'number': each_dic['number'],
            'start_day': each_dic['start_day'],
            'end_day': each_dic['end_day'],
            'start_time': each_dic['start_time'],
            'end_time': each_dic['end_time']
        }  # 将这个人的"number"键的值添加到event_values_dic集合中

# {'1': {'number': '1', 'start_day': '2022/10/1', 'end_day': '2022/10/1', 'start_time': '10:00', 'end_time': '15:20'},
# '2': {'number': '2', 'start_day': '2022/10/1', 'end_day': '2022/10/1', 'start_time': '21:45', 'end_time': '22:45'}}
# print(event_values_dic)

# 新建一个字典，用来储存number和算出来的持续时间
event_duration = []
# 通过datetime来计算事件的持续时间
for event in event_values_dic.values():
    start_datetime = datetime.datetime.strptime(event['start_day'] + ' ' + event['start_time'], '%Y/%m/%d %H:%M')
    end_datetime = datetime.datetime.strptime(event['end_day'] + ' ' + event['end_time'], '%Y/%m/%d %H:%M')
    if end_datetime < start_datetime:
        end_datetime += datetime.timedelta(days=1)
    duration = end_datetime - start_datetime
    # 从datetime.timedelta(seconds=19200)这种形式中，直接提取秒数
    duration = int(duration.total_seconds())
    durations = {'number': event['number'], 'duration': duration}
    event_duration.append(durations)

# 得到一个以下形式的列表
# [{'number': '1', 'duration': 19200}, {'number': '2', 'duration': 3600}, {'number': '3', 'duration': 15000}]
# print(event_duration)

# 通过让total_list和event_duration中的number键进行匹配，从而将对应的事件持续事件加入到total_list当中
for items_1 in total_list:
    for items_2 in event_duration:
        if items_1['number'] == items_2['number']:
            items_1.update({'duration': items_2['duration']})

# total_list更新为以下格式
# [{'number': '1', 'event': 'アルバイト', 'start_day': '2022/10/1', 'end_day': '2022/10/1', 'start_time': '10:00', 'end_time': '15:20', 'tag': 'バイト', 'person': 'なし', 'SNS': 'しなかった', 'place': '餃子の王将西田辺店', 'num_photo': '0', 'duration': 19200}
# print(total_list)

# 取出最大值和最小值
# 持续时间最大值
sorted_event_duration = sorted(event_duration, key=lambda x: x['duration'], reverse=True)
max_event_duration = sorted_event_duration[0]['duration']
# print(max_event_duration)

# 持续时间最小值
sorted_event_duration = sorted(event_duration, key=lambda x: x['duration'], reverse=False)
min_event_duration = sorted_event_duration[0]['duration']
# print(min_event_duration)



def weight_Event_Duration(count_duration):  # 传入int型的事件持续时间的秒数形式
    weight_event_duration = (count_duration - min_event_duration) / (max_event_duration - min_event_duration)
    return weight_event_duration  # 传出float型的事件持续时间的权重


weight_duration_result = {}  # 承接持续时间的权重的结果的空字典

for each_dic in total_list:
    calculate_weight_event_duration = weight_Event_Duration(each_dic.get('duration'))  # 用上面的方法计算每个事件的持续时间，并放入一个变量中
    weight_duration_result[
        each_dic.get('number')] = calculate_weight_event_duration  # 将这个变量的值赋给新创建的承接持续时间的权重的结果的空字典

# {'1': 1.0, '2': 0.1875, '3': 0.78125, '4': 0.0625, '5': 0.03125}
print(f"「持続時間」の重み!:{weight_duration_result}\n")

# for value in weight_event_duration_result.values():
#     print(value)


# 場所のランキング

# 先提取出所有场所信息放到一个列表中(不重复)
list_place_values = []  # 创建一个新的集合，用于存储所有"place"键的值
for place in total_list:
    if "place" in place:  # 如果这个人的字典中包含"place"键
        list_place_values.append(place["place"])  # 将这个人的"place"键的值添加到pre_place_values集合中
# ['餃子の王将西田辺店', 'クローバー・グランデ昭和町', '餃子の王将西田辺店', '餃子の王将西田辺店', 'おしゃれ洗濯じゃぶじゃぶ阪南店']
# print(list_place_values)


# 计算距离
# home_name = "ネオハイツ内本町"
home = get_gps(home_name)
print(f"自宅のGPSは：{home}\n")

# 用于存储地点和其坐标的字典
place_gps_dic = {}
for place in list_place_values:
    place_gps_dic[place] = get_gps(place)

# {'餃子の王将西田辺店': (34.6221374, 135.5149532), 'クローバー・グランデ昭和町': (34.6248917, 135.5159534), 'おしゃれ洗濯じゃぶじゃぶ阪南店': (34.624641, 135.5154115), '大阪公立大学 学術情報総合センター': (34.5922412, 135.5055288)]
# print(place_gps_dic)

# 计算两地点之间的相对距离
relative_distance_dic = {}

for location, coords in place_gps_dic.items():
    distance = haversine_distance(home[0], home[1], coords[0], coords[1])
    relative_distance_dic[location] = distance
# print(relative_distance_dic)

# 找到去过的最远的场所
max_distance = max((value for value in relative_distance_dic.values() if value is not None), default=0)
# 找到去过的最近的场所
min_distance = min((value for value in relative_distance_dic.values() if value is not None), default=0)


# 计算地点"遠い"的权重的函数
def weight_Distance(distance_place):  # 传入int型的场所对应的去过回数
    if distance_place is not None:
        weight_distance = (distance_place - min_distance) / (max_distance - min_distance)
        return weight_distance  # 传出float型的场所去过回数的权重
    else:
        return 0.0


weight_relative_distance_dic_result = {}  # 存储「距離」の重み的结果的字典
for place in relative_distance_dic:
    weight_relative_distance_dic_result[place] = weight_Distance(relative_distance_dic.get(place))

# print(f"「遠い」の重み:{weight_relative_distance_dic_result}\n")

# 计算所有地名出现的次数
place_times_visit = {}
for item in list_place_values:
    if item in place_times_visit:
        place_times_visit[item] += 1
    else:
        place_times_visit[item] = 1
# {'餃子の王将西田辺店': 10, 'クローバー・グランデ昭和町': 36, 'おしゃれ洗濯じゃぶじゃぶ阪南店': 1, '大阪公立大学 学術情報総合センター': 4}
# print(place_times_visit)

# 找到去过的最大次数的场所
max_count_place_times_visit = max(place_times_visit.values())
# print(f"max:{max_count_place_times_visit}")
# 找到去过的最小次数的场所
min_count_place_times_visit = min(place_times_visit.values())
# print(f"min:{min_count_place_times_visit}")

# 计算地点"去过回数"的权重的函数
def weight_Seldom_Visit(count_place_times_of_visited):  # 传入int型的场所对应的去过回数
    if max_count_place_times_visit == min_count_place_times_visit:
        return 0.0
    else:
        weight_seldom_visit = 1 - ((count_place_times_of_visited - min_count_place_times_visit) /
                                       (max_count_place_times_visit - min_count_place_times_visit))
        return weight_seldom_visit  # 传出float型的场所去过回数的权重


weight_place_seldom_visit_result = {}  # 存储「あまり行かない」の重み的结果的字典
for place in place_times_visit:
    weight_place_seldom_visit_result[place] = weight_Seldom_Visit(place_times_visit.get(place))

# print(f"「あまり行かない」の重み:{weight_place_times_visit_result}\n")


# 場所の重み

# 場所ランキングの関数
def weight_Place(weight_times_visit, weight_distance):  # 传入两个float型数据
    weight_place = weight_distance + weight_times_visit
    return weight_place  # 输入一个float型数据


weight_place_result = {}
for place in weight_place_seldom_visit_result:
    weight_place_result[place] = weight_Place(float(weight_relative_distance_dic_result[place]), float(
        weight_place_seldom_visit_result[place]))

# print(f"場所の重み:{weight_place_result}\n")


# 人物のランキング

# 「よく会った」の重み
set_person_values = set()  # "person"キーのすべての値を格納する新しいコレクションを作成する
for items in total_list:
    if "person" in items:  # その人の辞書に "person "キーが含まれている場合
        set_person_values.add(items["person"])  # この人の "person "キーの値をpre_person_valuesコレクションに追加する。
set_person_values.discard("なし")  # セットから「なし」を外す

# 現在のpre_person_valuesのリストに'、'でリンクされた項目を含めることがある
# 分割後も同じ人の名前が続くのを避けるため、重複を削除できるsetを使用
person_values = set()
for person in set_person_values:
    names = person.split("、")  # 如果这一项中包含'、'，将这一项拆分成多个子字符串
    person_values.update(names)  # 使用拆分后的字符串替换原来的项

# 最后将集合其转换为列表
person_values = list(person_values)
# 打印所有"person"键的值 ['鐘', '村上', '劉', '山田', '袁', '松本', '白川']
# print(f"person_values:{person_values}\n")

# 通过上一步找到的person的值，来找到对应日程的结束时间
pre_person_day_list = {x: [] for x in person_values}

# 更新pre_person_day_list字典中对应的值
for each_dic in total_list:
    for name in person_values:
        if name in each_dic['person']:
            pre_person_day_list[name].append({'person': each_dic['person'], 'end_day': each_dic['end_day']})

# print(f"pre_person_day_list:{pre_person_day_list}\n")

# 计算每个人物对应的所有日期
person_day_list = {}  # 创建一个包含每个人物及其对应的见面日期的空字典

for key, value in pre_person_day_list.items():
    calculation_list = []
    for item in value:
        if item not in calculation_list:
            calculation_list.append(item)
    person_day_list[key] = calculation_list

# {'袁': [{'person': '袁', 'end_day': '2022/10/23'}, {'person': '袁', 'end_day': '2022/10/27'}, {'person': '袁', 'end_day': '2022/10/28'}, {'person': '袁', 'end_day': '2022/10/29'}, {'person': '袁', 'end_day': '2022/10/30'}], '松本': [{'person': '白川、松本', 'end_day': '2022/10/20'}], '白川': [{'person': '白川、松本', 'end_day': '2022/10/20'}, {'person': '白川', 'end_day': '2022/10/20'}], '劉': [{'person': '劉', 'end_day': '2022/10/6'}], '鐘': [{'person': '鐘', 'end_day': '2022/10/8'}, {'person': '鐘', 'end_day': '2022/10/12'}], '山田': [{'person': '山田', 'end_day': '2022/10/12'}], '村上': [{'person': '村上', 'end_day': '2022/10/5'}, {'person': '村上', 'end_day': '2022/10/12'}, {'person': '村上', 'end_day': '2022/10/19'}]}
# print(f"person_day_list:{person_day_list}\n")

# 计算每个人共见面了几天
count_person_metdays_dic = {}
for key in person_day_list.keys():
    count_person_metdays_dic[key] = len(person_day_list[key])
# {'袁': 5, '村上': 3, '山田': 1, '松本': 1, '劉': 1, '鐘': 2, '白川': 2}
# print(f"count_person_metdays_dic:{count_person_metdays_dic}\n")

# 计算见面的次数的最大值 ，('袁', 5)
max_count_person_metdays = max(count_person_metdays_dic.values())
# print(f"max_count_person_metdays:{max_count_person_metdays}")
# 计算见面的次数的最小值 ，('袁', 5)
min_count_person_metdays = min(count_person_metdays_dic.values())
# print(f"min_count_person_metdays:{min_count_person_metdays}")


# 计算每个人的"见过的天数"的权重
def weight_FreqMet(count_metdays):  # 传入int型的见面的次数的最大值
    weight_metdays = (count_metdays - min_count_person_metdays) / (max_count_person_metdays - min_count_person_metdays)
    return weight_metdays  # 输出int型的见过的天数"的权重


weight_freqmet_result = {}  # 承接见面的次数的权重的结果的空字典
for items in count_person_metdays_dic:
    weight_freqmet_result[items] = weight_FreqMet(count_person_metdays_dic.get(items))

# 「よく会った」の重み
# print(f"「よく会った」の重み:{weight_freqmet_result}")


# 「最近会った」の重みを計算

# 将日期转换为datetime对象
for keys, values in person_day_list.items():
    # 比较出最晚的一天，并将日期转换为str格式
    min_date = datetime.datetime.strptime(values[-1]['end_day'], '%Y/%m/%d')
    person_day_list[keys] = min_date.strftime('%Y/%m/%d')

# 每个人物对应的最后见到的一天
# {'鐘': '2022/10/08', '村上': '2022/10/05', '松本': '2022/10/20', '山田': '2022/10/12', '劉': '2022/10/06', '白川': '2022/10/20', '袁': '2022/10/23'}
# print(f"person_day_list最后见到的一天:{person_day_list}")

# 截止最后一天2023/3/31为止，计算每个人距离最后一天为止的时间
target_date = date(2023, 3, 31)

for name, date_str in person_day_list.items():
    d = date.fromisoformat(date_str.replace('/', '-'))
    delta = (target_date - d).days
    person_day_list[name] = delta


# 2023/3/31までの日数
# {'山田': 19, '鐘': 23, '劉': 25, '松本': 11, '白川': 11, '袁': 8, '村上': 26}
# print(f"person_day_list締切日までの日数:{person_day_list}")

# 计算最后见到的天数的最大值 ，('袁', 5)
max_count_days_since_last_met = max(person_day_list.values())
# print(f"最后见到的天数的最大值:{max_count_days_since_last_met}")
# 计算最后见到的天数的最小值 ，('袁', 5)
min_count_days_since_last_met = min(person_day_list.values())
# print(f"最后见到的天数的最小值:{min_count_days_since_last_met}")


# 计算每个人的"距离最后一次见面的天数"的权重 函数
def weight_Recent_Met(count_days_since_last_Met):  # 传入int型的最后见到的天数的最大值
    if max_count_days_since_last_met == min_count_days_since_last_met:
        return 0.0
    else:
        weight_days_since_last_met = 1 - ((count_days_since_last_Met - min_count_days_since_last_met)
                                           / (max_count_days_since_last_met - min_count_days_since_last_met))
        return weight_days_since_last_met  # 输出int型的"距离最后一次见面的天数"的权重


weight_days_since_last_met_result = {}  # 存储「最後に会った日からの日数」的结果的字典
for items in person_day_list:
    weight_days_since_last_met_result[items] = weight_Recent_Met(person_day_list.get(items))

# print(f"「最近会った」の重み:{weight_days_since_last_met_result}")


# 人物の重み

# 计算人物权重的函数
def weight_Person(weight_freqmet_result, weight_days_since_met_seen):  # 传入两个float型数据
    weight_person = weight_freqmet_result + weight_days_since_met_seen
    return weight_person  # 输入一个float型数据


# 储存人物的权重
weight_person_result = {}
for person in weight_freqmet_result:
    weight_person_result[person] = weight_Person(float(weight_freqmet_result[person]), float(
        weight_days_since_last_met_result[person]))
# print(f"人物の重み:{weight_person_result}\n")


# 写真の枚数の重みを計算

# 写真の最大张数 最小张数
max_photo = max([dic['num_photo'] for dic in total_list])
# print(f"写真の最大张数:{max_photo}\n")
min_photo = min([dic['num_photo'] for dic in total_list])
# print(f"写真の最小张数:{min_photo}\n")

# 计算照片张数权重的函数
def weight_Photo(count_photo):
    if max_photo != 0:
        weight_photos = (count_photo - min_photo) / (max_photo - min_photo)
        return weight_photos  # 输出float型数据
    else:
        return 0.0

# 计算照片的权重
weight_photos_result = {}  # 承接照片张数权重的结果的空字典

for each_dic in total_list:
    calculate_weight_photos = weight_Photo(each_dic.get('num_photo'))  # 用上面的方法计算照片张数，并放入一个变量中
    weight_photos_result[
        each_dic.get('number')] = calculate_weight_photos  # 将这个变量的值赋给新创建的承接照片张数的权重的结果的空字典

# {'28': '0.00', '29': '0.29', '30': '0.29', '31': '0.00', '32': '0.14'}
# print(f"「写真枚数」の重み:{weight_photos_result}\n")


# イベントの重みを計算

# 计算事件权重的函数
def weight_Event(weight_duration_value, weight_place_value, weight_person_value, weight_photos_value, weight_sns_value):
    weight_event_value = weight_duration_value + weight_place_value + weight_person_value + weight_photos_value + weight_sns_value
    return weight_event_value


# 计算时间持续时间的函数
def get_weight_duration_value(number_value):
    if number_value in weight_duration_result:
        return weight_duration_result[number_value]
    else:
        return 0.0

# 给定一个int型的number的值，找出其对应的场所的权重
def get_weight_place_value(number_value):
    for each_dic in total_list:
        if each_dic['number'] == number_value:
            if each_dic['place'] in weight_place_result:
                return float(weight_place_result[each_dic['place']])
            else:
                return None

# 给定一个int型的number的值，找出其对应的人物的权重
def get_weight_person_value(number_value):
    for each_dic in total_list:
        if each_dic['number'] == number_value:
            # 如果person栏是なし，那么就返回0.0
            if each_dic['person'] == 'なし':
                return 0.0
            # 如果person值在weight_person_result人物权重的字典中，且只有一个人，那么只输出这个人的person值
            elif each_dic['person'] in weight_person_result and '、' not in each_dic['person']:
                return float(weight_person_result[each_dic['person']])
            # 如果person值在weight_person_result人物权重的字典中，且有一个人以上，那么输出这些人的权重的平均值
            else:
                person_values_list = each_dic['person'].split('、')
                # 输出: ['A', 'B', 'C', 'D', 'E']
                person_avg = []  # 计算人物有1个以上时，人物对应的平均值
                for everyone in person_values_list:
                    person_avg.append(float(weight_person_result[everyone]))

                average = sum(person_avg) / len(person_avg)
                return average


# 计算照片权重的函数
def get_weight_photo_value(number_value):
    if number_value in weight_photos_result:
        return weight_photos_result[number_value]
    else:
        return 0.0

# SNS
def get_weight_sns_value(number_value):
    for each_dic in total_list:
        if each_dic['number'] == number_value:
            if each_dic['SNS'] == 1:
                return 1.0
            else:
                return 0.0



weight_event_result_dic = {}
weight_event_result_list = []

for each_dic in total_list:
    number_value = each_dic['number']
    # 事件持续时间的权重
    weight_duration_value = get_weight_duration_value(number_value)
    # 场所
    weight_place_value = get_weight_place_value(number_value)
    # 人物
    weight_person_value = get_weight_person_value(number_value)
    # 照片
    weight_photo_value = get_weight_photo_value(number_value)
    # SNS
    weight_sns_value = get_weight_sns_value(number_value)
    # 让以上权重相加，得出这个number对应的数字
    weight_event_result = weight_Event(weight_duration_value, weight_place_value, weight_person_value,
                                       weight_photo_value, weight_sns_value)
    # 将number和结果放入新的字典里
    weight_event_result_dic = {'number': each_dic['number'], 'weight_event': weight_event_result}
    weight_event_result_list.append(weight_event_result_dic)

# print(f"イベントの重み:{weight_event_result_list}\n")


# 计算两种排序

# 思い出したい1
def remember1(weight_place_value, weight_person_value, weight_photo_value):
    remember1_value = weight_place_value + weight_person_value + weight_photo_value
    return remember1_value


weight_remember1_dic = {}
weight_remember1_list = []

for each_dic in total_list:
    number_value = each_dic['number']
    # 场所
    weight_place_value = get_weight_place_value(number_value)
    # 人物
    weight_person_value = get_weight_person_value(number_value)
    # 照片
    weight_photo_value = get_weight_photo_value(number_value)
    # 让以上权重相加，得出这个number对应的数字
    weight_remember1_result = remember1(weight_place_value, weight_person_value, weight_photo_value)
    # 将number和结果放入新的字典里
    weight_remember1_dic = {'number': each_dic['number'], 'weight_remember1': weight_remember1_result}
    weight_remember1_list.append(weight_remember1_dic)

# print(f"思い出したい1:{weight_remember1_list}\n")


# 思い出したい2
def remember2(weight_photo_value, weight_place_value, weight_sns_value):
    remember2_value = weight_photo_value + weight_place_value + weight_sns_value
    return remember2_value


weight_remember2_dic = {}
weight_remember2_list = []

for each_dic in total_list:
    number_value = each_dic['number']
    # 照片
    weight_photo_value = get_weight_photo_value(number_value)
    # 场所
    weight_place_value = get_weight_place_value(number_value)
    # sns
    weight_sns_value = get_weight_sns_value(number_value)
    # 让以上权重相加，得出这个number对应的数字
    weight_remember2_result = remember2(weight_photo_value, weight_place_value, weight_sns_value)
    # 将number和结果放入新的字典里
    weight_remember2_dic = {'number': each_dic['number'], 'weight_remember2': weight_remember2_result}
    weight_remember2_list.append(weight_remember2_dic)

# print(f"思い出したい2:{weight_remember2_list}\n")



# 将已有的数据添加到新创建的表格里

# 存放所有持続時間の重み的列表
duration_list = []
new_duration = {}
for number_value in range(1, len(total_list)+1):
    duration_list.append(get_weight_duration_value(number_value))
    new_duration = {'weight_duration': duration_list}

print(f"持続時間の重み:{new_duration}\n")

# 「遠い」の重み
def get_weight_distance_value(number_value):
    for each_dic in total_list:
        if each_dic['number'] == number_value:
            # 如果place值在list_place_values地名列表中，那么只输出这个地名的place值
            if each_dic['place'] in list_place_values:
                return float(weight_relative_distance_dic_result[each_dic['place']])
            else:
                return 0.0

# 存放所有「遠い」の重み的列表
distance_list = []
new_distance = {}
for number_value in range(1, len(total_list)+1):
    distance_list.append(get_weight_distance_value(number_value))
    new_distance = {'weight_distance': distance_list}

print(f"「遠い」の重み:{new_distance}\n")


# 「あまり行かない」の重み
def get_weight_seldom_visit_value(number_value):
    for each_dic in total_list:
        if each_dic['number'] == number_value:
            # 如果place值在list_place_values地名列表中，那么只输出这个地名的place值
            if each_dic['place'] in list_place_values:
                return float(weight_place_seldom_visit_result[each_dic['place']])
            else:
                return 0.0

# 存放所有「あまり行かない」の重み的列表
seldom_visit_list = []
new_seldom_visit = {}
for number_value in range(1, len(total_list)+1):
    seldom_visit_list.append(get_weight_seldom_visit_value(number_value))
    new_seldom_visit = {'weight_seldom_visit': seldom_visit_list}

print(f"「あまり行かない」の重み:{new_seldom_visit}\n")

# 場所の重み
# 存放所有場所の重み的列表
place_list = []
new_place = {}
for number_value in range(1, len(total_list)+1):
    place_list.append(get_weight_place_value(number_value))
    new_place = {'weight_place': place_list}

print(f"場所の重み:{new_place}\n")


# 「よく会った」の重み
def get_weight_freqmet_value(number_value):
    for each_dic in total_list:
        if each_dic['number'] == number_value:
            # 如果person栏是なし，那么就返回0.0
            if each_dic['person'] == 'なし':
                return 0.0
            # 如果person值在person_values人物列表中，且只有一个人，那么只输出这个人的person值
            elif each_dic['person'] in person_values and '、' not in each_dic['person']:
                return float(weight_freqmet_result[each_dic['person']])
            # 如果person值在weight_person_result人物权重的字典中，且有一个人以上，那么输出这些人的权重的平均值
            else:
                freqmet_values_list = each_dic['person'].split('、')
                # 输出: ['A', 'B', 'C', 'D', 'E']
                avg_list = []  # 计算人物有1个以上时，输出对应的平均值
                for everyone in freqmet_values_list:
                    avg_list.append(float(weight_freqmet_result[everyone]))

                average = sum(avg_list) / len(avg_list)
                return average


# 存放所有「よく会った」の重み的列表
freqmet_list = []
new_freqmet = {}
for number_value in range(1, len(total_list)+1):
    freqmet_list.append(get_weight_freqmet_value(number_value))
    new_freqmet = {'weight_freqmet': freqmet_list}

print(f"「よく会った」の重み:{new_freqmet}\n")


# 「最近会った」の重み
def get_weight_recent_met_value(number_value):
    for each_dic in total_list:
        if each_dic['number'] == number_value:
            # 如果person栏是なし，那么就返回0.0
            if each_dic['person'] == 'なし':
                return 0.0
            # 如果person值在person_values人物列表中，且只有一个人，那么只输出这个人的person值
            elif each_dic['person'] in person_values and '、' not in each_dic['person']:
                return float(weight_days_since_last_met_result[each_dic['person']])
            # 如果person值在weight_person_result人物权重的字典中，且有一个人以上，那么输出这些人的权重的平均值
            else:
                recent_met_values_list = each_dic['person'].split('、')
                # 输出: ['A', 'B', 'C', 'D', 'E']
                avg_list = []  # 计算人物有1个以上时，输出对应的平均值
                for everyone in recent_met_values_list:
                    avg_list.append(float(weight_days_since_last_met_result[everyone]))

                average = sum(avg_list) / len(avg_list)
                return average


# 存放所有「最近会った」の重み的列表
recent_met_list = []
new_recent_met = {}
for number_value in range(1, len(total_list)+1):
    recent_met_list.append(get_weight_recent_met_value(number_value))
    new_recent_met = {
        'weight_recent_met': recent_met_list}

print(f"「最近会った」の重み:{new_recent_met}\n")


# 人物の重み
# 存放所有人物の重み的列表
person_list = []
new_person = {}
for number_value in range(1, len(total_list)+1):
    person_list.append(get_weight_person_value(number_value))
    new_person = {'weight_person': person_list}

print(f"人物の重み:{new_person}\n")


# 写真枚数の重み

# 存放所有写真枚数の重み的列表
photo_list = []
new_photo = {}
for number_value in range(1, len(total_list)+1):
    photo_list.append(get_weight_photo_value(number_value))
    new_photo = {'weight_photo': photo_list}

print(f"写真枚数の重み:{new_photo}\n")


# SNSの重み
# 存放所有SNSの重み的列表
sns_list = []
new_sns = {}
for number_value in range(1, len(total_list)+1):
    sns_list.append(get_weight_sns_value(number_value))
    new_sns = {'weight_sns': sns_list}

print(f"SNSの重み:{new_sns}\n")


#イベントの重み
# 存放所有イベントの重み的列表
event_list = []
new_event = {}
event_list = [float(item['weight_event']) for item in weight_event_result_list]
new_event = {'weight_event': event_list}

print(f"イベントの重み:{new_event}\n")


# 思い出したい1
# 存放所有思い出したい1的列表
remember1_list = []
new_remember1 = {}
remember1_list = [float(item['weight_remember1']) for item in weight_remember1_list]
new_remember1 = {'weight_remember1': remember1_list}

print(f"思い出したい1:{new_remember1}\n")


# 思い出したい2
# 存放所有思い出したい2的列表
remember2_list = []
new_remember2 = {}
remember2_list = [float(item['weight_remember2']) for item in weight_remember2_list]
new_remember2 = {'weight_remember2': remember2_list}

print(f"思い出したい2:{new_remember2}\n")


# 指定已有的CSV文件路径
# filename_save = '/Users/wangsihan/Downloads/system_data/weight_normalization/3/Weight_C.csv'

# 检查CSV文件是否存在
if not os.path.exists(filename_save) or os.stat(filename_save).st_size == 0:
    # CSV文件不存在或为空，直接写入新数据到空文档
    with open(filename_save, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=total_list[0].keys())
        writer.writeheader()
        writer.writerows(total_list)

else:
    # CSV文件已存在且不为空，读取现有数据并在后面加入新的列数据
    existing_data = []
    with open(filename_save, mode='r') as file:
        reader = csv.DictReader(file)
        existing_data = list(reader)


    # 将新数据添加到已有数据中
    for i, row in enumerate(existing_data):
        # 持続時間の重み
        event_duration = new_duration['weight_duration'][i]
        row['weight_duration'] = event_duration
        # 「遠い」の重み
        distance = new_distance['weight_distance'][i]
        row['weight_distance'] = distance
        # 「あまり行かない」の重み
        times_of_visited = new_seldom_visit['weight_seldom_visit'][i]
        row['weight_seldom_visit'] = times_of_visited
        # 場所の重み
        place = new_place['weight_place'][i]
        row['weight_place'] = place
        # 「よく会った」の重み
        freqmet = new_freqmet['weight_freqmet'][i]
        row['weight_freqmet'] = freqmet
        # 「最近会った」の重み
        recent_met = new_recent_met['weight_recent_met'][i]
        row['weight_recent_met'] = recent_met
        # 「人物」の重み
        person = new_person['weight_person'][i]
        row['weight_person'] = person
        # 写真枚数の重み
        photo = new_photo['weight_photo'][i]
        row['weight_photo'] = photo
        # SNSの重み
        sns = new_sns['weight_sns'][i]
        row['weight_sns'] = sns
        # イベントの重み
        event = new_event['weight_event'][i]
        row['weight_event'] = event
        # 思い出したい1
        remember1 = new_remember1['weight_remember1'][i]
        row['weight_remember1'] = remember1
        # 思い出したい2
        remember2 = new_remember2['weight_remember2'][i]
        row['weight_remember2'] = remember2


    # 将合并后的数据写回CSV文件
    with open(filename_save, mode='w', newline='') as file:
        fieldnames = existing_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(existing_data)























