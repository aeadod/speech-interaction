from test_demo import input_record, recognition_speech
import speech_recognition as sr
import requests
import string
import hashlib
import json
import time
import pyttsx3

a = input("Please choose C(Chinese) or E(English?):")
print(a)

if a == 'E' :

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        print( r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("error; {0}".format(e))

    # init
    api_url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
    my_appid = '20190709000316223'
    cyber = 'l6ngE7GjtdvRESJqQzDL'
    lower_case = list(string.ascii_lowercase)


    def requests_for_dst(word):

        salt = str(time.time())[:10]
        final_sign = str(my_appid) + word + salt + cyber
        final_sign = hashlib.md5(final_sign.encode("utf-8")).hexdigest()


        paramas = {
            'q': word,
            'from': 'en',
            'to': 'zh',
            'appid': '%s' % my_appid,
            'salt': '%s' % salt,
            'sign': '%s' % final_sign
        }
        my_url = api_url + '?appid=' + str(
            my_appid) + '&q=' + word + '&from=' + 'en' + '&to=' + 'zh' + '&salt=' + salt + '&sign=' + final_sign

        response = requests.get(api_url, params=paramas).content
        content = str(response, encoding="utf-8")
        json_reads = json.loads(content)
        chi=json_reads['trans_result'][0]['dst']
        print(chi)
        engine=pyttsx3.init()
        engine.say(chi)
        engine.runAndWait()

    word = r.recognize_google(audio)
    requests_for_dst(word)


elif a == 'C' :

    file_path = "record-audio.wav"
    APP_ID = '16827721'
    API_KEY = 'RihNGLWOeendn2qvYbPmOAUS'
    SECRET_KEY = 'O7QnPsKsnGsRMvf49wzSkaUnUB38E6zj'


    input_record.record(file_path)
    input_message = recognition_speech.voice2text(APP_ID, API_KEY, SECRET_KEY, file_path)
    print(input_message)


    api_url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
    my_appid = '20190709000316223'
    cyber = 'l6ngE7GjtdvRESJqQzDL'
    lower_case = list(string.ascii_lowercase)


    def requests_for_dst(word):

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

else:
    print("Please enter a vaild character.")
