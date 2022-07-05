'''
run with sudo

indexfinder() - input: none, output: minimum RSSI value(positive), Index of Node has minimum RSSI value
findlocation() - input: nearest node index, RSSI of nearest node, defined path(1 dimension array, ex: 1,5,2,8,3)
'''
import numpy as np
from bluepy.btle import Scanner
 
def indexfinder(): #find nearest node's rssi & MAC address


    #scann part
    time = 10 #scan time
    print("start scanning..")

    scanner = Scanner()
    devices = scanner.scan(time)
   
    MACaddr = ["98:7b:f3:5e:38:2f", "98:d3:31:fc:32:03" ,"X" ,"X" ,"X" ,"X" ,"X" ,"X" ,"X" ,"X"]
    RSSIval = [1000,1000,1000,1000,1000,1000,1000,1000,1000,1000]


    #anchor filtering
    for device in devices:
        print("ADDR = {} RSSI = {}".format(device.addr, device.rssi))
        for i in range(10):
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
           
    print("index for nearest node", minINDEX+1)
    return minRSSI, minINDEX


def findlocation(node,rssi,path): #nearest node number, rssi, defined path(1 dimension array)
    thres = 10
    index = 0 #입력받은 node가 경로상에서 몇 번째인지 저장
   
    for i in range (100):
        if(node == path[i]):
            index = i
            break
   
    if(rssi < thres): #임계값보다 rssi가 작으면 해당 노드에 매우 근접한 것으로 판단하고 현재위치를 해당 노드로 판단
        return path[index]
    else: #그게 아니라면 경로상의 이전 노드에 위치한다고 판단하고 경로상 이전 노드 리턴
        return path[index-1]
     
   
indexfinder()
