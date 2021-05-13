import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, dump

# 한국산업인력공단_국가자격취득자 현황 조회 서비스
# T: 3408개 for pageNo in range(1, 70)
# C: 677개 for pageNo in range(1, 15):
# W: 295개 for pageNo in range(1, 7):

# 없는 종목코드 데이터 삽입 방지
# csv 파일 읽기
import csv

check = []
with open('certificate.csv', 'r', encoding='utf-8') as f:
    rdr = csv.reader(f)
    for certi_code in rdr:
        check = certi_code

statistics = {} # statistics table에 담을 data

# 자격구분 코드로 인한 idx 3회 순환.
for year in range(2016, 2021):
    for idx in range(3):
        print("한 자격구분 코드 완료")
        # 자격구분 코드 T
        if idx == 0:
            qualgbCd = "T"
            for pageNo in range(1, 70):

                url = "http://apis.data.go.kr/B490007/qualAcquPtcond/getQualAcquPtcond?numOfRows=50&pageNo={}&dataFormat=xml&acquYy={}&qualgbCd={}&serviceKey=".format(pageNo, year, qualgbCd)
                key = "pg48D3FYflY8PkE9Vhd%2FkHGfCpn6iggpyOE7SJfTfGmA%2Bjw%2FpOka%2B0o2gw6CWR0XvRmCi62UbbJfxqQ8UDBCEQ%3D%3D"
                url += key

                response = requests.get(url).content
                soup = BeautifulSoup(response, 'html.parser')
                doc = ET.fromstring(str(soup))
                iter_elem = doc.iter(tag="item")

                for elem in iter_elem:
                    statistic = {}
                    check_cd = elem.find('jmcd').text
                    if check_cd not in check:
                        continue
                    # 데이터 리스트에 담기.
                    agegrupcd = elem.find('agegrupcd').text
                    gendercd = elem.find('gendercd').text
                    if check_cd+agegrupcd+gendercd in statistics:
                        statistics[check_cd+agegrupcd+gendercd]['acqucnt'] += int(elem.find('acqucnt').text)
                    else:
                        statistic['agegrupnm'] = elem.find('agegrupnm').text
                        statistic['gendernm'] = elem.find('gendernm').text
                        statistic['acqucnt'] = int(elem.find('acqucnt').text)
                        statistic['jmcd'] = elem.find('jmcd').text
                        statistics[check_cd+agegrupcd+gendercd] = (statistic)
        # 자격 구분 코드 C
        elif idx == 1:
            qualgbCd = "C"
            for pageNo in range(1, 15):

                url = "http://apis.data.go.kr/B490007/qualAcquPtcond/getQualAcquPtcond?numOfRows=50&pageNo={}&dataFormat=xml&acquYy=2021&qualgbCd={}&serviceKey=".format(pageNo, qualgbCd)
                key = "pg48D3FYflY8PkE9Vhd%2FkHGfCpn6iggpyOE7SJfTfGmA%2Bjw%2FpOka%2B0o2gw6CWR0XvRmCi62UbbJfxqQ8UDBCEQ%3D%3D"
                url += key

                response = requests.get(url).content
                soup = BeautifulSoup(response, 'html.parser')
                doc = ET.fromstring(str(soup))
                iter_elem = doc.iter(tag="item")
                for elem in iter_elem:
                    statistic = {}
                    check_cd = elem.find('jmcd').text
                    if check_cd not in check:
                        continue
                    # 데이터 리스트에 담기.
                    agegrupcd = elem.find('agegrupcd').text
                    gendercd = elem.find('gendercd').text
                    if check_cd+agegrupcd+gendercd in statistics:
                        statistics[check_cd+agegrupcd+gendercd]['acqucnt'] += int(elem.find('acqucnt').text)
                    else:
                        statistic['agegrupnm'] = elem.find('agegrupnm').text
                        statistic['gendernm'] = elem.find('gendernm').text
                        statistic['acqucnt'] = int(elem.find('acqucnt').text)
                        statistic['jmcd'] = elem.find('jmcd').text
                        statistics[check_cd+agegrupcd+gendercd] = (statistic)
        # 자격 구분 코드 W
        elif idx == 2:
            qualgbCd = "W"
            for pageNo in range(1, 7):

                url = "http://apis.data.go.kr/B490007/qualAcquPtcond/getQualAcquPtcond?numOfRows=50&pageNo={}&dataFormat=xml&acquYy=2021&qualgbCd={}&serviceKey=".format(pageNo, qualgbCd)
                key = "pg48D3FYflY8PkE9Vhd%2FkHGfCpn6iggpyOE7SJfTfGmA%2Bjw%2FpOka%2B0o2gw6CWR0XvRmCi62UbbJfxqQ8UDBCEQ%3D%3D"
                url += key

                response = requests.get(url).content
                soup = BeautifulSoup(response, 'html.parser')
                doc = ET.fromstring(str(soup))
                iter_elem = doc.iter(tag="item")
                for elem in iter_elem:
                    statistic = {}
                    check_cd = elem.find('jmcd').text
                    if check_cd not in check:
                        continue
                    # 데이터 리스트에 담기.
                    agegrupcd = elem.find('agegrupcd').text
                    gendercd = elem.find('gendercd').text
                    if check_cd+agegrupcd+gendercd in statistics:
                        statistics[check_cd+agegrupcd+gendercd]['acqucnt'] += int(elem.find('acqucnt').text)
                    else:
                        statistic['agegrupnm'] = elem.find('agegrupnm').text
                        statistic['gendernm'] = elem.find('gendernm').text
                        statistic['acqucnt'] = int(elem.find('acqucnt').text)
                        statistic['jmcd'] = elem.find('jmcd').text
                        statistics[check_cd+agegrupcd+gendercd] = (statistic)

# 남성과 여성 성별 숫자 따로 총합 내기.
statistics_list = [st for st in statistics.values()]
new_statistics_dictionary = dict()
for statistic in statistics_list:
    jmcd = statistic['jmcd']
    agegrupnm = statistic['agegrupnm']
    gendernm = statistic['gendernm']
    acqucnt = statistic['acqucnt']
    if jmcd in new_statistics_dictionary:
        if gendernm == '남성':
            new_statistics_dictionary[jmcd]['남성'] += acqucnt
        elif gendernm == '여성':
            new_statistics_dictionary[jmcd]['여성'] += acqucnt
    else:
        if gendernm == '남성':
            new_statistics_dictionary[jmcd] = {'남성': acqucnt, '여성': 0}
        elif gendernm == '여성':
            new_statistics_dictionary[jmcd] = {'남성': 0, '여성': acqucnt}

# sql문 저장
f = open('statistic.sql', 'w', encoding='utf8')
for statistic in statistics_list:
    s = "insert into statistics (statistic_age, statistic_gender, statistic_get_number, total_number_men, total_number_women, certificate_code) values ("
    jmcd_temp = ''
    for key, value in statistic.items():
        if key == 'jmcd': jmcd_temp = value; continue
        if type(value) == int:
            value = str(value)
        s += "'"+value.strip()+"', "
    s += "'"+str(new_statistics_dictionary[jmcd_temp]['남성'])+"', "+"'"+str(new_statistics_dictionary[jmcd_temp]['여성'])+"', "+"'"+jmcd_temp+"', "
    s = s.rstrip(', ')
    s += ");\n"
    f.write(s)
f.close()
