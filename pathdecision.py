# Python3 program to find the shortest
# path between any two nodes using
# Floyd Warshall Algorithm.
 
# Initializing the distance and
# Next array

'''
Functionalization & add path edit function:
        pathdecision(start, end, V, graph, cutoff): 
        INPUT: index for start node, index for wnd node(exit), number of node, graph(map), 1 dimension list for coutoff node
        OUTPUT: 1 dimension list(not numpy) for path. ex: if path is 1 -> 5 -> 6 -> 7 then output is [1,5,6,7]
                summation of weighting in output path
                                        
    
    graph input for n node:
        graph is n by n matrix
        graph[i][k] =   1 if exists path from i to k'th node
                        INF if not exists path from i to k'th node
                        0 when i == k
                        
        for example,
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
                        
'''

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
    
    
    
    #결오가 전재하는지 판단
    if(len(path) != 0):
        for i in (0,len(path)-2):
            
            k = path[i]
            l = path[i+1]
            
            summation = summation + graph[k][l]
    else:
        return "NO path", "NO path"
    
    
 
    
    return path, summation

        # This code is contributed by mohit kumar 29



'''
for Debuging
'''




MAXM,INF = 100,10**7
 
#노드 개수
V = 11
 
#연결점 구현. 순서대로 0번 노드에서 시작해 0,1,2,3... 노드까지 가는 가중치(INF)는 경로 없음
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

cutoff = [7]
path1, summ = pathdecision(1, 7, V, graph, cutoff)

print("Decisioned path is :", path1, "Weighted sum is = ", summ)






