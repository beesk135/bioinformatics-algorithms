import sys, os, re, math, copy

def FarthestFirstTraversal(data, k):
    start = data[0]
    centers = [start]
    data.remove(start)
    while len(centers)<k:
        max_value = 0
        max_point = []
        for i in data:
            distance = []
            for j in centers:
                tmp_distance = 0
                for n in xrange(len(i)):
                    tmp_distance += (i[n]-j[n])**2
                distance.append(tmp_distance)
            if min(distance)>max_value:
                max_value = min(distance)
                max_point = i
        centers.append(max_point)
        data.remove(max_point)
    return centers


def distortion(data, centers):
    total = 0
    for i in data:
        min_dis = 1000000000
        for j in centers:
            tmp_dis = 0
            for k in xrange(len(j)):
                tmp_dis += (i[k]-j[k])**2
            if tmp_dis < min_dis:
                min_dis = tmp_dis
        total += min_dis
    return total/len(data)


def Lloyd(data, k):
    centers = data[0:k]
    total = 1000000000
    while total > 1e-9:
        graph = {}
        for i in xrange(k):
            graph[i] = []
        for i in data:
            min_dis = 1000000000
            for j in centers:
                tmp_dis = 0
                for n in xrange(len(data[0])):
                    tmp_dis += (i[n]-j[n])**2
                if tmp_dis < min_dis:
                    min_dis = tmp_dis
                    final_center = j
            graph[centers.index(final_center)].append(i)
        gravity = []
        for i in xrange(k):
            gravity.append([])
            for j in xrange(len(data[0])):
                tmp = 0                        
                for n in xrange(len(graph[i])):
                    tmp += graph[i][n][j]
                gravity[i].append(tmp/len(graph[i])) if len(graph[i])!=0 else gravity[i].append(0)

        total = 0
        for i in xrange(len(centers)):
            for j in xrange(len(centers[0])):
                total += (centers[i][j]-gravity[i][j])**2
        centers = gravity
    return centers
    


def expectationMax(data, k, beta, times):
    centers = copy.deepcopy(data[0:k])
    # centers = [[2.5],[-2.5]]
    n = 0
    while n<times:
        n += 1
        hiddenMatrix = [[0]*k for i in xrange(len(data))]
        for i in xrange(len(data)):
            dic = {}
            total = 0
            for j in xrange(len(centers)):
                distance = 0
                for m in xrange(len(data[i])):
                    distance += (data[i][m]-centers[j][m])**2
                dic[j] = math.sqrt(distance)
                total +=  math.exp(-beta*math.sqrt(distance))
            for center in xrange(len(centers)):
                hiddenMatrix[i][center] = math.exp(-beta*dic[center])/total

        ########### update the centers
        for i in xrange(len(centers)):
            for j in xrange(len(centers[i])):
                numerator = 0
                denominator = 0
                for m in xrange(len(data)):
                    numerator += hiddenMatrix[m][i]*data[m][j]
                    denominator += hiddenMatrix[m][i]
                centers[i][j] = numerator/denominator

    return centers

def hierachical(graph):
    times = len(graph)
    n = 1
    new_key = times+1

    cluster = {}
    for i in xrange(1,times+1):
        cluster[i] = {}
        cluster[i]['size'] = 1
        cluster[i]['items'] = [i]
        
    while n<times:
        cluster[new_key] = {}
        n += 1
        min_value = 1000000
        start = 0
        end = 0
        graph[new_key] = {}
        for i in graph:
            for j in graph[i]:
                if graph[i][j]<min_value:
                    min_value = graph[i][j]
                    start = i
                    end = j
        for i in graph:
            if i!=new_key:
                total = 0
                if start in graph[i]:
                    total += graph[i][start]*cluster[start]['size']
                if i in graph[start]:
                    total += graph[start][i]*cluster[start]['size']
                if end in graph[i]:
                    total += graph[i][end]*cluster[end]['size']
                if i in graph[end]:
                    total += graph[end][i]*cluster[end]['size']

                size = cluster[start]['size']+cluster[end]['size']
                cluster[new_key]['size'] = size
                cluster[new_key]['items'] = list(set(cluster[start]['items']+cluster[end]['items']))
                graph[new_key][i] = 1.0*total/size

        for i in graph:
            if start in graph[i]:
                graph[i].pop(start, None)
            if end in graph[i]:
                graph[i].pop(end, None)

        graph.pop(start, None)
        graph.pop(end, None)

        for items in cluster[new_key]['items']:          
            print items,
        print 

        new_key += 1
        




                
if  __name__ == '__main__':


    f = open('test', 'r')
    lines = f.readlines()
    n = int(lines[0].split()[0])
    graph = {}
    key = 1
    for line in lines[1:]:
        graph[key] = {}
        items = line.strip().split()
        for i in xrange(key,n):
            graph[key][i+1] = float(items[i])
        key += 1

    hierachical(graph)

    # f = open('test', 'r')
    # lines = f.readlines()
    # k = int(lines[0].split()[0])
    # m = int(lines[0].split()[1])
    # beta = float(lines[1])
    # data = []
    # for line in lines[2:]:
    #     data.append([float(x) for x in line.split()])
    # res = expectationMax(data, k, beta, 100)
    # for i in res:
    #     for j in i:
    #         print "%.3f" %j,

    #     print


    # f = open('test', 'r')
    # lines = f.readlines()
    # k = int(lines[0].split()[0])
    # m = int(lines[0].split()[1])
    # data = []
    # for line in lines[1:]:
    #     data.append([float(x) for x in line.split()])
    # res = Lloyd(data, k)
    # for i in res:
    #     for j in i:
    #         print "%.3f" %j,

    #     print


    # f = open('test', 'r')
    # lines = f.readlines()
    # k = int(lines[0].split()[0])
    # m = int(lines[0].split()[1])
    # centers = []
    # for line in lines[1:k+1]:
    #     centers.append([float(x) for x in line.split()])
    # data = []
    # for line in lines[k+2:]:
    #     data.append([float(x) for x in line.split()])
    # res = distortion(data, centers)

    # print res




    # f = open('test', 'r')
    # lines = f.readlines()
    # k = int(lines[0].split()[0])
    # m = int(lines[0].split()[1])
    # data = []
    # for line in lines[1:]:
    #     data.append([float(x) for x in line.split()])
    # res = FarthestFirstTraversal(data, k)

    # for i in res:
    #     for j in i:
    #         print j,
    #     print

