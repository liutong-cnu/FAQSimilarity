#!/usr/bin/env python
#encoding=utf8
'''
  Author: liutong liutong@cmos.chinamobile.com
  create@2019-03-20 16:48:20
'''
with open("res") as f:
    for line in f.readlines():
        print(line.split()[0])
