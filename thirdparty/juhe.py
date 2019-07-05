import json
import requests

def weather(cityname,areaname=None):
    key = '09a908c3a6264edfb6969d569e014d54'
    api = 'https://free-api.heweather.net/s6/weather/now'
    if areaname:
        cityname = areaname[:-1] + ',' + cityname[:-1]
    params = 'location=%s&key=%s' % (cityname,key)
    url = api +'?' + params
    print(url)
    response = requests.get(url=url)
    json_data = json.loads(response.text)
    print(json_data)
    data = json_data['HeWeather6'][0]
    result = data['now']
    response = dict()
    response['city'] = data['basic']['location']
    response['temperature'] = result['tmp']
    response['wind_direction'] = result['wind_dir']
    response['wind_strength'] = result['wind_sc']
    response['humidity'] = result['hum']
    response['time'] = data['update']['utc']
    response['city_info'] = dict()
    response['city_info']['province'] = data['basic']['admin_area']
    response['city_info']['city'] = data['basic']['parent_city']
    response['city_info']['area'] = data['basic']['location']

    return response


def stock(market,code):
    key = '69f870ef652bd9015e355a0199a0ef71'
    api = 'http://web.juhe.cn:8080/finance/stock/hs?'
    gid = market + code
    params = 'gid=%s&key=%s' % (gid,key)
    url = api + params
    request_data = requests.get(url=url)
    json_data = json.loads(request_data.text)
    result = json_data['result'][0]['data']
    response = {
        'name' : result['name'],
        'increPer' : result['increPer'],
        'start_price' : result['todayStartPri'],
        'now_price' : result['nowPri'],
        'today_max' : result['todayMax'],
        'today_min' : result['todayMin'],
        'date' : result['date'],
        'time' : result['time']
    }
    response['is_rising'] = result.get('nowPri') >= result.get('todayStartPri')
    print('nowPri:',result.get('nowPri'),'todayStartPri',result.get('todayStartPri'))
    print('is_rising:',response['is_rising'])
    sub = abs(float(result.get('nowPri')) - float(result.get('todayStartPri')))  # 差值
    response['sub'] = float('%.3f' % sub)
    return response

def constellation(cons_name):
    '''
    :param cons_name:星座名字
    :return: 今天运势
    '''
    key = '97cc392cada91655cc31bf5b23320a7f'
    api = 'http://web.juhe.cn:8080/constellation/getAll'
    types = ['today','tomorrow','week','month','year']
    params = 'consName=%s&type=%s&key=%s' % (cons_name,types[0],key)
    url = api + '?' + params
    request_data = requests.get(url=url)
    json_data = json.loads(request_data.text)
    response = {
        'name':json_data['name'],
        'text':json_data['summary']
    }
    return response


if __name__ == '__main__':
    a = weather('深圳')
    print('*'*30,a)
    b = stock('sh','000001')
    print('*'*30,b)