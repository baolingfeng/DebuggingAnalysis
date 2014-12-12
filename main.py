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

log_name = "ydh_gui"
db = DBInterface.DBInterface('127.0.0.1', 'root', '123456','datacollect');
rs = db.get_log_events(log_name)
procs = db.get_distinct_process(log_name)
print procs

actions = []
eclipse_views = ['Package Explorer', 'Console', 'Outline', 'Search', 'Problems', 'Variables', 'Breakpoints', 'Error Log']
dates = []
values = []

apps = []

pre_view = None
for r in rs:
    if r.has_acc and r.mouse_action != None:
        #print r.mouse_action.action_parent
        if r.process_name == 'explorer.exe' and r.window_name == 'Running applications':
            continue;
            #app_name = util.get_taskbar_app(r.mouse_action.action_name)

        app_name = util.get_app_name(r.process_name)

        #print app_name
        if r.process_name == 'javaw.exe' or r.process_name == 'eclipse.exe':
            view = util.get_eclipse_view(r.mouse_action, pre_view)
            app_name = app_name + ' - ' + view
            pre_view = view
        elif util.is_browser(r.process_name):
            app_name = app_name + ' - ' + util.get_web_page_title(r)


        apps.append((app_name, r.timestamp))

app_stat = {}
eclipse_view_stat = {}
pre_app = None
aggr_apps = []
arr = []
for index,app in enumerate(apps):
    timestamp = datetime.datetime.strptime(app[1], "%Y-%m-%d-%H-%M-%S-%f")
    print timestamp.strftime('%H:%M:%S.%f'),app[0]

    interval = 0
    if index >= len(apps)-1:
        last_timestamp = datetime.datetime.strptime(rs[-1].timestamp, "%Y-%m-%d-%H-%M-%S-%f")
        interval = last_timestamp - timestamp
    else:
        next_timestamp = datetime.datetime.strptime(apps[index+1][1], "%Y-%m-%d-%H-%M-%S-%f")
        interval = next_timestamp - timestamp

    idx = app[0].find(' - ')
    if idx>=0:
        app_name = app[0][0:idx]
    else:
        app_name = app[0]

    if app_stat.has_key(app_name):
        app_stat[app_name] = app_stat[app_name] + interval
    else:
        app_stat[app_name] = interval

    if app_name == 'Eclipse':
        view = app[0][idx+3:]
        idx = view.find(' - ')
        if idx>=0:
            view = view[0:idx]

        if eclipse_view_stat.has_key(view):
            eclipse_view_stat[view] = eclipse_view_stat[view] + interval
        else:
            eclipse_view_stat[view] = interval

print eclipse_view_stat

#bar chart for application
# plt.figure(0)
# fig, ax = plt.subplots()
# values = [e.total_seconds()/60 for e in app_stat.values()]
# keys = app_stat.keys()
# x_pos = np.arange(len(keys))
#
# ax.bar(x_pos,values,0.35)
# plt.xticks(x_pos, keys)
# plt.ylabel('Total Time')

fig, ax2 = plt.subplots()
values = [e.total_seconds()/60 for e in eclipse_view_stat.values()]
keys = eclipse_view_stat.keys()
x_pos = np.arange(len(keys))

ax2.bar(x_pos,values,0.35)
plt.xticks(x_pos, keys, rotation=30)
plt.ylabel('Total Time')

plt.show()


#dates = mdates.date2num(dates)
#plt.plot_date(dates, values)
#plt.show()

db.close()