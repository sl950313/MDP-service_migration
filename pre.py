#!/usr/bin/python
import numpy as np
import math
import random
import mdptoolbox.example
import matplotlib.pyplot as plt
from getCloudlet import getCloudlet, getDistance

curCloudlet = 1;
servCloudlet = 1;

cloudlet = open('cloudletPosition.txt')
status = open('user_position.txt')
clHop = open('cloudletHop.txt')
TimeFile = open('dwellTime.txt')
position_states = []
Time = []
cloudletHop = np.zeros((13, 13))
positions = status.readlines()
clHops = clHop.readlines()
cloudletPositions = cloudlet.readlines()
#cloudletPositions = cloudletPositionsFile.readlines()
dwellTimes = TimeFile.readlines()
clP = {}

totalPositionCount = 18
s_lat_long = {} # ref to a map, position -> (lat, long). for easy to caculate distance between user position and cloudlet.
for position in positions:
    position_detail = position.split(' ')
    position_states.append((int)(position_detail[0]))
    s_lat_long[(int)(position_detail[0]) - 1] = ((float)(position_detail[1]), (float)(position_detail[2])) 

for cloudletPosition in cloudletPositions:
    tmp = cloudletPosition.split(' ')
    clP[(int)(tmp[0])] = ((float)(tmp[1]), (float)(tmp[2]))

for dwellTime in dwellTimes:
    Time.append((int)(dwellTime))

print Time

print "clP"
print clP
print "s_lat_long"
print s_lat_long
print "totalPositionCount"
print totalPositionCount

i = 0;
for clHop in clHops:
    clHop_tmp = clHop.split(' ')
    for j in range(len(clHop_tmp)):
        cloudletHop[i][j] = (int)(clHop_tmp[j])
    i += 1
print "cloudletHop : "
print cloudletHop


# 1-D Markov Prediction Model.
statePre = [[0 for col in range(totalPositionCount)] for row in range(totalPositionCount)] 
for i in range(len(position_states) - 2):
    statePre[(int)(position_states[i]) - 1][(int)(position_states[i + 1]) - 1] += 1
print "statePre"
print statePre

#definition of dwell time of user.
v = 5.0 # the velocity of user.
R = 20.0 # the region of cloudlet.
tao = 0.1 # the user dentity of Cloudlet.
belta = 0.5 # service thredhold.
c = 2 # ...
E = 2
thita = 2
# compare R of AMP,RNP, NMP
# AMP_R = np.zeros(30)
# RNP_R = np.zeros(30)
# NMP_R = np.zeros(30)
# MDP_R = np.zeros(30)
AMP_R = [0 for i in range(0, 30)]
NMP_R = [0 for i in range(0, 30)]
MDP_R = [0 for i in range(0, 30)]
RNP_R = [0 for i in range(0, 30)]

AMP_policy = [1 for i in range(13 * 13)]
RNP_policy = [0 for i in range(13 * 13)]
NMP_policy = [0 for i in range(13 * 13)]


