from flask import Flask, jsonify, request, make_response, render_template
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from python.kafka.src.calc_dispy import calc
import asyncio, json
from aiohttp import ClientSession

executor = ThreadPoolExecutor(max_workers=2)
app = Flask(__name__)
app.config.update(DEBUG=True)
weather_list = []


def get_citys():
    citys = ["上海", "北京", "北京市", "朝阳", "朝阳区", "海淀", "元谋", "南充", "且末", "荔波", "佛山", "庆阳", "保山", "二连浩特", "丽江", "北京", "锦州",
             "塔城",
             "大庆", "西安", "芷江", "西宁", "喀什", "三亚", "恩施", "三女河", "连云港", "长春", "牡丹江", "伊春", "山海关", "鸡西", "昭通", "达州", "海淀",
             "宜宾",
             "运城", "安阳", "酒泉", "通辽", "济宁", "重庆", "延吉", "黑河", "无锡", "榆林", "九江", "兴城", "乌海", "邢台", "阿克苏", "厦门", "晋江",
             "黎平", "昆明",
             "深圳", "宁波", "文山", "临沂", "伊宁", "大理", "揭阳", "邯郸", "南阳", "大同", "腾冲", "银川", "呼和浩特", "合肥", "乌兰浩特", "襄樊", "柳州",
             "南宁",
             "长海", "蓬莱", "缨芬河", "满洲里", "成都", "安顺", "珠海", "库尔勒", "通化", "兴宁", "长沙", "依兰", "西双版纳", "温州", "万县", "延安", "上海",
             "安康",
             "潍坊", "广汉", "武汉", "佳木斯", "博尔塔拉", "长治", "湛江", "哈尔滨", "思茅", "富蕴", "鞍山", "兴义", "鄂尔多斯", "天津", "常德", "杭州", "朝阳",
             "拉萨",
             "长白山", "烟台", "福州", "梁平", "泸州", "芒市", "临沧", "安庆", "保安营", "济南", "蚌埠", "石家庄", "南昌", "张家界", "吉林", "吉安", "海拉尔",
             "遵义",
             "朝阳区", "铜仁", "南通", "广州", "太原", "阜阳", "齐齐哈尔", "大连", "景德镇", "徐州", "贵阳", "苏州", "东营", "常州", "丹东", "梧州", "永州",
             "衢州",
             "黄山", "惠州", "新源", "阿尔山", "百色", "兰州", "荆州", "梅州", "和田", "扬州", "海口", "林芝", "青岛", "哈密", "库车", "洛阳", "嘉峪关",
             "沈阳", "绵阳",
             "克拉玛依", "玉树", "西昌", "汉中", "赣州", "威海", "迪庆", "盐城", "武夷山", "阿勒泰", "乌鲁木齐", "庐山", "秦皇岛", "格尔木", "衡阳", "桂林",
             "义乌", "连城",
             "井冈山", "宜昌", "昌都", "赤峰", "九寨沟", "锡林浩特", "黄岩", "敦煌", "南京", "舟山", "郑州", "北海", "淮安", "固原", "包头", "广元", "康定",
             "万县",
             "三亚", "三女河", "上海", "且末", "东营", "临沂", "临沧", "丹东", "丽江", "义乌", "乌兰浩特", "乌海", "乌鲁木齐", "九寨沟", "九江", "二连浩特",
             "井冈山",
             "伊宁", "伊春", "佛山", "佳木斯", "依兰", "保安营", "保山", "元谋", "克拉玛依", "兰州", "兴义", "兴城", "兴宁", "包头", "北京", "北海", "南京",
             "南充",
             "南宁", "南昌", "南通", "南阳", "博尔塔拉", "厦门", "合肥", "吉安", "吉林", "呼和浩特", "和田", "哈密", "哈尔滨", "喀什", "嘉峪关", "固原", "塔城",
             "大同",
             "大庆", "大理", "大连", "天津", "太原", "威海", "宁波", "安庆", "安康", "安阳", "安顺", "宜宾", "宜昌", "富蕴", "山海关", "常州", "常德",
             "广元", "广州",
             "广汉", "庆阳", "庐山", "库尔勒", "库车", "康定", "延吉", "延安", "张家界", "徐州", "思茅", "恩施", "惠州", "成都", "扬州", "拉萨", "揭阳",
             "敦煌", "文山",
             "新源", "无锡", "昆明", "昌都", "昭通", "晋江", "景德镇", "朝阳", "杭州", "林芝", "柳州", "格尔木", "桂林", "梁平", "梅州", "梧州", "榆林",
             "武夷山",
             "武汉", "永州", "汉中", "沈阳", "泸州", "洛阳", "济南", "济宁", "海口", "海拉尔", "淮安", "深圳", "温州", "湛江", "满洲里", "潍坊", "烟台",
             "牡丹江",
             "玉树", "珠海", "百色", "盐城", "石家庄", "福州", "秦皇岛", "绵阳", "缨芬河", "腾冲", "舟山", "芒市", "芷江", "苏州", "荆州", "荔波", "蓬莱",
             "蚌埠",
             "衡阳", "衢州", "襄樊", "西双版纳", "西宁", "西安", "西昌", "贵阳", "赣州", "赤峰", "达州", "运城", "连云港", "连城", "迪庆", "通化", "通辽",
             "遵义",
             "邢台", "邯郸", "郑州", "鄂尔多斯", "酒泉", "重庆", "铜仁", "银川", "锡林浩特", "锦州", "长春", "长沙", "长治", "长海", "长白山", "阜阳", "阿克苏",
             "阿勒泰",
             "阿尔山", "青岛", "鞍山", "鸡西", "黄山", "黄岩", "黎平", "黑河", "齐齐哈尔"]
    return citys


async def get_web_weather(city):
    async with ClientSession() as session:
        async with session.get("http://wthrcdn.etouch.cn/weather_mini?city=" + city) as response:
            response = await response.read()
            print(response.decode("utf-8"))
            weatherData = json.loads(response.decode("utf-8"))

            weather_dict = dict()
            if weatherData["status"] == 1000:
                weather_dict['city'] = city
                weather_dict['high'] = weatherData['data']['forecast'][0]['high']
                weather_dict['low'] = weatherData['data']['forecast'][0]['low']
                weather_dict['type'] = weatherData['data']['forecast'][0]['type']
                weather_dict['fengxiang'] = weatherData['data']['forecast'][0]['fengxiang']
                weather_dict['ganmao'] = weatherData['data']['ganmao']
            weather_list.append(weather_dict)

def get_city_weather(city):
    dt = datetime.now()
    print(dt.strftime("%H:%M:%S %f"))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_web_weather(city=city))

@app.route('/test1/', methods=['GET'])
def test1():
    print("===============")
    citys = get_citys()
    for city in citys:
        get_city_weather(city)
    hot_city,cold_city = calc(weather_list)
    return make_response(hot_city), 201


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=5000)
