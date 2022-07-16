import requests
from bs4 import BeautifulSoup

def crawling_sites(url):
    # 요청한 url을 html 문서 형식으로 받아오기
    response = requests.request('GET', url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 특정 태그의 
    # 클래스 중심으로 찾고 싶을 때는 태그 바로 뒤에 '.클래스명'을 써주고,
    # id 중심으로 찾고 싶을 때는 태그 바로 뒤에 '#id명'을 써준다
    # 아래와 같이 쓴 경우에는 'rbj0Ud' 클래스명을 가진 div의 하위 div 태그를 가리킨다.
    titles = soup
    print(type(titles))
    print(titles)


url = 'http://192.168.167.5/'
crawling_sites(url)