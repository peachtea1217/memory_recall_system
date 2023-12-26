import csv
from datetime import date
import datetime
import os
from get_haversine_distance import haversine_distance
from get_gps import get_gps

filename = '/Users/wangsihan/Downloads/system_data/person_data/yuan/data_yuan.csv'

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

# print(total_list)

# 人物のランキング

set_person_values = set()  # 创建一个新的集合，用于存储所有"person"键的值
for items in total_list:
    if "person" in items:  # 如果这个人的字典中包含"person"键
        set_person_values.add(items["person"])  # 将这个人的"person"键的值添加到pre_person_values集合中
set_person_values.discard("なし")  # 在集合中去掉"なし"这个项

# 现在的pre_person_values列表中可能存在用'、'连接的项
# 避免拆分后继续出现同一个人名，用set去掉重复项
person_values = set()
for person in set_person_values:
    names = person.split("、")  # 如果这一项中包含'、'，将这一项拆分成多个子字符串
    person_values.update(names)  # 使用拆分后的字符串替换原来的项

# 最后将集合其转换为列表
person_values = list(person_values)
# 打印所有"person"键的值 ['鐘', '村上', '劉', '山田', '袁', '松本', '白川']
print("person_values")
print(person_values)
print("")

# 通过上一步找到的person的值，来找到对应日程的结束时间
pre_person_day_list = {x: [] for x in person_values}

# 更新pre_person_day_list字典中对应的值
for each_dic in total_list:
    for name in person_values:
        if name in each_dic['person']:
            pre_person_day_list[name].append({'person': each_dic['person'], 'end_day': each_dic['end_day']})
print("pre_person_day_list")
print(pre_person_day_list)
print("")

# 计算每个人物对应的所有日期
person_day_list = {}  # 创建一个包含每个人物及其对应的见面日期的空字典

for key, value in pre_person_day_list.items():
    calculation_list = []
    for item in value:
        if item not in calculation_list:
            calculation_list.append(item)
    person_day_list[key] = calculation_list

# {'袁': [{'person': '袁', 'end_day': '2022/10/23'}, {'person': '袁', 'end_day': '2022/10/27'}, {'person': '袁', 'end_day': '2022/10/28'}, {'person': '袁', 'end_day': '2022/10/29'}, {'person': '袁', 'end_day': '2022/10/30'}], '松本': [{'person': '白川、松本', 'end_day': '2022/10/20'}], '白川': [{'person': '白川、松本', 'end_day': '2022/10/20'}, {'person': '白川', 'end_day': '2022/10/20'}], '劉': [{'person': '劉', 'end_day': '2022/10/6'}], '鐘': [{'person': '鐘', 'end_day': '2022/10/8'}, {'person': '鐘', 'end_day': '2022/10/12'}], '山田': [{'person': '山田', 'end_day': '2022/10/12'}], '村上': [{'person': '村上', 'end_day': '2022/10/5'}, {'person': '村上', 'end_day': '2022/10/12'}, {'person': '村上', 'end_day': '2022/10/19'}]}
print("person_day_list")
print(person_day_list)
print("")

# 计算每个人共见面了几天
count_person_metdays_dic = {}
for key in person_day_list.keys():
    count_person_metdays_dic[key] = len(person_day_list[key])
# {'袁': 5, '村上': 3, '山田': 1, '松本': 1, '劉': 1, '鐘': 2, '白川': 2}
print("count_person_metdays_dic")
print(count_person_metdays_dic)

# 计算见面的次数的最大值 ，('袁', 5)
max_count_person_metdays = max(count_person_metdays_dic.values())  # 只取最大值


# 计算每个人的"见过的天数"的权重
def weight_MetDays(count_metdays):  # 传入int型的见面的次数的最大值
    weight_metdays = count_metdays / max_count_person_metdays
    return weight_metdays  # 输出int型的见过的天数"的权重


weight_metdays_result = {}  # 承接见面的次数的权重的结果的空字典
for items in count_person_metdays_dic:
    weight_metdays_result[items] = weight_MetDays(count_person_metdays_dic.get(items))
    # weight_metdays_result[items] = "{:.4f}".format(weight_metdays_result[items])

