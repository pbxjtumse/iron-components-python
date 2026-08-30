from abc import ABC, abstractmethod
from datetime import datetime


class Clock(ABC):
    """时间源抽象。

    技术组件不应直接依赖 datetime.now() 获取当前时间，
    而是通过 Clock 获取，从而允许测试时替换时间源。
    """

    @abstractmethod
    def now(self) -> datetime:
        """返回当前时间。"""
        raise NotImplementedError