# use MDP value_iterator algrithm to get an optimal policy. and get a Reward.  
# get the closest cloudlet to user.
R_i = 0
for index in range(len(position_states) - 30, len(position_states) - 1):
    a = 2
    curCloudlet = getCloudlet(s_lat_long[position_states[index] - 1][0], s_lat_long[position_states[index] - 1][1], cloudletPositions)
    print "in MDP curCloudlet = " + str(curCloudlet)
    print curCloudlet
    r = getDistance(s_lat_long[position_states[index] - 1][0], s_lat_long[position_states[index] - 1][1], clP[curCloudlet][0], clP[curCloudlet][1])

    #T_avg = (float)((((R - r) / (float)(v)) + ((R + r) / (float)(v))) / 2.0)
    T_avg = math.pi
    print T_avg
    #definition of alpha(T(Ci)).
    if (float)(Time[curCloudlet - 1]) > T_avg:
        alpha = 1.0
    else:
        alpha = math.exp(Time[curCloudlet] - T_avg)
    rou = alpha * E * (cloudletHop[curCloudlet - 1][servCloudlet - 1])
    R = np.zeros((2, 13 * 13, 13 * 13))

    #definition of Rg(r)
    Rg = math.pow(belta, -c) * r
    #definition of cloudlet load.
    epsilon = math.exp(-2 * math.pi * tao * Rg)

    for C in range(1, 14):
        for C2 in range(1, 14):
            if Time[C2 - 1] > T_avg:
                alpha = 1
            else:
                alpha = math.exp(Time[C2 - 1] - T_avg)
            rou = alpha * E * cloudletHop[C - 1][C2 - 1]
            R[1][(C- 1) * 13 + C2 - 1][(C2 - 1) * 13 + C2 - 1] = cloudletHop[C2 - 1][C - 1] * epsilon * alpha * (rou - thita)
    P = np.zeros((2, 13 * 13, 13 * 13))
    for C in range(1, 14):
        for C2 in range(1, 14):
            P[1][(C - 1) * 13 + C2 - 1][(C2 - 1) * 13 + C2 - 1] = 1

    pre = statePre[position_states[len(position_states) - 1] - 1]
    print "position_states[position_states[len(position_states) - 1]]"
    print position_states[position_states[len(position_states) - 1] - 1]
    print "pre"
    print pre

    cloudletNum = np.zeros((totalPositionCount))
    print "curCloudlet"
    print curCloudlet
    for i in range(totalPositionCount):
        if pre[i] != 0:
            cloudletNum[i] = (int)(getCloudlet(s_lat_long[i][0], s_lat_long[i][1], cloudletPositions)) 
            P[0][(servCloudlet - 1) * 13 + curCloudlet - 1][(servCloudlet - 1) * 13 + cloudletNum[i] - 1] += ((float)(pre[i]) / (float)(sum(pre)))

    for i in range(0, 13 * 13):
        if sum(P[0][i]) != 1:
            for j in range(0, 13 * 13):
                P[0][i][j] = 1.0 / (float)(13 * 13)
    initV = []
    for i in range(0, 13 * 13):
        initV.append(0)
    print len(initV)

    discout_factor = 0.9
    vi = mdptoolbox.mdp.ValueIteration(P, R, discout_factor, 0.01, 1000, initV, True) 
    vi.run()

    # vi.policy = [] is result of MDP.
    # get the RNP_policy
    MDP_policy = vi.policy
    if R_i > 0:
        tmp = MDP_R[R_i - 1]
    else:
        tmp = 0
    if MDP_policy[(servCloudlet - 1) * 13 + curCloudlet - 1] == 1:
        MDP_R[R_i] = R[1][(servCloudlet - 1) * 13 + curCloudlet - 1][(curCloudlet - 1) * 13 + curCloudlet - 1] + tmp
        servCloudlet = curCloudlet
    else:
        MDP_R[R_i] = tmp

    R_i += 1

# use AMP_policy.
R_i = 0
for index in range(len(position_states) - 30, len(position_states) - 1):
    curCloudlet = getCloudlet(s_lat_long[position_states[index] - 1][0], s_lat_long[position_states[index] - 1][1], cloudletPositions)
    print curCloudlet
    r = getDistance(s_lat_long[position_states[index] - 1][0], s_lat_long[position_states[index] - 1][1], clP[curCloudlet][0], clP[curCloudlet][1])
    T_avg = ((R - r) / v + (R + r) / v) / 2
    T_avg = math.pi
    #definition of alpha(T(Ci)).
    alpha = 0
    if Time[curCloudlet - 1] > T_avg:
        alpha = 1
    else:
        alpha = math.exp(Time[curCloudlet] - T_avg)
    rou = alpha * E * (cloudletHop[curCloudlet - 1][servCloudlet - 1])
    R = np.zeros((2, 13 * 13, 13 * 13))

    #definition of Rg(r)
    Rg = math.pow(belta, -c) * r
    #definition of cloudlet load.
    epsilon = math.exp(-2 * math.pi * tao * Rg)

    for C in range(1, 14):
        for C2 in range(1, 14):
            if Time[C2 - 1] > T_avg:
                alpha = 1
            else:
                alpha = math.exp(Time[C2 - 1] - T_avg)
            rou = alpha * E * cloudletHop[C - 1][C2 - 1]
            R[1][(C- 1) * 13 + C2 - 1][(C2 - 1) * 13 + C2 - 1] = cloudletHop[C2 - 1][C - 1] * epsilon * alpha * (rou - thita)
    if R_i > 0:
        tmp = AMP_R[R_i - 1]
    else:
        tmp = 0

    AMP_R[R_i] = R[1][(servCloudlet - 1) * 13 + curCloudlet - 1][(curCloudlet - 1) * 13 + curCloudlet - 1] + tmp
    servCloudlet = curCloudlet
    R_i += 1