# 「会った日数」の重み
print(f"「会った日数」の重み:{weight_metdays_result}")

# 「最後に会った日からの日数」の重みを計算

# 将日期转换为datetime对象
for keys, values in person_day_list.items():
    # 比较出最晚的一天，并将日期转换为str格式
    min_date = datetime.datetime.strptime(values[-1]['end_day'], '%Y/%m/%d')
    person_day_list[keys] = min_date.strftime('%Y/%m/%d')

# 每个人物对应的最后见到的一天
# {'鐘': '2022/10/08', '村上': '2022/10/05', '松本': '2022/10/20', '山田': '2022/10/12', '劉': '2022/10/06', '白川': '2022/10/20', '袁': '2022/10/23'}
# print("person_day_list最后见到的一天")
# print(person_day_list)
# print("")


# 截止最后一天2023/3/31为止，计算每个人距离最后一天为止的时间
target_date = date(2023, 3, 31)

for name, date_str in person_day_list.items():
    d = date.fromisoformat(date_str.replace('/', '-'))
    delta = (target_date - d).days
    person_day_list[name] = delta

# 2023/3/31までの日数
# {'山田': 19, '鐘': 23, '劉': 25, '松本': 11, '白川': 11, '袁': 8, '村上': 26}
print("2023/3/31までの日数")
print(person_day_list)
print("")

# 计算最后见到的天数的最大值 ，('袁', 5)
max_count_days_since_last_seen = max(person_day_list.values())  # 只取最大值


# 计算每个人的"距离最后一次见面的天数"的权重 函数
def weight_Number_Of_Days_Since_Last_Seen(count_days_since_last_seen):  # 传入int型的最后见到的天数的最大值
    weight_days_since_last_seen = 1 - (count_days_since_last_seen / max_count_days_since_last_seen)
    return weight_days_since_last_seen  # 输出int型的"距离最后一次见面的天数"的权重,且保留两位小数


weight_days_since_last_seen_result = {}  # 存储「最後に会った日からの日数」的结果的字典
for items in person_day_list:
    weight_days_since_last_seen_result[items] = weight_Number_Of_Days_Since_Last_Seen(person_day_list.get(items))
    # weight_days_since_last_seen_result[items] = "{:.2f}".format(weight_days_since_last_seen_result[items])  # 保留两位小数

print(f"「最後に会った日からの日数」の重み:{weight_days_since_last_seen_result}")


# 人物の重み

# 计算人物权重的函数
def weight_person(weight_met_days, weight_days_since_last_seen):  # 传入一个int型数据，一个float型数据
    weight_person = weight_met_days + weight_days_since_last_seen
    return weight_person  # 输入一个float型数据


weight_person_result = {}
for items in weight_metdays_result:
    weight_person_result[items] = weight_metdays_result[items] + float(weight_days_since_last_seen_result[items])
    # weight_person_result[items] = "{:.2f}".format(weight_person_result[items])  # 保留两位小数
print(f"人物の重み:{weight_person_result}\n")

# 場所のランキング

# 先提取出所有场所信息放到一个列表中(不重复)
list_place_values = []  # 创建一个新的集合，用于存储所有"place"键的值
for place in total_list:
    if "place" in place:  # 如果这个人的字典中包含"place"键
        list_place_values.append(place["place"])  # 将这个人的"place"键的值添加到pre_place_values集合中
# ['餃子の王将西田辺店', 'クローバー・グランデ昭和町', '餃子の王将西田辺店', '餃子の王将西田辺店', 'おしゃれ洗濯じゃぶじゃぶ阪南店']
# print(list_place_values)

# 计算所有地名出现的次数
place_times_of_visited = {}
for item in list_place_values:
    if item in place_times_of_visited:
        place_times_of_visited[item] += 1
    else:
        place_times_of_visited[item] = 1
# {'餃子の王将西田辺店': 10, 'クローバー・グランデ昭和町': 36, 'おしゃれ洗濯じゃぶじゃぶ阪南店': 1, '大阪公立大学 学術情報総合センター': 4}
print("所有地名出现的次数")
print(place_times_of_visited)
print("")

