# 문화재청 문화재 정보 Open API를 활용해 데이터 받아오기

`정부 공공데이터 중 문화재청에서 제공하는 문화재 정보 Open API를 활용해 원하는 데이터만을 받아와 Sql 파일의 형태로 저장해보는 연습을 가졌습니다.`

- [문화재청 문화재 Open API 주소](https://www.cha.go.kr/html/HtmlPage.do?pg=/publicinfo/pbinfo3_0201.jsp&mn=NS_04_04_02)



## 홈페이지 데이터 설명서 확인

![image-20210124215736394](README.assets/image-20210124215736394.png)

![image-20210124215803504](README.assets/image-20210124215803504.png)

- 문화재 정보 Open API 요청을 위한 기본 url 정보와 그 외 요청 파라미터 값들을 확인한다.
- 우선 전체 페이지 조회를 위한 'pageUnit'과 'pageIndex' 파라미터 외에 필요한 파라미터 정보들은 홈페이지의 `활용정보`에서 확인할 수 있다.
- 데이터를 받아오기 위한 코드를 짜기 전, 전체 파라미터 사용법과 전체 데이터의 양을 확인하기 위해 웹상에서 요청파라미터 인자들을 넣어 데이터를 html 형식으로 확인해 봤다.
  - 파라미터를 넣은 검색주소: http://www.cha.go.kr/cha/SearchKindOpenapiList.do?pageUnit=900&pageIndex=18
  - 페이지 하나동 조회 정보의 개수를 900으로 놓고 18페이지를 조회하면 가장 마지막 데이터인 16054번째의 데이터를 확인할 수 있다.



## 작업수행을 위한 기본 라이브러리 활용법

```python
import requests
from bs4 import BeautifulSoup as bs
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, dump, ElementTree
```

- `requests`: **Requests** allows you to send HTTP/1.1 requests extremely easily. There’s no need to manually add query strings to your URLs, or to form-encode your POST data. Keep-alive and HTTP connection pooling are 100% automatic, thanks to [urllib3](https://github.com/urllib3/urllib3).

  - ```python
    # 사용예시
    >>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
    >>> r.status_code
    200
    >>> r.headers['content-type']
    'application/json; charset=utf8'
    >>> r.encoding
    'utf-8'
    >>> r.text
    '{"type":"User"...'
    >>> r.json()
    {'private_gists': 419, 'total_private_repos': 77, ...}
    ```
  
- `Beautiful Soup`:  Beautiful Soup is a Python library for pulling data out of HTML and XML files.

  - ```python
    # 사용예시
    import requests
    from bs4 import BeautifulSoup
    
    url = 'https://kin.naver.com/search/list.nhn?query=%ED%8C%8C%EC%9D%B4%EC%8D%AC'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        print(soup)
    
    else : 
        print(response.status_code)
    ```

- `xml.etree.ElementTree`:  The [`xml.etree.ElementTree`](https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree) module implements a simple and efficient API for parsing and creating XML data.

  - ```python
    # 사용예시
    import xml.etree.ElementTree as ET
    tree = ET.parse('country_data.xml')
    root = tree.getroot()
    # Or directly from a string:
root = ET.fromstring(country_data_as_string)
    ```
    
  - `Element.find`: [`Element.find()`](https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element.find) finds the *first* child with a particular tag
  
  - `Element.text`: [`Element.text`](https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element.text) accesses the element’s text content. [`Element.get()`](https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element.get) accesses the element’s attributes
  
  - `ElementTree`: [`ElementTree`](https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.ElementTree) provides a simple way to build XML documents and write them to files. The [`ElementTree.write()`](https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.ElementTree.write) method serves this purpose.
  
  - `dump`: Writes an element tree or element structure to sys.stdout. This function should be used for debugging only.



## 전체 목록 가져오기

```python
#전체 목록 가져오기
cnt = 1 # 진행상황 확인을 위한 cnt 선언
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
```



## 상세정보 가져오기

![image-20210124231632560](README.assets/image-20210124231632560.png)

- 문화재검색 상세조회를 위한 필수 요청 파라미터들이다.

```python
#상세정보 가져오기

#7000개마다 연결 끊김
cnt=1 # 상세정보 가져오기 진행상황 확인을 위한 cnt 선언
for heritage in heritages[:7000]:
    # 문화재검색 상세조회를 위한 필수 요청 파라미터들을 url에 넣어 API 요청을 보낸다.
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
```



## 필요없는 속성 삭제 & 싱글쿼터 제거

```python
#필요없는 속성 삭제
# 순번과 문화재명(한자)는 필요없으므로 삭제해준다.
cnt = 1
for i in heritages:
    del i['sn'] # 순번 
    del i['ccbamnm2'] # 문화재명(한자)
    if cnt%1000 == 0:
        print(cnt)
    cnt += 1
```

- `del` dict[key]

  - ```python
    # 사용법 참고
    # Dictionary of strings and int
    word_freq_dict = {"Hello": 56,
                      "at": 23,
                      "test": 43,
                      "this": 43}
    # Deleting an item from dictionary using del
    del word_freq_dict['at']
    print(word_freq_dict)
    ```

```python
#싱글쿼터 제거
cnt = 1
for heritage in heritages:
    for key, value in heritage.items():
        heritage[key] = value.replace("'", "‘")
    print(heritage)
    if cnt % 1000 == 0:
        print(cnt)
    cnt += 1
```

- `dic.items()`: The `items()` method returns a view object. The view object contains the key-value pairs of the dictionary, as tuples in a list.



## Sql문 파일로 저장

```python
#sql문 저장
f = open('test.sql', 'w', encoding='utf8')
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
```

- `open`(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)

  - Open *file* and return a corresponding [file object](https://docs.python.org/3/glossary.html#term-file-object).

- `Write to an Existing File`

  - `"a"` - Append - will append to the end of the file

  - `"w"` - Write - will overwrite any existing content

  - ```python
    # 사용예시
    f = open("demofile2.txt", "a")
    f.write("Now the file has more content!")
    f.close()
    
    #open and read the file after the appending:
    f = open("demofile2.txt", "r")
    print(f.read())
    ```

- **Python** Dictionary **values() Method**

  The **values() method** returns a view object. The view object contains the **values** of the dictionary, as a list.



## 결과물 조회

![result](README.assets/result.png)



## 참조한 주요 공식문서

- [python xml.etree.ElementTree 공식문서](https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element)



