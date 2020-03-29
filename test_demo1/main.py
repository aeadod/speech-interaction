# -*- coding: utf-8 -*-

from test_demo import input_record, recognition_speech, tuling_robot

from test_demo import compound_speech, output_redio

import requests
import string
import time
import hashlib
import json

# 存放的文件名称
file_path = "record-audio.wav"
# 百度需要的参数
APP_ID = '16492415'
API_KEY = 'EgQpNVHvlrb8j31nfd9jtViB'
SECRET_KEY = 'ARwZG5bGRpoZQwqHLuOyqlMNq3xUtKjD'
# 图灵需要的参数
TULING_KEY = '2e960b3fb0ed4aa599b461b3fc03e25a'

# 先调用录音函数 (Speech input)
input_record.record(file_path)

# 语音转成文字的内容 (Speech to text)
input_message = recognition_speech.voice2text(APP_ID, API_KEY, SECRET_KEY, file_path)
print(input_message)


# init
api_url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
my_appid ='20190709000316223'
cyber = 'l6ngE7GjtdvRESJqQzDL'
lower_case = list(string.ascii_lowercase)


def requests_for_dst(word):
    # init salt and final_sign
    salt = str(time.time())[:10]
    final_sign = str(my_appid) + word + salt + cyber
    final_sign = hashlib.md5(final_sign.encode("utf-8")).hexdigest()
    paramas = {
            'q': word,
            'from': 'zh',
            'to': 'en',
            'appid': '%s' % my_appid,
            'salt': '%s' % salt,
            'sign': '%s' % final_sign
        }
    my_url = api_url + '?appid=' + str(
        my_appid) + '&q=' + word + '&from=' + 'zh' + '&to=' + 'en' + '&salt=' + salt + '&sign=' + final_sign
    response = requests.get(api_url, params=paramas).content
    content = str(response, encoding="utf-8")
    json_reads = json.loads(content)
    print(json_reads['trans_result'][0]['dst'])

word = str(input_message)
requests_for_dst(word)