# 找到去过的最大次数的场所
max_count_place_times_of_visited = max(place_times_of_visited.values())


# 计算地点"去过回数"的权重的函数
def weight_times_of_visited(count_place_times_of_visited):  # 传入int型的场所对应的去过回数
    weight_times_of_visited = 1 - (count_place_times_of_visited / max_count_place_times_of_visited)
    return weight_times_of_visited  # 传出float型的场所去过回数的权重


weight_place_times_of_visited_result = {}  # 存储「行った回数」の重み的结果的字典
for place in place_times_of_visited:
    weight_place_times_of_visited_result[place] = weight_times_of_visited(place_times_of_visited.get(place))
    # weight_place_times_of_visited_result[place] = "{:.2f}".format(weight_place_times_of_visited_result[place])  # 保留两位小数

print(f"「行った回数」の重み:{weight_place_times_of_visited_result}")

# 计算距离
home_name = "フェニックス椎名町駅前"
home = get_gps(home_name)
print(f"自宅のGPSは：{home}\n")

# 之后可以改进
# 对于每个地点都获取它的gps

# 用于存储地点和其坐标的字典
place_gps_dic = {}
for place in list_place_values:
    place_gps_dic[place] = get_gps(place)

# {'餃子の王将西田辺店': (34.6221374, 135.5149532), 'クローバー・グランデ昭和町': (34.6248917, 135.5159534), 'おしゃれ洗濯じゃぶじゃぶ阪南店': (34.624641, 135.5154115), '大阪公立大学 学術情報総合センター': (34.5922412, 135.5055288)]
print(place_gps_dic)

# 计算两地点之间的相对距离

relative_distance_dic = {}

for location, coords in place_gps_dic.items():
    distance = haversine_distance(home[0], home[1], coords[0], coords[1])
    relative_distance_dic[location] = distance

# print(relative_distance_dic)
# 找到去过的最远的场所
# max_distance = max(relative_distance_dic, key = relative_distance_dic.get)
max_distance = max((value for value in relative_distance_dic.values() if value is not None), default=0)


# 计算地点"距离"的权重的函数
def weight_distance(distance_place):  # 传入int型的场所对应的去过回数
    if distance_place is not None:
        weight_distance = distance_place / max_distance
        return weight_distance  # 传出float型的场所去过回数的权重
    else:
        return None


weight_relative_distance_dic_result = {}  # 存储「距離」の重み的结果的字典
for place in relative_distance_dic:
    weight_relative_distance_dic_result[place] = weight_distance(relative_distance_dic.get(place))
    if weight_relative_distance_dic_result[place] is not None:
        weight_relative_distance_dic_result[place] = weight_relative_distance_dic_result[place]  # 保留两位小数
    else:
        pass

print(f"「距離」の重み:{weight_relative_distance_dic_result}\n")

# 将「距離」の重み的字典的内容按照从大到小排列
sorted_weight_relative_distance_dic = {}
for key, value in weight_relative_distance_dic_result.items():
    # 如果值为 None，添加相同键但值为 0
    if value is not None:
        sorted_weight_relative_distance_dic[key] = value
    # 如果值为 float，直接添加到新字典中
    else:
        sorted_weight_relative_distance_dic[key] = '0.0000'
print(f"「距離」の重み:{sorted_weight_relative_distance_dic}\n")


# 場所の重み

# 場所ランキングの関数
def weight_place(weight_times_of_visited, weight_distance):  # 传入两个float型数据
    weight_place = weight_distance + weight_times_of_visited
    return weight_place  # 输入一个float型数据


weight_place_result = {}
for place in weight_place_times_of_visited_result:
    weight_place_result[place] = weight_place(float(weight_place_times_of_visited_result[place]), float(
        sorted_weight_relative_distance_dic[place]))

print(f"場所の重み:{weight_place_result}\n")

# イベントのランキング

event_values_dic = {}  # 创建一个新的字典，用于存储所有"number"键的值
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

