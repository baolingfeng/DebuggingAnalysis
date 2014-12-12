#!/user/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'baolingfeng'

class LogEvent:
    def __init__(self):
        self.timestamp = ""
        self.type = ""
        self.event_name = ""
        self.pos_x = -1
        self.pos_y = -1
        self.window_name = ""
        self.parent_window = ""
        self.process_name = ""
        self.win_rect_left = -1
        self.win_rect_top = -1
        self.win_rect_right = -1
        self.win_rect_bottom = -1
        self.has_screenshot = False
        self.has_acc = False
        self.mouse_action = None

class MouseAction:
    def __init__(self):
        self.timestamp = ""
        #self.event = None
        self.action_name = ""
        self.action_type = ""
        self.action_value = ""
        self.action_parent = ""
        self.action_parent_type = ""
        self.bound_left = -1
        self.bound_top = -1
        self.bound_right = -1
        self.bound_bottom = -1