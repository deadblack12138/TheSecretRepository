from rsa import encrpt
import re
import requests
import json
from bs4 import BeautifulSoup

login_url = "http://114.55.35.72/Login/CheckLogin"
kkcj_url = 'http://114.55.35.72/Tschedule/C6Cjgl/GetKccjResult'
tjfx_url = 'http://114.55.35.72/Tschedule/C6Cjgl/GetXskccjResult'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'}

session = requests.Session()


def login(name, password):
    """
    向登录网址post，返回登录状态 (在调用jxgl.py下的其他程序前先调用它)
    :param name: 学号
    :param password: 密码
    :return: 登录状态result
    """
    name = encrpt(str(name).strip())
    password = str(password).strip()
    login_data = {'username': name,
                  'password': password,
                  'code': '',
                  'isautologin': 0}
    r = session.post(login_url, headers=headers, data=login_data, timeout=5)
    result = json.loads(r.text)["message"]
    return result


def getKccj():
    """
    获取课程成绩，并写入文件 'all_result.txt'
        xq_list: 学期列表
        kc_name_list: 课程名字列表
        kc_info_list: 课程信息列表
    :return: None
    """
    r = session.post(kkcj_url, headers=headers, data={'order': 'zxjxjhh desc,kch'})

    html = r.text
    soup = BeautifulSoup(html, 'html.parser')

    # 定义‘学期信息’和‘单科课程成绩信息’正则表达式对象
    pat_xq = re.compile(r'<td colspan="8">(.*?)</td>')
    pat_kc_name = re.compile(r'<td tyle="vertical-align:middle; ">(.*?)</td>')
    pat_kc_info = re.compile(r'<td style="vertical-align:middle; ">(.*?)</td>')
    xq_list = []
    kc_name_list = []
    kc_info_list = []
    sub_kc_name_list = []
    sub_kc_info_list = []

    for tr in soup.find('table').children:
        # 录入课程name和课程info列表
        match_kc_info = pat_kc_info.findall(str(tr))
        match_kc_name = pat_kc_name.findall(str(tr))
        if match_kc_name:
            sub_kc_name_list.append(match_kc_name[0])
        if match_kc_info:
            # del前三个不重要的信息
            del match_kc_info[0], match_kc_info[0], match_kc_info[0]
            sub_kc_info_list.append(match_kc_info)
            continue
        # 录入学期列表
        match_xq = pat_xq.findall(str(tr))
        if match_xq:
            xq_list.append(match_xq)
            kc_name_list.append(sub_kc_name_list)
            kc_info_list.append(sub_kc_info_list)
            sub_kc_name_list = []
            sub_kc_info_list = []

    # 删除第一个的空列表,加入未加入的子列表
    del kc_name_list[0], kc_info_list[0]
    kc_name_list.append(sub_kc_name_list)
    kc_info_list.append(sub_kc_info_list)

    for i in range(len(kc_name_list)):
        for j in range(len(kc_name_list[i])):
            kc_name_list[i][j] = kc_name_list[i][j].replace(' ', '　').replace('(', '（').replace(')', '）')

    # xq_list: 学期列表
    # kc_name_list: 课程名字列表
    # kc_info_list: 课程信息列表
    with open('user/all_result.txt', 'w') as f:
        tplt = "{0:{4}<13}\t{1:{4}<10}\t{2:{4}<10}\t{3:{4}<10}\t\n"
        for i in range(len(xq_list)):
            # 打印学期
            f.write('\t\t\t\t' + xq_list[i][0].center(20).strip() + '\n\n')
            f.write(tplt.format("课程名", "学分", "课程属性", "成绩", chr(12288)))
            for j in range(len(kc_name_list[i])):
                f.write(tplt.format(str(kc_name_list[i][j]), kc_info_list[i][j][0], kc_info_list[i][j][1], kc_info_list[i][j][3], chr(12288)))
            f.write('\n' + '——'*60 + '\n')
        f.write('\n')


def getTjfx():
    """
    获取成绩统计分析，追加到 'all_result.txt'
    :return: None
    """
    r = session.post(tjfx_url, headers=headers, data={'order': 'zxjxjhh desc,kch'})
    html = r.text
    pat_name = re.compile(r'<div class="profile-info-name">(.*?)</div>')
    pat_value = re.compile(r'<div class="profile-info-value"> <span>(.*?)</span></div>')
    info_name = pat_name.findall(html)
    info_value = pat_value.findall(html)
    info_num = [3, 12, 4, 13, 5, 14, 6, 15, 7]

    with open('user/all_result.txt', 'a') as f:
        for i in range(3):
            for j in range(3):
                name = info_name[info_num[3 * j + i]].replace(' ', '')
                value = info_value[info_num[3 * j + i]].replace(' ', '')
                f.write('{0:{1}<15}\t'.format(name+value, chr(12288)))
            f.write('\n')
