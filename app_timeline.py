#!/user/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'baolingfeng'

import DBInterface
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import util

def plot_app_timeline(name):
    db = DBInterface.DBInterface('127.0.0.1', 'root', '123456','datacollect');
    rs = db.get_log_events(name)
    #procs = db.get_distinct_process(name)

    apps = util.get_clear_apps(rs)

    times = []
    values = []
    node_set = set()
    for app in apps:
        temp_arr = app[0].split(' - ')

        if temp_arr[0] == 'Eclipse':
            node_set.add(temp_arr[0] + ' - ' + temp_arr[1])
        else:
            node_set.add(temp_arr[0])

        times.append(datetime.datetime.strptime(app[1], "%Y-%m-%d-%H-%M-%S-%f"))

    node_arr = list(node_set)
    node_arr.sort()
    print node_arr

    for app in apps:
        for v, n in enumerate(node_arr):
            if app[0].find(n)>=0:
                break

        values.append(v)

    times = mdates.date2num(times)

    fig, ax = plt.subplots()

    #y_pos = np.arange(len(node_arr))
    #ax.xticks(y_pos, node_arr)
    plt.plot_date(times, values)
    plt.show()


plot_app_timeline('lj_gui')
