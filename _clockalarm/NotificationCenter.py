import threading

from _clockalarm.UI import NotificationPopup


class NotificationCenter:
    _popup_queue = []
    _lock = threading.RLock()

    def __init__(self):
        super(NotificationCenter, self).__init__()

    def display(self, notification):
        """display QWidget"""
        popup = NotificationPopup(notification)

        self._lock.acquire()
        self._popup_queue.append(popup)
        self._popup_queue[0].show()
        self._lock.release()
