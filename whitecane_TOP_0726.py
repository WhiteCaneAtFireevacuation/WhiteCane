'''
whitecane 탑레벨 실행파일

07_28 노드 2개 테스트용
'''
#패키지
import os
import time
import datetime
import requests
import urllib.request
from bs4 import BeautifulSoup
from bluepy.btle import Scanner
from selenium import webdriver
#from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

#함수
def indexfinder(MACaddr): #find nearest node's rssi & MAC address
    #scann part
    time = 10 #scan time
    print("start scanning..")

    scanner = Scanner()
    devices = scanner.scan(time)
    RSSIval = [1000,1000,1000,1000,1000,1000,1000,1000,1000,1000]


    #anchor filtering
    for device in devices:
        print("ADDR = {} RSSI = {}".format(device.addr, device.rssi))
        for i in range(len(devices)):
            if(device.addr == MACaddr[i]):
                RSSIval[i] = device.rssi * (-1)
                print("detected. rssi value is =", RSSIval[i])
                break
   
               
    minRSSI = 10000
    minINDEX = 11


    #find nearest node
    for k in range(10):
        if(minRSSI > RSSIval[k]):
            minRSSI = RSSIval[k]
            minINDEX = k
           
    print("index for nearest node", minINDEX)
    return minRSSI, minINDEX
def findlocation(node,rssi,path): #nearest node number, rssi, defined path(1 dimension array)
    thres = 60
    index = 0 #입력받은 node가 경로상에서 몇 번째인지 저장
   
    for i in range (100):
        if(node == path[i]):
            index = i
            break
   
    if(rssi < thres): #임계값보다 rssi가 작으면 해당 노드에 매우 근접한 것으로 판단하고 현재위치를 해당 노드로 판단
        return path[index], index
    else: #그게 아니라면 경로상의 이전 노드에 위치한다고 판단하고 경로상 이전 노드 리턴
        return path[index-1], index -1
def getdatafromweb(ipaddr): #웹으로부터 데이터를 받아와서 화재 발생시 1, 통신 불가능 시 2 리턴
    try:
        fire = int(0)
    
        page = urllib.request.urlopen(ipaddr)
        text = page.read().decode("utf-8")

        where=text.find('Celsius:')

        start_of_information = where + 8
        end_of_information = start_of_information + 11

        information1 = text[start_of_information:end_of_information]
        information1 = float(information1)

        where=text.find('Humidity:')

        start_of_information = where + 9
        end_of_information = start_of_information + 11

        information2 = text[start_of_information:end_of_information]
        information2 = float(information2)

        print('Celsius: ')
        print(information1)
        print('Humidity: ')
        print(information2)

        if (information1 < 50):
            return 0
        else:
            return 1
    except:
        print("Error Occured")
        return 2
def pathdecision(start, end, V, igraph, cutoff):
    global dis, Next
    MAXM,INF = 100,10**7
    
    '''
    ignore blocked node part
    '''
    
    graph = igraph #copy graph

    #eliminate blocked node
    for i in range(V):
        for k in (0, (len(cutoff)) - 1):
            graph[i][cutoff[k]] = INF
        k = 0


    def initialise(V):
        
        for i in range(V):
            for j in range(V):
                dis[i][j] = graph[i][j]
     
                # No edge between node
                # i and j
                if (graph[i][j] == INF):
                    Next[i][j] = -1
                else:
                    Next[i][j] = j
     
    # Function construct the shortest
    # path between u and v
    def constructPath(u, v):
        global graph, Next
         
        # If there's no path between
        # node u and v, simply return
        # an empty array
        if (Next[u][v] == -1):
            return {}
     
        # Storing the path in a vector
        path = [u]
        while (u != v):
            u = Next[u][v]
            path.append(u)
     
        return path
     
    # Standard Floyd Warshall Algorithm
    # with little modification Now if we find
    # that dis[i][j] > dis[i][k] + dis[k][j]
    # then we modify next[i][j] = next[i][k]
    def floydWarshall(V):
        global dist, Next
        for k in range(V):
            for i in range(V):
                for j in range(V):
                     
                    # We cannot travel through
                    # edge that doesn't exist
                    if (dis[i][k] == INF or dis[k][j] == INF):
                        continue
                    if (dis[i][j] > dis[i][k] + dis[k][j]):
                        dis[i][j] = dis[i][k] + dis[k][j]
                        Next[i][j] = Next[i][k]
     
    # Print the shortest path
    def printPath(path):
        n = len(path)
        for i in range(n - 1):
            print(path[i], end=" -> ")
        print (path[n - 1])
     
    # Driver code
    #if __name__ == '__main__':
    MAXM,INF = 100,10**7
    dis = [[-1 for i in range(MAXM)] for i in range(MAXM)]
    Next = [[-1 for i in range(MAXM)] for i in range(MAXM)]
 
   
    # Function to initialise the
    # distance and Next array
    initialise(V)
 
    # Calling Floyd Warshall Algorithm,
    # this will update the shortest
    # distance as well as Next array
    floydWarshall(V)
    path = []
 
    
    path = constructPath(start, end)
    
    #sum of weight value
    summation = 1
    
    
    
    #경로가 전재하는지 판단
    if(len(path) != 0):
        for i in (0,len(path)-2):
            
            k = path[i]
            l = path[i+1]
            
            summation = summation + graph[k][l]
    else:
        return "NO path", "NO path"
    
    
 
    
    return path, summation
