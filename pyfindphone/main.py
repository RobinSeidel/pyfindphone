# -----------------------------------------------------------
# A python package to detect known phones in close proximity
#
# (C) 2022 Robin Seidel, Munich, Germany
# Released under MIT License
# Email: robin.seidel@tum.de
# -----------------------------------------------------------

import subprocess
from typing import Callable

from apscheduler.schedulers.background import BlockingScheduler


class PhoneFinder:

    scheduler = BlockingScheduler()

    def __init__(
        self,
        mac_address: str,
        callback: Callable,
        interval: int = 15,
        on_change: bool = True,
    ):
        self.callback = callback
        self.mac_address = mac_address
        self.callback = callback
        self.interval = interval
        self.on_change = on_change
        self.device_name = ""

    def __get_device_name(self) -> str:
        device_name = subprocess.run(
            ["hcitool", "name", self.mac_address], stdout=subprocess.PIPE
        ).stdout
        return device_name.decode("utf-8").strip()

    def __detect_phone_on_change(self):
        device_name = self.__get_device_name()

        if device_name == self.device_name:
            return

        self.callback(device_name != "", self.mac_address, device_name)
        self.device_name = device_name

    def __detect_phone_always(self):
        device_name = self.__get_device_name()
        self.callback(device_name != "", self.mac_address, device_name)

    def start(self):
        if self.on_change:
            self.scheduler.add_job(
                self.__detect_phone_on_change, "interval", seconds=self.interval
            )
        else:
            self.scheduler.add_job(
                self.__detect_phone_always, "interval", seconds=self.interval
            )

        self.scheduler.start()
