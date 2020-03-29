# -*- coding: utf-8 -*-


"""
获取对话的内容
"""

import requests
import json


def answer(message, key):
    url = 'http://www.tuling123.com/openapi/api?key='+key+'&info='+message
    res = requests.get(url)
    res.encoding = 'utf-8'
    answer_message = json.loads(res.text)

    return answer_message
