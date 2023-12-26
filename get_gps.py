import requests
import googlemaps
from datetime import datetime
from geopy import distance

# 使用您的API密钥替换YOUR_API_KEY
api_key = "AIzaSyB4TZOkrHXKvVfNHWjggfI_1db7ApsPCnA"


def get_gps(address):  # # 日文地址字符串

    # 通过HTTP GET请求向Google Maps Geocoding API发送查询
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url)

    # 解析响应的JSON数据
    data = response.json()

    # 提取经度和纬度信息
    if len(data['results']) > 0:
        latitude = data['results'][0]['geometry']['location']['lat']
        longitude = data['results'][0]['geometry']['location']['lng']
    else:
        latitude = None
        longitude = None

    # 打印GPS坐标
    return (latitude, longitude)

# 计算两地点之间的相对距离的函数
# def calculate_relative_distance(home, address):
#     try:
#         url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={home}&destinations={address}&key={api_key}"
#
#         response = requests.get(url).json()
#         print(response)  # 打印出请求返回的JSON数据，检查是否包含需要的字段
#         distance = response["rows"][0]["elements"][0]["distance"]["value"] / 1000  # 返回值是米，除以1000转换成公里
#         return distance  # 输出两个城市之间的距离（单位：公里）
#     except Exception as e:
#         print(f"Error: {e}")
#         return None

# 计算两地点之间的相对距离的函数
def calculate_relative_distance(home, address):
    # 创建一个Google Maps API客户端
    gmaps = googlemaps.Client(key='AIzaSyB4TZOkrHXKvVfNHWjggfI_1db7ApsPCnA')

    try:
        # 调用distance_matrix()函数获取距离矩阵
        result = gmaps.distance_matrix(home, address, mode='driving', units='metric',
                                       departure_time=datetime.now())

        # 从结果中提取距离信息
        distance_in_meters = result['rows'][0]['elements'][0]['distance']['value']
        distance_in_kilometers = distance_in_meters / 1000
        distance = float(distance_in_kilometers)

        # 返回结果
        return distance

    except Exception as e:
        print(f"Error: {e}！")
        return None



def calculate_relative_distance_geopy(home, address):
    # 计算两点之间的距离
    distance_in_meters = distance.distance(home, address).m
    distance_in_kilometers = distance_in_meters / 1000
    distance = float(distance_in_kilometers)

    # 返回结果
    return distance

