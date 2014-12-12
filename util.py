#!/user/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'baolingfeng'
import re

PROCESS_MAP = {'WINWORD.EXE':'Microsoft Word', 'javaw.exe':'Eclipse', 'eclipse.exe':'Eclipse',
               'chrome.exe':'Google Chrome','firefox.exe':'Mozilla Firefox','iexplore.exe':'Internet Explorer', 'explorer.exe':'Windows Explorer'}

APPS = ['Word','Microsoft Word','Eclipse','Google Chrome', 'Mozilla Firefox', 'Internet Explorer', 'Windows Explorer']

ECLIPSE_VIEWS = ['Project Explorer','Package Explorer', 'Console', 'Outline','Search', 'Problems', 'Variables', 'Breakpoints', 'Error Log']

COLOR_MAP = {'Eclipse':'r', 'Microsoft Word':'b', 'Google Chrome':'#00ff00', 'Mozilla Firefox':'#00aa00','Internet Explorer':'#007700', \
            'Windows Explorer':'k'}

def get_app_name(process):
    if PROCESS_MAP.has_key(process):
        return PROCESS_MAP[process]
    else:
        return "Undefined Application - " + process

def is_running_jedit(mouse_action):
    m1 = re.search(r'^jEdit - .+', mouse_action.action_name)
    m2 = re.search(r'^jEdit - .+', mouse_action.action_parent)
    if m1 != None and mouse_action.action_type == 'window' or \
        m2 != None and mouse_action.action_parent_type == 'window':
        return True

    if mouse_action.action_name == 'jEdit Help' or mouse_action.action_parent == 'jEdit Help':
        return True

    return False

def is_run_java_application(mouse_action, pre_view):
    if mouse_action.action_name[0:3] == 'Run' and mouse_action.action_type == 'split button':
        return True

    if mouse_action.action_parent == 'Select Java Application' and pre_view == "Run Java Application":
        return True

    if mouse_action.action_type == 'menu item' and mouse_action.action_name == 'Run As':
        return True

    if mouse_action.action_type == 'menu item' and mouse_action.action_name.find('Alt+Shift+X')>0:
        return True

    return False

def is_debug_java_application(mouse_action, pre_view):
    if mouse_action.action_name[0:5] == 'Debug' and mouse_action.action_type == 'split button':
        return True

    if mouse_action.action_parent == 'Select Java Application' and pre_view == "Debug Java Application":
        return True

    if mouse_action.action_type == 'menu item' and mouse_action.action_name == 'Debug As':
        return True

    if mouse_action.action_type == 'menu item' and mouse_action.action_name.find('Alt+Shift+D')>0:
        return True

    return False

def get_eclipse_view(mouse_action, pre_view):
    if mouse_action.action_parent in ECLIPSE_VIEWS:
        idx = ECLIPSE_VIEWS.index(mouse_action.action_parent)
        return ECLIPSE_VIEWS[idx]

    m = re.search(r'.+\.java$',mouse_action.action_parent)
    if m != None:
        return "Code Editor - " + mouse_action.action_parent

    if is_running_jedit(mouse_action):
        return "JEdit"

    if is_run_java_application(mouse_action, pre_view):
        return "Run Java Application"

    if is_debug_java_application(mouse_action, pre_view):
        return "Debug Java Application"

    print "Not Defined: "+ mouse_action.action_name + '/' + mouse_action.action_type + '#' + mouse_action.action_parent
    return pre_view

def is_browser(process):
    return process in ['firefox.exe','chrome.exe','iexplore.exe']

def get_web_page_title(e):
    app_name = PROCESS_MAP[e.process_name]
    win_name = e.window_name
    if app_name == 'Google Chrome' and e.window_name == 'Chrome Legacy Window':
        win_name = e.parent_window

    idx = win_name.find(" - " + app_name)
    if idx > 0:
        return win_name[0:idx]
    else:
        return win_name

def get_taskbar_app(control_name):
    idx = control_name.rfind(' - ')
    if idx >=0:
        app_name = control_name[idx+3:]
        if app_name in APPS:
            return app_name

    if control_name[0:7] == 'jEdit -':
        return "jEdit"

    return "Undefined Application - " + control_name

def get_clear_apps(rs):
    apps = []
    pre_view = None
    for r in rs:
        if r.has_acc and r.mouse_action != None:
            if r.process_name == 'explorer.exe' and r.window_name == 'Running applications':
                continue;
                #app_name = util.get_taskbar_app(r.mouse_action.action_name)

            app_name = get_app_name(r.process_name)

            if r.process_name == 'javaw.exe' or r.process_name == 'eclipse.exe':
                view = get_eclipse_view(r.mouse_action, pre_view)
                app_name = app_name + ' - ' + view
                pre_view = view
            elif is_browser(r.process_name):
                app_name = app_name + ' - ' + get_web_page_title(r)

            apps.append((app_name, r.timestamp))

    return apps