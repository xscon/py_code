#百度通用翻译API,不包含词典、tts语音合成等资源，如有相关需求请联系translate_api@baidu.com
# coding=utf-8

import http.client
import hashlib
import re
import urllib
import random
import json
import os


def trans_file_name(q):
    """

    @param q: 英文
    @return: 中文
    """
    appid = '20200310000395663'  # 填写你的appid
    secretKey = 'RqooC86glGM9yDZjBHot'  # 填写你的密钥

    httpClient = None
    myurl = '/api/trans/vip/translate'

    fromLang = 'auto'   #原文语种
    toLang = 'zh'   #译文语种
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
    salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        eng = result['trans_result'][0]['src']
        chn = result['trans_result'][0]['dst']
        return eng,chn

    except Exception as e:
        print (e)
    finally:
        if httpClient:
            httpClient.close()


def show_file_name(path):
    list_dir = os.listdir(path)
    for filename in list_dir:
        filepath = os.path.join(path, filename)
        eng_filename = ' '.join(re.findall(r'[a-zA-Z]+', filename)[:-1])
        print(eng_filename)
        if eng_filename:
            en, chn = trans_file_name(filename)
            chn_path = os.path.join(path, chn + '.mp4')
            os.rename(filepath, chn_path)
        else:
            print(filename)




if __name__ == '__main__':
    # e,c = trans_file_name('chinese')
    show_file_name(r'C:\Users\Frank\Desktop\1')