sorted_event_duration = sorted(event_duration, key=lambda x: x['duration'], reverse=True)
max_event_duration = sorted_event_duration[0]['duration']
# print(max_event_duration)

# 通过让total_list和event_duration中的number键进行匹配，从而将对应的事件持续事件加入到total_list当中
for items_1 in total_list:
    for items_2 in event_duration:
        if items_1['number'] == items_2['number']:
            items_1.update({'duration': items_2['duration']})


# total_list更新为以下格式
# [{'number': '1', 'event': 'アルバイト', 'start_day': '2022/10/1', 'end_day': '2022/10/1', 'start_time': '10:00', 'end_time': '15:20', 'tag': 'バイト', 'person': 'なし', 'SNS': 'しなかった', 'place': '餃子の王将西田辺店', 'num_photo': '0', 'duration': 19200}
# print(total_list)

def weight_event_duration(count_duration):  # 传入int型的事件持续时间的秒数形式
    weight_event_duration = count_duration / max_event_duration
    # weight_event_duration = "{:.2f}".format(weight_event_duration) # 保留两位小数
    return weight_event_duration  # 传出float型的事件持续时间的权重


weight_event_duration_result = {}  # 承接持续时间的权重的结果的空字典

for each_dic in total_list:
    calculate_weight_event_duration = weight_event_duration(each_dic.get('duration'))  # 用上面的方法计算每个事件的持续时间，并放入一个变量中
    # weight_event_duration_result[
    #     each_dic.get('event')] = calculate_weight_event_duration  # 将这个变量的值赋给新创建的承接持续时间的权重的结果的空字典
    # {'アルバイト': 0.609375, '情報基盤システム特論のスライド': 0.703125, 'まかない': 0.09375}
    weight_event_duration_result[
        each_dic.get('number')] = calculate_weight_event_duration  # 将这个变量的值赋给新创建的承接持续时间的权重的结果的空字典
    # weight_event_duration_result = {
    #     'number': each_dic['number'],
    #     'weight_event_duration': calculate_weight_event_duration
    # }

# {'1': 1.0, '2': 0.1875, '3': 0.78125, '4': 0.0625, '5': 0.03125}
print(f"「持続時間」の重み!:{weight_event_duration_result}\n")

for value in weight_event_duration_result.values():
    print(value)

# 写真の枚数の重みを計算

# 写真の最大枚数
for each_dic in total_list:
    max_photo = max([dic['num_photo'] for dic in total_list])


# print(max_photo)

# 计算照片张数权重的函数
def weight_photos(count_photo):
    if max_photo != 0:
        weight_photos = count_photo / max_photo
        # weight_photos = "{:.2f}".format(weight_photos) # 保留两位小数
        return weight_photos  # 输出float型数据
    else:
        return 0.0


# 计算照片的权重
weight_photos_result = {}  # 承接照片张数权重的结果的空字典

for each_dic in total_list:
    calculate_weight_photos = weight_photos(each_dic.get('num_photo'))  # 用上面的方法计算照片张数，并放入一个变量中
    weight_photos_result[
        each_dic.get('number')] = calculate_weight_photos  # 将这个变量的值赋给新创建的承接照片张数的权重的结果的空字典


# {'28': '0.00', '29': '0.29', '30': '0.29', '31': '0.00', '32': '0.14'}
# print(f"「写真枚数」の重み:{weight_photos_result}\n")


# イベントの重みを計算

# 计算事件权重的函数
def weight_event(weight_event_duration_value, weight_sns_value, weight_person_value, weight_place_value,
                 weight_photos_value):
    weight_event_value = weight_event_duration_value + weight_sns_value + weight_person_value + weight_place_value + weight_photos_value
    return weight_event_value


# 计算时间持续时间的函数
def get_weight_event_duration_value(number_value):
    if number_value in weight_event_duration_result:
        return weight_event_duration_result[number_value]
    else:
        return 0.0


# SNS
def get_weight_sns_value(number_value):
    for each_dic in total_list:
        if each_dic['number'] == number_value:
            if each_dic['SNS'] == 0:
                return 0.0
            elif each_dic['SNS'] == 1:
                return 1.0
            else:
                return 0.0


