#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt


states= open('user_position.txt')
positions = states.readlines() 
position_states = []
totalPositionCount = 18
s_lat_long = {}
for position in positions:
    position_detail = position.split(' ')
    position_states.append((int)(position_detail[0]))
    s_lat_long[(int)(position_detail[0]) - 1] = ((float)(position_detail[1]), (float)(position_detail[2])) 

print "s_lat_long"
print s_lat_long
print "position_states"
print position_states
print "totalPositionCount"
print totalPositionCount

statePre = [[0 for col in range((int)(totalPositionCount) )] for row in range((int)(totalPositionCount) )] 
prob = []
prob.append(0)

j = 0
intervals = 20
pre_intervals = 10
count = 0
print len(position_states)
for j in range(0, (int)(len(position_states) / intervals)):
   for i in range(j * intervals, min(j * intervals + intervals - 1, (int)(len(position_states) - 1))):
      statePre[(int)(position_states[i]) - 1][(int)(position_states[i + 1] - 1)] += 1
   count = 0
   tmp_pre_intervals = min(pre_intervals, len(position_states) - (j + 1) * intervals)
   for k in range(0, tmp_pre_intervals): 
      pre = statePre[(int)(position_states[k + j * intervals + intervals - 1]) - 1]
      if pre[(int)(position_states[j * intervals + intervals + k]) - 1] >= max(pre):
         count += 1
   prob.append((float)(count) / tmp_pre_intervals)

#prob[8] = 0.7
#prob[9] = 0.8
print prob

point_count = [i * 20 for i in range(0, 10)]
print point_count

plt.plot(point_count, prob, 'b*')
plt.plot(point_count, prob, 'r')
plt.xlabel('learning basic points')
plt.ylabel('accuracy')
plt.ylim(0,1)
plt.title('1-D markov prediction model')
plt.legend()
plt.show()

