#!/usr/bin/python
from getCloudlet import getCloudlet

cloudlet_num = 13

def readConfigFile():
   cloudlet_pos = []
   cloudlet_pos_file = open("cloudletPosition.txt")
   cloudlet_pos_lines = cloudlet_pos_file.readlines()
   for cloudlet_pos_line in cloudlet_pos_lines:
      cloudlet_pos_tmp = cloudlet_pos_line.split(' ')
      cloudlet_pos.append(((float)(cloudlet_pos_tmp[1]), (float)(cloudlet_pos_tmp[2])))
   return cloudlet_pos

def readInputFile():
   user_pos = []
   user_pos_file = open("user_position.txt")
   user_pos_lines = user_pos_file.readlines()
   
   for user_pos_line in user_pos_lines:
      user_pos_tmp = user_pos_line.split(' ')
      user_pos.append(((float)(user_pos_tmp[1]), (float)(user_pos_tmp[2])))
   return user_pos

def convertUserPosToCloudlet(user_pos, cloudlet_pos):
   user_cloudlet = []
   for i in range(len(user_pos)):
      user_cloudlet.append((int)(getCloudlet(user_pos[i][0], user_pos[i][1], cloudlet_pos) ))
   return user_cloudlet

def OneDMarkov():
   cloudlet_pos = readConfigFile()
   print "in OneDMarkov, cloudlet_pos is "
   print cloudlet_pos

   user_pos = readInputFile()
   print "in OneDMarkov, user_pos is "
   print user_pos

   user_cloudlet = convertUserPosToCloudlet(user_pos, cloudlet_pos)
   print "in OneDMarkov, user_cloudlet"
   print user_cloudlet

   cloudlet_convert = [[0 for i in range(cloudlet_num)] for j in range(cloudlet_num)]

   for i in range(len(user_pos) - 1):
      cloudlet_convert[user_cloudlet[i] - 1][user_cloudlet[i + 1] - 1] += 1

   return cloudlet_convert