# 计算照片权重的函数
def get_weight_photos_value(number_value):
    if number_value in weight_photos_result:
        return weight_photos_result[number_value]
    else:
        return 0.0


# 给定一个int型的number的值，找出其对应的人物的权重
# def get_weight_person_value(number_value):
#     for each_dic in total_list:
#         if each_dic['number'] == number_value:
#             if each_dic['person'] == 'なし':
#                 return 0.0
#             elif each_dic['person'] in weight_person_result:
#                 return float(weight_person_result[each_dic['person']])
#             else:
#                 return 0.0
#     return None

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


# 给定一个int型的number的值，找出其对应的见过的天数的权重
def get_weight_metdays_value(number_value):
    for each_dic in total_list:
        if each_dic['number'] == number_value:
            if each_dic['person'] == 'なし':
                return 0.0
            elif each_dic['person'] in weight_person_result:
                return float(weight_metdays_result[each_dic['person']])
            else:
                return 0.0
    return None


# 给定一个int型的number的值，找出其对应的场所的权重
def get_weight_place_value(number_value):
    for each_dic in total_list:
        if each_dic['number'] == number_value:
            if each_dic['place'] in weight_place_result:
                return float(weight_place_result[each_dic['place']])
            else:
                return None


weight_event_result_dic = {}
weight_event_result_list = []

for each_dic in total_list:
    number_value = each_dic['number']
    # 事件持续时间的权重
    weight_event_duration_value = get_weight_event_duration_value(number_value)
    # SNS
    weight_sns_value = get_weight_sns_value(number_value)
    # 人物
    weight_person_value = get_weight_person_value(number_value)
    # 场所
    weight_place_value = get_weight_place_value(number_value)
    # 照片
    weight_photos_value = get_weight_photos_value(number_value)
    # 让以上权重相加，得出这个number对应的数字
    weight_event_result = weight_event(weight_event_duration_value, weight_sns_value, weight_person_value, weight_place_value,
                     weight_photos_value)
    # 将number和结果放入新的字典里
    weight_event_result_dic = {'number': each_dic['number'], 'weight_event': weight_event_result}
    weight_event_result_list.append(weight_event_result_dic)

print(f"イベントの重み:{weight_event_result_list}\n")


# # 将事件权重的结果分行输出
# for items in weight_event_result_list:
#     print(items['weight_event'])


# 计算三种排序

# 「思い出したい」順
def remember(weight_person_value, weight_place_value, weight_photos_value):
    remember_value = weight_person_value + weight_place_value + weight_photos_value
    return remember_value


weight_remember_dic = {}
weight_remember_list = []

for each_dic in total_list:
    number_value = each_dic['number']
    # 人物
    weight_person_value = get_weight_person_value(number_value)
    # 场所
    weight_place_value = get_weight_place_value(number_value)
    # 照片
    weight_photos_value = get_weight_photos_value(number_value)
    # 让以上权重相加，得出这个number对应的数字
    weight_remember_result = remember(weight_person_value, weight_place_value, weight_photos_value)
    # 将number和结果放入新的字典里
    weight_remember_dic = {'number': each_dic['number'], 'weight_remember': weight_remember_result}
    weight_remember_list.append(weight_remember_dic)

print(f"「思い出したい」順:{weight_remember_list}\n")


# 「思い出したい」順（new）
def remember_new(weight_sns_value, weight_place_value, weight_photos_value):
    remember_new_value = weight_sns_value + weight_place_value + weight_photos_value
    return remember_new_value


weight_remember_new_dic = {}
weight_remember_new_list = []

for each_dic in total_list:
    number_value = each_dic['number']
    # sns
    weight_sns_value = get_weight_sns_value(number_value)
    # 场所
    weight_place_value = get_weight_place_value(number_value)
    # 照片
    weight_photos_value = get_weight_photos_value(number_value)
    # 让以上权重相加，得出这个number对应的数字
    weight_remember_new_result =  remember(weight_sns_value, weight_place_value, weight_photos_value)
    # 将number和结果放入新的字典里
    weight_remember_new_dic = {'number': each_dic['number'], 'weight_remember(new)': weight_remember_new_result}
    weight_remember_new_list.append(weight_remember_new_dic)