def getmap(): #웹으로부터 그래프 가져오는 함수(미구현)
    
    graph = [ [ 0, INF, 1, INF, INF, INF, INF, INF, INF, INF, INF ],
        [ INF, 0, INF, INF, INF, 1, INF, INF, INF, INF, INF],
        [ INF, INF, 0, INF, INF, 1, INF, INF, INF, INF, INF],
        [ INF, INF, 1, 0, INF, INF, INF, INF, INF, INF, INF],
        [ INF, INF, INF, 1, 0, INF, INF, INF, INF, INF, INF],
        [ INF, INF, INF, INF, INF, 0, 1, INF, INF, INF, INF],
        [ INF, INF, INF, INF, INF, INF, 0, 1, 1, INF, INF], 
        [ INF, INF, INF, INF, INF, INF, INF, 0, INF, INF, INF], #탈출구
        [ INF, INF, INF, INF, INF, INF, INF, INF, 0, 1, INF],
        [ INF, INF, INF, INF, INF, INF, INF, INF, INF, 0, 1],
        [ INF, INF, INF, INF, INF, INF, INF, 1, INF, INF, 0]
        ]

    graph = [ [0, 1],
    [INF, 0]
    ]

    return graph

def alarmorder(alarm,control): #지정된 노드로 알림명령 전송. control이 0이면 알람 on, 1이면 알람 off
    URL0 = 'http://192.168.191.131'
    URL1 = 'http://192.168.191.131'

    URLaddr = [URL0,URL1]
    s = Service('/usr/local/bin/chromedriver') #라즈베리파이용 chromedriver 주소
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome(service=s,options=chrome_options)
    print("adwdawdadwadadw")
    print("IP addr is: ", URLaddr[alarm])
    driver.get(URLaddr[alarm])

    if(control == 0):
        print("LED ON: ", alarm, "Node")
        driver.find_element("xpath",'/html/body/a[1]').click()

    
    else:
        print("LED OFF: ", alarm, "Node")
        driver.find_element("xpath",'/html/body/a[2]').click()
def setup(): #IP,MAC주소 입력용
    arr1 = []
    arr2 = []

    print("url 주소 입력. 완료하려면 -1 입력")
    while(True):
        URL = input()
        if(URL != -1):
            arr1.append(URL)
        else:
            break

    print("MAC 주소 입력. 완료하려면 -1 입력")
    while(True):
        MAC = input()
        if(MAC != -1):
            arr2.append(MAC)
        else:
            break

    return arr1, arr2

#각 노드별 url주소(IP), 화재발생여부
URL0 = 'http://192.168.191.131'
URL1 = 'http://192.168.191.131'

