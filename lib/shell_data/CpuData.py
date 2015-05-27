#!/usr/bin/env python
#-*- coding:utf-8 -*-

import simplejson as json
import time

while True:
    now_data = {} # ��ǰ /proc/stat ��ֵ
    last_data = {} # ��һ�� /proc/stat ��ֵ��ʱ�����㹻��
    
    # ��ȡ��ǰ����
    raw_data = file('/proc/stat').readlines()
    results = raw_data[0].strip()
    cpu_all =results.split()
    cpu_all.pop(0)
    cpu_data = [int(i) for i in cpu_all]
    now_data['idle'] = cpu_data[3]
    now_data['total'] = sum(cpu_data)
    
    # ��ȡ��ʷ����
    try:
        raw_data = file('/tmp/proc_stat').read()
        last_data = json.loads("%s" % raw_data.strip())
    except:
        last_data = now_data
    
    # ���浱ǰ���ݵ���ʷ���ݱ���
    fp = file('/tmp/proc_stat', 'w')
    fp.write(json.dumps(now_data))
    fp.close()
    
    # �����������ݣ��õ�Ҫ�����ֵ
    results = {}
    diff_total = int(now_data['total'])-int(last_data['total'])
    diff_idle=(int(now_data['idle'])-int(last_data['idle']))
    if diff_total > 0:
        results['cpuuse']=int(round(100*(float(diff_total-diff_idle)/diff_total)))
    else:
        # ��һ�μ��ص�ʱ����ʷ����Ϊ�գ��޷����㣬 ���г�ʼ��Ϊ0
        results['cpuuse']=0 
    print results
    time.sleep(1)