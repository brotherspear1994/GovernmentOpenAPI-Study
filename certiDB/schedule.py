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

for jmCd in check:
    url = "http://apis.data.go.kr/B490007/qualExamSchd/getQualExamSchdList?numOfRows=50&pageNo=1&dataFormat=xml&implYy=2021&jmCd={}&ServiceKey=".format(jmCd)
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
        if (cnt%2) == 0: print("진행중.")

        data = {}

        # 데이터 리스트에 담기.
        if elem.find('docexamenddt').text == None:
            temp = '00000000'
            data['docexamenddt'] = temp
        else:
            data['docexamenddt'] = elem.find('docexamenddt').text
        if elem.find('docexamstartdt').text == None:
            temp = '00000000'
            data['docexamstartdt'] = temp
        else:
            data['docexamstartdt'] = elem.find('docexamstartdt').text
        if elem.find('docpassdt').text == None:
            temp = '00000000'
            data['docpassdt'] = temp
        else:
            data['docpassdt'] = elem.find('docpassdt').text
        if elem.find('docregenddt').text == None:
            temp = '00000000'
            data['docregenddt'] = temp
        else:
            data['docregenddt'] = elem.find('docregenddt').text
        if elem.find('docregstartdt').text == None:
            temp = '00000000'
            data['docregstartdt'] = temp
        else:
            data['docregstartdt'] = elem.find('docregstartdt').text

        data['implseq'] = elem.find('implseq').text
        data['implyy'] = elem.find('implyy').text
        data['pracexamenddt'] = elem.find('pracexamenddt').text
        data['pracexamstartdt'] = elem.find('pracexamstartdt').text
        data['pracpassdt'] = elem.find('pracpassdt').text
        data['pracregenddt'] = elem.find('pracregenddt').text
        data['pracregstartdt'] = elem.find('pracregstartdt').text
        data['jmcd'] = jmCd
        if None in data.values():
            continue
        datas.append(data)

# sql문 저장
f = open('schedule.sql', 'w', encoding='utf8')
for data in datas:
    s = "insert into schedule (schedule_doc_exam_end_dt, schedule_doc_exam_start_dt, schedule_doc_pass_dt, schedule_doc_reg_end_dt, schedule_doc_reg_start_dt, \
    schedule_impl_seq, schedule_impl_year, schedule_prac_exam_end_dt, schedule_prac_exam_start_dt, schedule_prac_pass_dt, schedule_prac_reg_end_dt, \
    schedule_prac_reg_start_dt, certificate_code) values ("
    for value in data.values():
        s += "'"+value.strip()+"', "
    s = s.rstrip(', ')
    s += ");\n"
    f.write(s)
f.close()
