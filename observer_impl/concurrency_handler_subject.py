from threading import Lock

from observer_impl.observer_interface import observer_interface
from observer_impl.subject_interface import subject_interface


class concurrency_handler_subject(subject_interface):
    """
    The Subject owns some important state and notifies observers when the state
    changes.
    """
    def __init__(self) -> None:
        self._objects_waiting_in_queue_counter = 0
        self._objects_waiting_in_queue = []
        self._observer = None
        self.mutex = Lock()

    def attach(self, observer: observer_interface) -> None:
        self._observer = observer

    def detach(self, observer: observer_interface) -> None:
        self._observer.remove = observer

    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """

        self._observer.update(self)

    def add_object_to_queue(self,object):
        """

        :return:
        """
        self.mutex.acquire()
        self._objects_waiting_in_queue_counter += 1
        self._objects_waiting_in_queue.append(object)
        self.mutex.release()
        self.notify()

    def remove_object_from_queue(self):
        """

        :return:
        """
        self.mutex.acquire()
        self._objects_waiting_in_queue_counter -= 1
        first_in_line = self._objects_waiting_in_queue.pop(0)
        self.mutex.release()
        return first_in_line