print(f"「思い出したい」順(new):{weight_remember_new_list}\n")

# # 将「思い出したい」順的结果分行输出
# for items in weight_remember_list:
#     print(items['weight_remember_result'])

# 「重要」順 = 按照number输出場所的权重
weight_place_value_dic = {}
weight_place_value_list = []
for each_dic in total_list:
    number_value = each_dic['number']
    weight_place_value = get_weight_place_value(number_value)
    weight_place_value_dic = {'number': each_dic['number'], 'weight_place': weight_place_value}
    weight_place_value_list.append(weight_place_value_dic)

print(f"場所の重み(number順):{weight_place_value_list}\n")


# # 将「重要」順的结果分行输出
# for items in weight_place_value_list:
#     print(items['weight_place_result'])


# 「幸せな気分」順
def happy(weight_metdays_value, weight_place_value, weight_event_duration_value, weight_photos_value):
    happy_value = weight_metdays_value + weight_place_value + weight_event_duration_value + weight_photos_value
    return happy_value


weight_happy_dic = {}
weight_happy_list = []

for each_dic in total_list:
    number_value = each_dic['number']
    # 见过的天数的权重
    weight_metdays_value = get_weight_metdays_value(number_value)
    # 场所
    weight_place_value = get_weight_place_value(number_value)
    # 事件持续时间的权重
    weight_event_duration_value = get_weight_event_duration_value(number_value)
    # 照片
    weight_photos_value = get_weight_photos_value(number_value)
    # 让以上权重相加，得出这个number对应的数字
    weight_happy_result = happy(weight_metdays_value, weight_place_value, weight_event_duration_value, weight_photos_value)
    # 将number和结果放入新的字典里
    weight_happy_dic = {'number': each_dic['number'], 'weight_happy': weight_happy_result}
    weight_happy_list.append(weight_happy_dic)

print(f"「幸せな気分」順:{weight_happy_list}\n")


# # 将「幸せな気分」順的结果分行输出
# for items in weight_happy_list:
#     print(items['weight_happy'])


# 将已有的数据添加到新创建的表格里
# 将已有的计算结果，变成new_data = {'地址': ['北京', '上海', '杭州']}的形式

# 「会った日数」の重み
def get_weight_metdays_value(number_value):
    for each_dic in total_list:
        if each_dic['number'] == number_value:
            # 如果person栏是なし，那么就返回0.0
            if each_dic['person'] == 'なし':
                return 0.0
            # 如果person值在person_values人物列表中，且只有一个人，那么只输出这个人的person值
            elif each_dic['person'] in person_values and '、' not in each_dic['person']:
                return float(weight_metdays_result[each_dic['person']])
            # 如果person值在weight_person_result人物权重的字典中，且有一个人以上，那么输出这些人的权重的平均值
            else:
                metdays_values_list = each_dic['person'].split('、')
                # 输出: ['A', 'B', 'C', 'D', 'E']
                avg_list = []  # 计算人物有1个以上时，输出对应的平均值
                for everyone in metdays_values_list:
                    avg_list.append(float(weight_metdays_result[everyone]))

                average = sum(avg_list) / len(avg_list)
                return average


# 存放所有「会った日数」の重み的列表
metdays_list = []
new_metdays = {}
for number_value in range(1, len(total_list) + 1):
    metdays_list.append(get_weight_metdays_value(number_value))
    new_metdays = {'weight_person_metdays': metdays_list}

print(f"「会った日数」の重み:{new_metdays}\n")


