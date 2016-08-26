#!/usr/bin/python
import random
#import numpy as np
from OneDMarkov import OneDMarkov

test_num = 500

belta_star = 0.1
h_star = 3
cloudlet_num = 13
c = 2
R = 10

beltas = [0 for i in range(cloudlet_num)]

cloudlet_convert = [[0 for i in range(cloudlet_num)] for j in range(cloudlet_num)]
cloudlet_hops = [[0 for i in range(cloudlet_num)] for j in range(cloudlet_num)]
def readFiles():
    i = 0
    hop_file = open("cloudletHop.txt")
    hops = hop_file.readlines()
    for each in hops:
        tmp = each.split(' ')
        for j in range(len(tmp)):
            cloudlet_hops[i][j] = (int)(tmp[j])
        i += 1
    print "cloudletHop.txt read success."
    print cloudlet_hops 

    return 0

#def OneDMarkov():
#   return 0

def getCloudletsByHistorical(cloudlet):
    result = []
    cur = cloudlet
    next_cloudlet = 0
    max_num = 0
    for i in range(h_star):
        for j in range(1, cloudlet_num + 1):
            if cloudlet_convert[cur - 1][j - 1] > max_num:
                max_num = cloudlet_convert[cur - 1][j - 1]
                next_cloudlet = j
        cur = next_cloudlet
        if cur == 0:
            print "current cloudlet don't have historical data."
            break
        if getHop(cur, cloudlet) > h_star:
            print "over h_star"
            break
        #result[i] = cur
        result.append(cur)
        max_num = 0
        next_cloudlet = 0
    return result

def getDistance(cloudlet, user_dis):
    return user_dis

def getBelta(cloudlet, user_dis):
    return (1.0 / (user_dis ** c)) / ((beltas[cloudlet - 1]) + 1.0 / (getDistance(cloudlet, user_dis) ** c))

def getHop(cloudlet1, cloudlet2):
    return cloudlet_hops[cloudlet1 - 1][cloudlet2 - 1]

def obrap(cloudlet, user_dis): 
    belta = getBelta(cloudlet, user_dis)
    print "belta is " 
    print belta
    if (belta >= belta_star):
        beltas[cloudlet - 1] += 1.0 / (user_dis ** c)
        return cloudlet
    
    # get prediction by historical orbit.
    pre_cloudlets = getCloudletsByHistorical(cloudlet)
    print "pre_cloudlets is "
    print pre_cloudlets

    # get a cloudlet in pre_cloudlets fit the load need and hop limit.
    for pre_cloudlet in pre_cloudlets:
        if pre_cloudlet == 0:
            continue
        if getHop(pre_cloudlet, cloudlet) <= h_star:
            belta = getBelta(pre_cloudlet, user_dis)
            if (belta >= belta_star):
                beltas[cloudlet - 1] += 1.0 / (user_dis ** c)
                return pre_cloudlet

    # search for the closest cloudlet that fit the need.
    for hop in range(1, h_star + 1):
        for other in range(1, cloudlet_num + 1):
            if getHop(cloudlet, other) == hop:
                belta = getBelta(other, user_dis)
                if (belta >= belta_star):
                    beltas[cloudlet - 1] += 1.0 / (user_dis ** c)
                    return other
    
    # no suitable cloudlet exist.
    return 0

def notDispatch(cloudlet, user_dis):
    '''
    the policy don't dispatch request to other cloudlet.
    if current cloudlet can accept it, then return the cloudlet.
    else return 0 refer to reject the request.
    ''' 
    belta = getBelta(cloudlet, user_dis)
    print "belta is " 
    print belta
    if (belta >= belta_star):
        beltas[cloudlet - 1] += 1.0 / (user_dis ** c)
        return cloudlet
    return 0

def randDispatch(cloudlet, user_dis):
    '''
    the policy do randomly choose a cloudlet until the cloudlet 
    fit the load need to accept the request.
    if all cloudlet can not fit the need, then return 0.
    '''
    cloudlet_is_choosen = [0 for i in range(cloudlet_num)]
    not_end = True
    while not_end:
        cloudlet_id = random.randint(1, cloudlet_num)
        if cloudlet_is_choosen[cloudlet_id - 1] == 0:
            belta = getBelta(cloudlet_id, user_dis)
            print "belta is " 
            print belta
            if (belta >= belta_star and getHop(cloudlet_id, cloudlet) <= h_star):
                beltas[cloudlet - 1] += 1.0 / (user_dis ** c)
                return cloudlet
        cloudlet_is_choosen[cloudlet_id - 1] = 1
        for i in range(cloudlet_num):
            if cloudlet_is_choosen[i] == 0:
                not_end = True
                continue
        break 
    return 0

def greedyDispath(cloudlet, user_dis):
    '''
    use greedy algorithm to find the closest cloudlet fit the need.
    '''
    #max_hop = max(cloudlet_hops[cloudlet - 1])
    for i in range(1, h_star + 1):
        for j in range(cloudlet_num):
            if getHop(j, cloudlet) == i:
                belta = getBelta(j, user_dis)
                if (belta >= belta_star):
                    return j
    return 0

result_obrdp = [0 for i in range(test_num)]
result_rdp = [0 for i in range(test_num)]
result_greedydp = [0 for i in range(test_num)]
result_notdp = [0 for i in range(test_num)]
if __name__ == '__main__':
    cloudlet_convert = OneDMarkov()
    readFiles()
    print "after OneDMarkov"
    print cloudlet_convert
    for i in range(len(cloudlet_convert)):
        print sum(cloudlet_convert[i])
    print "begin exp"
    for i in range(test_num):
        cloudlet = random.randint(1, cloudlet_num)
        r_dis = random.uniform(0, R)
        print "clodlet is " + str(cloudlet)
        print "r_dis is " + str(r_dis)
        result_obrdp[i] = obrap(cloudlet, r_dis)
        result_notdp[i] = notDispatch(cloudlet, r_dis)
        result_rdp[i] = randDispatch(cloudlet, r_dis)
        result_greedydp[i] = randDispatch(cloudlet, r_dis)

    print "obr dp"
    print result_obrdp
    print "not dp"
    print result_notdp
    print "rand dp"
    print result_rdp
    print "greedy dp"
    print result_greedydp
