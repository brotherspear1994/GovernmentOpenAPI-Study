import requests
from bs4 import BeautifulSoup as bs # Beautiful Soup is a Python library for pulling data out of HTML and XML files.
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, dump, ElementTree

#전체 목록 가져오기
cnt = 1
heritages = []
for page in range(1,18):
    url = "http://www.cha.go.kr/cha/SearchKindOpenapiList.do?pageUnit=1000&pageIndex=" + str(page)
    response = requests.get(url).content
    soup = bs(response, 'html.parser')
    doc = ET.fromstring(str(soup)) # object 형태로 데이터를 반환
    iter_elem = doc.iter(tag="item") # Creates a tree iterator with the current element as the root.
    for elem in iter_elem:
        # 파라미터 값에 접근할때 전부 소문자임을 주의
        heritage = {} # 딕셔너리에 키와 벨류 형태로 문화재 목록 정보를 담는다.
        heritage['sn'] = elem.find('sn').text
        heritage['no'] = elem.find('no').text
        heritage['ccmaname'] = elem.find('ccmaname').text
        heritage['crltsnonm'] = elem.find('crltsnonm').text
        heritage['ccbamnm1'] = elem.find('ccbamnm1').text
        heritage['ccbamnm2'] = elem.find('ccbamnm2').text
        heritage['ccbactcdnm'] = elem.find('ccbactcdnm').text
        heritage['ccsiname'] = elem.find('ccsiname').text
        heritage['ccbaadmin'] = elem.find('ccbaadmin').text
        heritage['ccbakdcd'] = elem.find('ccbakdcd').text
        heritage['ccbactcd'] = elem.find('ccbactcd').text
        heritage['ccbaasno'] = elem.find('ccbaasno').text
        heritage['ccbacncl'] = elem.find('ccbacncl').text
        heritage['ccbacpno'] = elem.find('ccbacpno').text
        heritage['longitude'] = elem.find('longitude').text
        heritage['latitude'] = elem.find('latitude').text
        heritages.append(heritage) # 문화재 1개의 필요 파라미터 값들을 모두 딕셔너리에 담는 것을 완료한 후, heritages 배열에 담아준다.
    if cnt % 1000 == 0:
        print(cnt)
    cnt+=1
    print(page, " 전체목록 완료")
    

#상세정보 가져오기

#7000개마다 연결 끊김
cnt=1 # 상세정보 가져오기 진행상황 확인을 위한 cnt 선언
for heritage in heritages[:7000]: # 중간에 7000개로 끊었는데 어떻게 16504개 정보다 가져왔지,,,
    url = "http://www.cha.go.kr/cha/SearchKindOpenapiDt.do?ccbaKdcd="+heritage['ccbakdcd']+"&ccbaCtcd="+heritage['ccbactcd']+"&ccbaAsno="+heritage['ccbaasno']
    response = requests.get(url).content
    soup = bs(response, 'html.parser')
    doc = ET.fromstring(str(soup))
    iter_elem = doc.iter(tag="item")
    for elem in iter_elem: # 위와 마찬가지의 방법으로, 위 문화재검색 목록조회를 완료한 문화재 딕셔너리 아이템에 문화재 검색 상세조회를 위한 파라미터들과 그 값을 추가로 넣어준다.
        heritage['gcodename'] = elem.find('gcodename').text
        heritage['bcodename'] = elem.find('bcodename').text
        heritage['mcodename'] = elem.find('mcodename').text
        heritage['scodename'] = elem.find('scodename').text
        heritage['ccbaquan'] = elem.find('ccbaquan').text
        heritage['ccbaasdt'] = elem.find('ccbaasdt').text
        heritage['ccbalcad'] = elem.find('ccbalcad').text
        heritage['cccename'] = elem.find('cccename').text
        heritage['ccbaposs'] = elem.find('ccbaposs').text
        heritage['content'] = elem.find('content').text
    if cnt%500 == 0:
        print(cnt, "개 완료!!!")
    cnt += 1

#필요없는 속성 삭제
# 순번과 문화재명(한자)는 필요없으므로 삭제해준다.
cnt = 1
for i in heritages:
    del i['sn'] # 순번 
    del i['ccbamnm2'] # 문화재명(한자)
    if cnt%1000 == 0:
        print(cnt)
    cnt += 1
    

#싱글쿼터 제거
cnt = 1
for heritage in heritages:
    for key, value in heritage.items():
        heritage[key] = value.replace("'", "‘")
    if cnt % 1000 == 0:
        print(cnt)
    cnt += 1


#sql문 저장
f = open('heritage.sql', 'w', encoding='utf8')
cnt = 1
for heritage in heritages:
    # 파일 형식이 insert into heritage values (' 로 시작해서 ');로 끝나게 전환.
    s = "insert into heritage values ("
    for i in heritage.values():
        s += "'" + i.strip() + "', "
    s = s.rstrip(' ,')
    s += ");\n"
    f.write(s) # sql 파일에 appending
    if cnt % 1000 == 0:
        print(cnt)
    cnt += 1
f.close()