URLaddr = [URL0,URL1]
#URLaddr = URLaddr1.split(',')
MACaddr = ["98:7b:f3:5e:38:2f", "98:d3:31:fc:32:03", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"]
cutoff = [] #화재가 발생한 노드번호. 즉 차단된 노드
discon = [] #통신이 불가능한 노드번호.

#임의실행용 상수
MAXM,INF = 100,10**7

#전역변수
location = 0 #현재 지팡이 위치(노드)
fire = True #화재 발생 여부(bool)
V = 10 #총 노드 개수
igraph = getmap() #건물 그래프
Exit = [1] #탈출구 노드 인덱스
firstexcute = True #길 안내 최초 시작 여부
thres = 50 #rssi 임계값

while(True):
    rssi, index = indexfinder(MACaddr) #지팡이 최근접 노드 rssi값, 노드 인덱스
    print("for debug: index is ", index)
    
    #노드 정보 갱신
    cutoff = [] 
    discon = [] 

    #화재 발생 여부 판단. 화재가 발생한 노드의 인덱스를 cutoff에 저장
    for i in range (len(URLaddr)):
        if(getdatafromweb(URLaddr[i]) == 1): #i번 노드에서 화재가 발생했다고 감지되면
            cutoff.append(i) #cutoff배열에 인덱스인 i 추가

            fire = True #화재가 발생한것으로 판단

    i = 0 #변수 초기화인데 이거 필요한가..?

    #통신 불가 여부 판단. 통신이 끊어진 노드의 인덱스를 discon에 저장
    for i in range (len(URLaddr)):
        if(getdatafromweb(URLaddr[i]) == 2): #i번 노드에서 화재가 발생했다고 감지되면
            discon.append(i) #cutoff배열에 인덱스인 i 저장

    i = 0

    '''
    배열 cutoff, discon 웹에 전송(아직 구현 안함)
    '''
    print("for debuging: 화재가 발생한 노드는", cutoff, "입니다.")

    if(fire == True): #화재 발생시 아래 코드 실행
        print("for debuging: FIRE ALERT")

        #최초 발생여부 판단. 화재 발생 이전에는 경로가 지정되지 않았기 때문에 
        #최근접 노드에 충분히 가까이 위치시킬 필요가 있음

        if(firstexcute == True):
            while(True):
                print("for debug: line 333 excuted")
                #try:
                    #no_space = URLaddr[index].encode('acsii', 'ignore').decode('unicode_escape')
                alarmorder(index,0)#최단거리 노드에 도착하도록 알림 전송
                #except:
                   # print("try - except excuted")
                   # os.system('sudo python3 bell.py')                    
                
                rssi, index = indexfinder(MACaddr) #rssi값 갱신
                if(rssi < thres): #rssi가 미리 지정된 임계값 thres보다 작다면
                    print("for debug: firstexcute turns False")
                    firstexcute = False #최초 실행단계는 벗어났다고 판단
                    break #그 후 반복문 중단 - 최근접 노드에 위치시키는 과정 중단

        else: #최초 실행단계를 벗어난 경우(즉 최근접 노드에 충분히 가깝다고 판단되면) 
              #경로를 지정하고 거기에 맞추어 유도 시작
            
            #최단경로 찾는 부분
            for k in Exit:
                minsum = 1000 #최소 가중치합
                minpath_index = 1000 #최소 가중치합을 가지는 탈출구의 인덱스
                path, summation = pathdecision(index, k, V, igraph, cutoff)

                #탈출 가능 경로가 없는 경우
                if(summation == "NO path"):
                    print("you died")
                    exit()
                else:
                    if(summation <= minsum):
                        minsum = summation #최소값 갱신
                        minpath_index = k #인덱스 갱신
       
            #tmp 변수는 그냥 함수 리턴값 때문에 넣음 노쓸모
            path_final, tmp = pathdecision(index, minpath_index, V, igraph, cutoff) #최단거리를 가지는 탈출구로 유도하는 경로 

            #지팡이의 위치를 결정. index_node는 현재 노드가 경로상 몇 번째에 있는지를 의미
            location, index_node = findlocation(index, rssi, path_final)

            #경로상 다음 노드에 알람을 전송
            alarmorder(path_final[index_node + 1],0)
    else:
        print("화재 발생하지 않음")
        time.sleep(5)