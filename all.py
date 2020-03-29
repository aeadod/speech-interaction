# -*- coding: utf-8 -*-
# 树莓派
from pyaudio import PyAudio, paInt16
import numpy as np
from datetime import datetime
import wave
import time
import requests#导入requests库
import urllib,urllib.request, pycurl
import base64
import json
import os
import sys
from imp import reload

# 调用电脑API生成语音交互
import speech
import win32api
import os
import sys
import time
import win32con


#百度语音合成
import urllib.request
import requests#导入requests库
import urllib
import json
import base64


reload(sys)

#sys.setdefaultencoding( "utf-8" )
#一些全局变量
save_count = 0
save_buffer = []
t = 0
sum = 0
time_flag = 0
flag_num = 0
filename = ''
duihua = '1'
def getHtml(url):
        html= requests.get(url)
       # html.encoding = 'utf-8'#防止中文乱码

        return html.text
def get_token():
    apiKey = "AxXDYEN27Ks9XHocsGmCEdPm"
    secretKey = "61cd52759f4d704d91c155a22ff7183d"
    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;
    res = requests.get(auth_url)
    #res.encoding = 'utf-8'#防止中文乱码
    #print (res.text)
    return json.loads(res.text)['access_token']
def dump_res(buf):#输出百度语音识别的结果
    global duihua
    #print ("字符串类型")
    #print (buf)
    a = eval(buf)
    #print (type(a))
    if a['err_msg']=='success.':
        #print (a['result'][0]）#终于搞定了，在这里可以输出，返回的语句
        duihua = a['result'][0]
        print ("我："+duihua)
def use_cloud(token):#进行合成
    fp = wave.open(filename, 'rb')
    nf = fp.getnframes()
    f_len = nf * 2
    audio_data = fp.readframes(nf)
    cuid = "9120612" #产品id
    srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token
    http_header = ['Content-Type: audio/pcm; rate=8000','Content-Length: %d' % f_len]
    c = pycurl.Curl()
    c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode
    #c.setopt(c.RETURNTRANSFER, 1)
    c.setopt(c.HTTPHEADER, http_header)#must be list, not dict
    c.setopt(c.POST, 1)
    c.setopt(c.CONNECTTIMEOUT, 30)
    c.setopt(c.TIMEOUT, 30)
    c.setopt(c.WRITEFUNCTION, dump_res)
    c.setopt(c.POSTFIELDS, audio_data)
    c.setopt(c.POSTFIELDSIZE, f_len)
    c.perform() #pycurl.perform() has no return val
# 将data中的数据保存到名为filename的WAV文件中
def save_wave_file(filename, data):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes(b"".join(data))
    wf.close()



#百度语音合成---------------------------------------
class BaiduRest:
    def __init__(self, cu_id, api_key, api_secert):
        # token认证的url
        self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        # 语音合成的resturl
        self.getvoice_url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
        # 语音识别的resturl
        self.upvoice_url = 'http://vop.baidu.com/server_api'

        self.cu_id = cu_id
        self.getToken(api_key, api_secert)
        return

    def getToken(self, api_key, api_secert):
        # 1.获取token
        token_url = self.token_url % (api_key,api_secert)

        r_str = requests.get(token_url).text
        token_data = json.loads(r_str)
        self.token_str = token_data['access_token']
        pass

    def getVoice(self, text, filename):
        # 2. 向Rest接口提交数据
        get_url = self.getvoice_url % (urllib.parse.quote(text), self.cu_id, self.token_str)

        voice_data = urllib.request.urlopen(get_url).read()
        # 3.处理返回数据
        voice_fp = open(filename,'wb+')
        voice_fp.write(voice_data)
        voice_fp.close()
        pass

#百度语音合成--------------------------------------


NUM_SAMPLES = 2000# pyAudio内部缓存的块的大小
SAMPLING_RATE = 8000# 取样频率
LEVEL = 1500# 声音保存的阈值
COUNT_NUM = 20# NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
SAVE_LENGTH = 8# 声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样
exception_on_overflow=False
# 开启声音输入ｐｙａｕｄｉｏ对象
pa = PyAudio()
stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True,frames_per_buffer=NUM_SAMPLES)
token = get_token()#获取ｔｏｋｅｎ
key = '35ff2856b55e4a7f9eeb86e3437e23fe'
api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='

#百度语音合成--------------------------------------
if __name__ == "__main__":
    # 我的api_key,供大家测试用，在实际工程中请换成自己申请的应用的key和secert
    api_key = "SrhYKqzl3SE1URnAEuZ0FKdT" 
    api_secert = "hGqeCkaMPb0ELMqtRGc2VjWdmjo7T89d"
    # 初始化
    bdr = BaiduRest("test_python", api_key, api_secert)
    # 将字符串语音合成并保存为out.mp3
#百度语音合成--------------------------------------

while(True):
    # 读入NUM_SAMPLES个取样
    string_audio_data = stream.read(NUM_SAMPLES,False);
    # 将读入的数据转换为数组
    audio_data = np.fromstring(string_audio_data, dtype=np.short)
    # 计算大于LEVEL的取样的个数
    large_sample_count = np.sum( audio_data > LEVEL )
    temp = np.max(audio_data)
    if temp > 2000 and t == 0:
        t = 1#开启录音
        print ("---------主人我在听你说！（5S）----------")
        begin = time.time()
        # print (temp)
    if t:
        #print (np.max(audio_data))
        if np.max(audio_data)<1000:
           sum += 1
           # print (sum)
        end = time.time()
        if end-begin>5:
              time_flag = 1
        # print ("五秒到了，准备结束")
        # 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
        if large_sample_count > COUNT_NUM:
            save_count = SAVE_LENGTH
        else:
             save_count -= 1
        if save_count < 0:
            save_count = 0
        if save_count > 0:
# 将要保存的数据存放到save_buffer中
                save_buffer.append(string_audio_data )
        else:
        # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
        #if  time_flag:
                if len(save_buffer) > 0 or time_flag:
                        #filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".wav"#原本是用时间做名字
                        filename = str(flag_num)+".wav"
                        flag_num += 1
                        save_wave_file(filename, save_buffer)
                        save_buffer = []
                        t = 0
                        sum =0
                        time_flag = 0
                        #  print (filename, "保存成功正在进行语音识别")
                        use_cloud(token)
                        #   print (duihua)
                        info = duihua
                        duihua = ""
                        request = api + str(info)
                        response = getHtml(request)
                        #  print ( "-----1-----")
                        dic_json = json.loads(response)
                        a = dic_json['text']
                        unicodestring = a
                        # 将Unicode转化为普通Python字符串："encode"
                        utf8string = unicodestring.encode("utf-8")
                        print ("科塔娜："+str(a))

                         # 将字符串语音合成并保存为out.mp3
                        bdr.getVoice(str(a), "out1.mp3")

    
                        # 电脑说话
                        #speech.say(str(a))

                        os.system('out1.mp3')
                        
                        url = "http://tsn.baidu.com/text2audio?tex="+dic_json['text']+"&lan=zh&per=0&pit=1&spd=7&cuid=7519663&ctp=1&tok=25.41bf315625c68b3e947c49b90788532d.315360000.1798261651.282335-9120612"
                        os.system('mpg123 "%s"'%(url))
