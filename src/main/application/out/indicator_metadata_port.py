from abc import ABC, abstractmethod


class IndicatorMetadataPort(ABC):

    @abstractmethod
    def find_indicator_metadata():
        pass

    @abstractmethod
    def age_bands():
        pass