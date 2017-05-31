# ClockAlarm is a cross-platform alarm manager
# Copyright (C) 2017  Loïc Charrière, Samuel Gauthier
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time

from tinydb import TinyDB, Query

from _clockalarm import Notification
from _clockalarm.SimpleAlert import SimpleAlert
from _clockalarm.utils import importExportUtils


class AlertCollection(object):
    """Collection of all the Alert objects running on the program.

    This class contains utilities to load, update and save the alerts in a TinyDB database, and maintain the correct
    state of all the alerts

    """

    def __init__(self, parent=None):
        """Default constructor for AlertCollection object

        Attributes:
            parent (main.App, optional): Parent of the class

        Exceptions:
            ValueError: If the parent argument is not None but isn't an instance of _clockalarm.main.App

        """
        super(self.__class__, self).__init__()
        import _clockalarm.main
        if parent and not isinstance(parent, _clockalarm.main.App):
            raise ValueError("parent argument is set but isn't an instance of _clockalarm.main.App")
        self.parent = parent
        self.db = TinyDB(importExportUtils.ALERT_DB_PATH, default_table="alerts")
        self.alert_list = []
        self.clean_db()
        self.load_db()
        self.display()

    def add(self, alert: SimpleAlert):
        """

        :param alert:
        :return:
        """
        self.alert_list.append(alert)
        if self.parent:
            alert.timeout.connect(self.parent.notification_center.add_to_queue)
        alert.id = self.db.insert(
            {'trigger_time': alert.trigger_time,
             'message': alert.get_notification().get_message(),
             'color_hex': alert.notification.color_hex,
             'font_family': alert.notification.font_family,
             'font_size': alert.notification.font_size,
             'sound': alert.notification.sound,
             'periodicity': alert.periodicity})
        self.display()

    def edit(self, id_alert: int, notification: Notification = None,
             trigger_time: int = None, periodicity: int = None):
        """

        :param id_alert:
        :param notification:
        :param trigger_time:
        :param periodicity:
        :return:
        """
        alert_to_edit = next(alert for alert in self.alert_list
                             if alert.id == id_alert)
        if alert_to_edit:
            if notification:
                alert_to_edit.notification = notification
                self.db.update({'message': notification.message,
                                'color_hex': notification.color_hex,
                                'font_family': notification.font_family,
                                'font_size': notification.font_size,
                                'sound': notification.sound}, eids=[id_alert])
            if periodicity:
                alert_to_edit.periodicity = periodicity
                self.db.update({'periodicity': alert_to_edit.periodicity},
                               eids=[id_alert])
            if trigger_time:
                alert_to_edit.trigger_time = trigger_time
                self.db.update({'trigger_time': alert_to_edit.trigger_time},
                               eids=[id_alert])
            self.display()

    def delete(self, id_alert: int):
        """

        :param id_alert:
        :return:
        """
        self.alert_list = [alert for alert in self.alert_list
                           if alert.id != id_alert]
        self.db.remove(eids=[id_alert])
        self.display()

    def check_timers(self, trig_time):
        """

        :param trig_time:
        :return:
        """
        for alert in self.alert_list:
            if trig_time >= alert.trigger_time:
                alert.triggered()
                if not alert.periodicity:
                    self.delete(alert.get_id())
                else:
                    self.edit(alert.get_id(),
                              trigger_time=alert.get_trigger_time() +
                                           alert.get_periodicity())

    def display(self):
        """

        :return:
        """
        if self.parent:
            self.parent.main_window.alert_list_widget.actualize(self.alert_list)

    def load_db(self):
        """

        :return:
        """
        for alert in self.db.all():
            notification = Notification(alert["message"],
                                        color_hex=alert["color_hex"],
                                        font_family=alert["font_family"],
                                        font_size=alert["font_size"],
                                        sound=alert["sound"])
            new_alert = SimpleAlert(alert["trigger_time"], notification)
            if "periodicity" in alert:
                new_alert.periodicity = alert["periodicity"]
            new_alert.id = alert.eid

            self.alert_list.append(new_alert)
            if self.parent:
                new_alert.timeout.connect(self.parent.notification_center.add_to_queue)

    def save_db(self):
        """

        :return:
        """
        self.db.purge()
        for alert in self.alert_list:
            self.db.insert({'trigger_time': alert.trigger_time,
                            'message': alert.get_notification().get_message(),
                            'font_family': alert.notification.font_family,
                            'font_size': alert.notification.font_size,
                            'color_hex': alert.notification.color_hex,
                            'sound': alert.notification.sound,
                            'periodicity': alert.periodicity})

    def clean_db(self):
        """

        :return:
        """

        def operation():
            def transform(element):
                trig = element['trigger_time']
                while trig < time.time():
                    trig += element['periodicity']
                element['trigger_time'] = trig

            return transform

        alert_query = Query()
        self.db.update(operation(), alert_query.periodicity != None)
        self.db.remove(alert_query.trigger_time <= time.time())