# use RNP_policy
R_i = 0
for index in range(len(position_states) - 30, len(position_states) - 1):
    curCloudlet = getCloudlet(s_lat_long[position_states[index] - 1][0], s_lat_long[position_states[index] - 1][1], cloudletPositions)
    print "curCloudlet = "
    print curCloudlet
    r = getDistance(s_lat_long[position_states[index] - 1][0], s_lat_long[position_states[index] - 1][1], clP[curCloudlet][0], clP[curCloudlet][1])
    T_avg = ((R - r) / v + (R + r) / v) / 2
    T_avg = math.pi
    #definition of alpha(T(Ci)).
    alpha = 0
    print Time[curCloudlet - 1] > T_avg
    print Time[curCloudlet - 1]
    if Time[curCloudlet - 1] > T_avg:
        alpha = 1
    else:
        alpha = math.exp(Time[curCloudlet] - T_avg)
    print "alpha = " + str(alpha)
    rou = alpha * E * (cloudletHop[curCloudlet - 1][servCloudlet - 1])
    R = np.zeros((2, 13 * 13, 13 * 13))

    #definition of Rg(r)
    Rg = math.pow(belta, -c) * r
    #definition of cloudlet load.
    epsilon = math.exp(-2 * math.pi * tao * Rg)

    for C in range(1, 14):
        for C2 in range(1, 14):
            if Time[C2 - 1] > T_avg:
                alpha = 1
            else:
                alpha = math.exp(Time[C2 - 1] - T_avg)
            rou = alpha * E * cloudletHop[C - 1][C2 - 1]
            R[1][(C- 1) * 13 + C2 - 1][(C2 - 1) * 13 + C2 - 1] = cloudletHop[C2 - 1][C - 1] * epsilon * alpha * (rou - thita)
    for i in range(13 * 13):
        RNP_policy[i] = random.randint(0, 1)
    if R_i > 0:
        tmp = RNP_R[R_i - 1]
    else:
        tmp = 0
    if RNP_policy[(servCloudlet - 1) * 13 + curCloudlet - 1] == 1:
        RNP_R[R_i] = R[1][(servCloudlet - 1) * 13 + curCloudlet - 1][(curCloudlet - 1) * 13 + curCloudlet - 1] + tmp
        servCloudlet = curCloudlet
    else:
        RNP_R[R_i] = tmp

    R_i += 1
RNP_R.pop()
AMP_R.pop()
NMP_R.pop()
MDP_R.pop()

print "result is below:"
print RNP_R
print AMP_R
print NMP_R
print MDP_R

point_count = [i for i in range(0, 29)]
print point_count

plt.plot(point_count, RNP_R, 'b*')
plt.plot(point_count, RNP_R, 'r')
plt.plot(point_count, RNP_R, color='red', linewidth=2, linestyle="-", label="RNP_policy")
plt.plot(point_count, AMP_R, 'b*')
plt.plot(point_count, AMP_R, 'b')
plt.plot(point_count, AMP_R, color='black', linewidth=2, linestyle="-", label="MDP_policy")
plt.plot(point_count, NMP_R, 'b*')
plt.plot(point_count, NMP_R, 'g')
plt.plot(point_count, NMP_R, color='green', linewidth=2, linestyle="-", label="NMP_policy")
plt.plot(point_count, MDP_R, 'b*')
plt.plot(point_count, MDP_R, 'm')
plt.plot(point_count, MDP_R, color='magenta', linewidth=2, linestyle="-", label="AMP_policy")

plt.xlabel('point counts')
plt.ylabel('Total Reward')
plt.ylim(0, 50)
plt.title('different policy reward')
plt.legend()
plt.show()
