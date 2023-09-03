#!/usr/bin/env python3
#
#  config.py
"""
Parse configuration files.
"""
#
#  Copyright © 2023 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from typing import List

# 3rd party
import attr
import tomli
from domdf_python_tools.paths import PathPlus

# this package
from car_charging.influxdb import InfluxDBConfig
from car_charging.tariff import Tariff

__all__ = ["Config"]


@attr.define
class Config:
	"""
	Configuration for this library.
	"""

	#: The configuration for InfluxDB.
	influxdb: InfluxDBConfig

	#: The list of tariffs (minimum 1 tariff).
	tariffs: List[Tariff]

	@classmethod
	def load(cls, filename: PathPlus) -> "Config":
		"""
		Load a :class:`~.Config` from a TOML file.
		"""

		config = tomli.loads(filename.read_text())
		tariffs_toml = config["tariffs"]
		tariffs = [Tariff.from_dict(tariff) for tariff in tariffs_toml.values()]

		return cls(
				config["influxdb"],
				tariffs,
				)