# 「最後に会った日からの日数」の重み
def get_weight_number_of_days_since_last_since_value(number_value):
    for each_dic in total_list:
        if each_dic['number'] == number_value:
            # 如果person栏是なし，那么就返回0.0
            if each_dic['person'] == 'なし':
                return 0.0
            # 如果person值在person_values人物列表中，且只有一个人，那么只输出这个人的person值
            elif each_dic['person'] in person_values and '、' not in each_dic['person']:
                return float(weight_days_since_last_seen_result[each_dic['person']])
            # 如果person值在weight_person_result人物权重的字典中，且有一个人以上，那么输出这些人的权重的平均值
            else:
                number_of_days_since_last_since_values_list = each_dic['person'].split('、')
                # 输出: ['A', 'B', 'C', 'D', 'E']
                avg_list = []  # 计算人物有1个以上时，输出对应的平均值
                for everyone in number_of_days_since_last_since_values_list:
                    avg_list.append(float(weight_days_since_last_seen_result[everyone]))

                average = sum(avg_list) / len(avg_list)
                return average


# 存放所有「会った日数」の重み的列表
number_of_days_since_last_since_list = []
new_number_of_days_since_last_since = {}
for number_value in range(1, len(total_list) + 1):
    number_of_days_since_last_since_list.append(get_weight_number_of_days_since_last_since_value(number_value))
    new_number_of_days_since_last_since = {
        'weight_number_of_days_since_last_since': number_of_days_since_last_since_list}

print(f"「最後に会った日からの日数」の重み:{new_number_of_days_since_last_since}\n")

# 人物の重み

# 存放所有人物の重み的列表
person_list = []
new_person = {}
for number_value in range(1, len(total_list) + 1):
    person_list.append(get_weight_person_value(number_value))
    new_person = {'weight_person': person_list}

print(f"人物の重み:{new_person}\n")


# 「行った回数」の重み
def get_weight_times_of_visited_value(number_value):
    for each_dic in total_list:
        if each_dic['number'] == number_value:
            # 如果place值在list_place_values地名列表中，那么只输出这个地名的place值
            if each_dic['place'] in list_place_values:
                return float(weight_place_times_of_visited_result[each_dic['place']])
            else:
                return 0.0


# 存放所有「行った回数」の重み的列表
times_of_visited_list = []
new_times_of_visited = {}
for number_value in range(1, len(total_list) + 1):
    times_of_visited_list.append(get_weight_times_of_visited_value(number_value))
    new_times_of_visited = {'weight_times_of_visited': times_of_visited_list}

print(f"「行った回数」の重み:{new_times_of_visited}\n")


# 「距離」の重み
def get_weight_distance_value(number_value):
    for each_dic in total_list:
        if each_dic['number'] == number_value:
            # 如果place值在list_place_values地名列表中，那么只输出这个地名的place值
            if each_dic['place'] in list_place_values:
                return float(sorted_weight_relative_distance_dic[each_dic['place']])
            else:
                return 0.0


# 存放所有「距離」の重み的列表
distance_list = []
new_distance = {}
for number_value in range(1, len(total_list) + 1):
    distance_list.append(get_weight_distance_value(number_value))
    new_distance = {'weight_distance': distance_list}

print(f"「距離」の重み:{new_distance}\n")

# 場所の重み

# 存放所有場所の重み的列表
place_list = []
new_place = {}
for number_value in range(1, len(total_list) + 1):
    place_list.append(get_weight_place_value(number_value))
    new_place = {'weight_place': place_list}

print(f"場所の重み:{new_place}\n")

# 持続時間の重み

# 存放所有持続時間の重み的列表
event_duration_list = []
new_event_duration = {}
for number_value in range(1, len(total_list) + 1):
    event_duration_list.append(get_weight_event_duration_value(number_value))
    new_event_duration = {'weight_event_duration': event_duration_list}

print(f"持続時間の重み:{new_event_duration}\n")
value_count_7 = len(new_event_duration['weight_event_duration'])

# SNSの重み

# 存放所有SNSの重み的列表
sns_list = []
new_sns = {}
for number_value in range(1, len(total_list) + 1):
    sns_list.append(get_weight_sns_value(number_value))
    new_sns = {'weight_sns': sns_list}

print(f"SNSの重み:{new_sns}\n")
value_count_8 = len(new_sns['weight_sns'])

# 写真枚数の重み

