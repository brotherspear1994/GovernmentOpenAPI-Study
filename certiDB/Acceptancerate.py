import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, dump

# 없는 종목코드 데이터 삽입 방지
# csv 파일 읽기
import csv

check = []
with open('certificate.csv', 'r', encoding='utf-8') as f:
    rdr = csv.reader(f)
    for certi_code in rdr:
        check = certi_code

datas = [] # statistics table에 담을 data

for pageNo in range(1, 55):
    url = "http://openapi.q-net.or.kr/api/service/rest/InquiryAcquStatisSVC/getEuhistList?numOfRows=50&pageNo={}&baseYY=2020&ServiceKey=".format(pageNo)
    key = ""
    url += key

    response = requests.get(url).content
    soup = BeautifulSoup(response, 'html.parser')
    doc = ET.fromstring(str(soup))
    iter_elem = doc.iter(tag="item")

    # 경과체크
    cnt = 0
    for elem in iter_elem:
        cnt +=1
        if (cnt%10) == 0: print("진행중.")
        data = {}
        check_cd = elem.find('jmcd').text
        if check_cd not in check:
            continue
        # 데이터 리스트에 담기.
        data['pilpassrate'] = elem.find('pilpassrate').text
        data['silpassrate'] = elem.find('silpassrate').text
        data['lastrsltpassrate'] = elem.find('lastrsltpassrate').text
        data['statisyy'] = elem.find('statisyy').text
        data['jmcd'] = elem.find('jmcd').text

        datas.append(data)

# sql문 저장
f = open('Acceptancerate.sql', 'w', encoding='utf8')
for data in datas:
    s = "insert into acceptance_rate (acceptance_rate_doc, acceptance_rate_prac, acceptance_rate_result, acceptance_stat_date, certificate_code) values ("
    for value in data.values():
        s += "'"+value.strip()+"', "
    s = s.rstrip(', ')
    s += ");\n"
    f.write(s)
f.close()
