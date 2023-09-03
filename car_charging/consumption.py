#!/usr/bin/env python3
#
#  consumption.py
"""
Models electricity consumption.
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
import datetime
from typing import List, TypedDict

# 3rd party
from domdf_python_tools.paths import PathPlus

__all__ = ["Consumption", "from_json", "to_json"]


class Consumption(TypedDict):
	"""
	Represents electricity consumption for a 20s window in time.
	"""

	#: The consumption in Watt hours.
	value: float

	#: The start date and time of the 20s window.
	start_time: datetime.datetime


def to_json(consumption_data: List[Consumption], filename: PathPlus) -> None:
	"""
	Write a JSON representation of consumption data to a file.

	:param consumption_data:
	:param filename:
	"""

	output_data = []
	for period_data in consumption_data:
		output_data.append({
				"value": period_data["value"],
				"start_time": period_data["start_time"].isoformat(),
				})

	filename.dump_json(output_data)


def from_json(filename: PathPlus) -> List[Consumption]:
	"""
	Parse consumption data from a JSON file.

	:param filename:
	"""

	consumption_data = filename.load_json()  # List

	for period in consumption_data:
		period["start_time"] = datetime.datetime.fromisoformat(period["start_time"])

	return consumption_data
