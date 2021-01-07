from abc import ABC, abstractmethod

from observer_impl.subject_interface import subject_interface


class observer_interface(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: subject_interface) -> None:
        """
        Receive update from subject.
        """
        pass