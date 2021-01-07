from abc import ABC, abstractmethod

from observer_impl import observer_interface


class subject_interface(ABC):
    """
     The Subject interface declares a set of methods for managing subscribers.
     """

    @abstractmethod
    def attach(self, observer: observer_interface) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: observer_interface) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass
    @abstractmethod
    def remove_object_from_queue(self) -> None:
        pass