#!/user/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'baolingfeng'

import mysql.connector
import dao


class DBInterface:

    def __init__(self, host_in, user_in, pwd_in, db_in):
        try:
            self.conn = mysql.connector.connect(user=user_in,
                                            password=pwd_in,
                                            host=host_in,
                                            database=db_in)
        except mysql.connector.Error as err:
            print err

    def close(self):
        self.conn.close()

    def get_log_events(self, name):
        res = []
        try:
            cursor = self.conn.cursor()
            query = "select * from v_log_events_"+name
            cursor.execute(query)
            rs = cursor.fetchall()

            for rec in rs:
                e = dao.LogEvent()
                e.timestamp = rec[1]
                e.event_name = rec[2]
                e.pos_x = rec[3]
                e.pos_y = rec[4]
                e.window_name = rec[5]
                e.process_name = rec[6]
                e.parent_window = rec[7]
                e.win_rect_left = rec[8]
                e.win_rect_top = rec[9]
                e.win_rect_right = rec[10]
                e.win_rect_bottom = rec[11]
                e.has_screenshot = rec[12]
                e.has_acc = rec[13]
                e.type = rec[14]

                if e.has_acc:
                     e.mouse_action = self.get_ui_action(name, rec[0])

                res.append(e)

        except mysql.connector.Error as err:
            print err

        return res

    def get_ui_action(self, name, eid):
        try:
            cursor = self.conn.cursor()
            query = "select * from mouse_event_action_"+name+" where id = %d" % eid
            cursor.execute(query)

            rs = cursor.fetchall()

            for rec in rs:
                e = dao.MouseAction()
                e.action_name = rec[1]
                e.action_type = rec[2]
                e.action_value = rec[3]
                e.action_parent = rec[4]
                e.action_parent_type = rec[5]
                e.bound_left = rec[6]
                e.bound_top = rec[7]
                e.bound_right = rec[8]
                e.bound_bottom = rec[9]
                cursor.close()
                return e

        except mysql.connector.Error as err:
            print err

    def get_distinct_process(self, name):
        procs = []
        try:
            cursor = self.conn.cursor()
            query = "select distinct process_name from mouse_event_"+name
            cursor.execute(query)

            rs = cursor.fetchall()
            for inst in rs:
                procs.append(inst[0])

        except mysql.connector.Error as err:
            print err

        return procs

if __name__ == '__main__':
    db = DBInterface('127.0.0.1', 'root', '123456','datacollect');

    db.get_ui_action("sample")

    db.close()