# 存放所有写真枚数の重み的列表
photos_list = []
new_photos = {}
for number_value in range(1, len(total_list) + 1):
    photos_list.append(get_weight_photos_value(number_value))
    new_photos = {'weight_photos': photos_list}

print(f"写真枚数の重み:{new_photos}\n")
value_count_9 = len(new_photos['weight_photos'])

# イベントの重み

# 存放所有イベントの重み的列表
event_list = []
new_event = {}
event_list = [float(item['weight_event']) for item in weight_event_result_list]
new_event = {'weight_event': event_list}

print(f"イベントの重み:{new_event}\n")
value_count_10 = len(new_event['weight_event'])

print(f"列表中有 {value_count_10} 个值")

# 「思い出したい」順

# 存放所有「思い出したい」順的列表
remember_list = []
new_remember = {}
remember_list = [float(item['weight_remember']) for item in weight_remember_list]
new_remember = {'weight_remember': remember_list}

print(f"「思い出したい」順:{new_remember}\n")
value_count_11 = len(new_remember['weight_remember'])

# 「重要」順

# 存放所有「重要」順的列表
# 「重要」順 = 按照number输出場所的权重
new_important = {'weight_important': place_list}

print(f"「重要」順:{new_important}\n")
value_count_12 = len(new_important['weight_important'])

# 「幸せな気分」順

# 存放所有「幸せな気分」順的列表
happy_list = []
new_happy = {}
happy_list = [float(item['weight_happy']) for item in weight_happy_list]
new_happy = {'weight_happy': happy_list}

print(f"「幸せな気分」順:{new_happy}\n")
value_count_13 = len(new_happy['weight_happy'])

# 「思い出したい」順(new)

# 存放所有「思い出したい」順(new)的列表
remember_new_list = []
new_remember_new = {}
remember_new_list = [float(item['weight_remember(new)']) for item in weight_remember_new_list]
new_remember_new = {'weight_remember(new)': remember_new_list}

print(f"「思い出したい」順(new):{new_remember_new}\n")
value_count_14 = len(new_remember_new['weight_remember(new)'])

# 指定已有的CSV文件路径
filename_save = '/Users/wangsihan/Downloads/system_data/Weight_new_remember/3/Weight_wang.csv'

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
        # 「会った日数」の重み
        metdays = new_metdays['weight_person_metdays'][i]
        row['weight_person_metdays'] = metdays
        # 「最後に会った日からの日数」の重み
        number_of_days_since_last_since = new_number_of_days_since_last_since['weight_number_of_days_since_last_since'][
            i]
        row['weight_number_of_days_since_last_since'] = number_of_days_since_last_since
        # 「人物」の重み
        person = new_person['weight_person'][i]
        row['weight_person'] = person
        # 「行った回数」の重み
        times_of_visited = new_times_of_visited['weight_times_of_visited'][i]
        row['weight_times_of_visited'] = times_of_visited
        # 「距離」の重み
        distance = new_distance['weight_distance'][i]
        row['weight_distance'] = distance
        # 場所の重み
        place = new_place['weight_place'][i]
        row['weight_place'] = place
        # 持続時間の重み
        event_duration = new_event_duration['weight_event_duration'][i]
        row['weight_event_duration'] = event_duration
        # SNSの重み
        sns = new_sns['weight_sns'][i]
        row['weight_sns'] = sns
        # 写真枚数の重み
        photos = new_photos['weight_photos'][i]
        row['weight_photos'] = photos
        # イベントの重み
        event = new_event['weight_event'][i]
        row['weight_event'] = event
        # 「思い出したい」順
        remember = new_remember['weight_remember'][i]
        row['weight_remember'] = remember
        # 「重要」順
        important = new_important['weight_important'][i]
        row['weight_important'] = important
        # 「幸せな気分」順
        happy = new_happy['weight_happy'][i]
        row['weight_happy'] = happy
        # 「思い出したい」順(new)
        remember_new = new_remember_new['weight_remember(new)'][i]
        row['weight_remember(new)'] = remember_new

    # 将合并后的数据写回CSV文件
    with open(filename_save, mode='w', newline='') as file:
        fieldnames = existing_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(existing_data)
