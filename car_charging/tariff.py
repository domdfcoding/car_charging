#!/usr/bin/env python3
#
#  tariff.py
"""
Models an electricity tariff with different rates for day and night time.
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
from typing import Any, Dict, Optional

# 3rd party
import attr

# this package
from car_charging.utils import compensate_bst

__all__ = ["Tariff"]


@attr.define
class Tariff:
	"""
	Models an electricity tariff with different rates for day and night time.
	"""

	#: The start time for the night electricity rate.
	night_start_time: datetime.time

	#: The end time for the night electricity rate.
	night_end_time: datetime.time

	#: The daytime electricity rate.
	day_rate: float

	#: The nighttime electricity rate.
	night_rate: float

	#: The date (and time) this tariff started.
	start_date: Optional[datetime.date] = attr.field(default=None)

	#: The date (and time) this tariff ended.
	end_date: Optional[datetime.date] = attr.field(default=None)

	def get_rate(self, time: datetime.time) -> float:
		"""
		Return the rate (day/night) in ``p/kWh`` for the given time.

		:param time:
		"""

		if self.night_start_time > self.night_end_time:
			if time >= self.night_start_time:
				return self.night_rate
			elif time < self.night_end_time:
				return self.night_rate
			else:
				return self.day_rate

		if self.night_start_time <= time < self.night_end_time:
			return self.night_rate
		else:
			return self.day_rate

	@classmethod
	def from_dict(cls, d: Dict[str, Any]) -> "Tariff":
		"""
		Construct a :class:`~.Tariff` from a dictionary representation.

		:param d:
		"""

		if "start_date" in d:
			start_date = compensate_bst(d["start_date"].replace(tzinfo=datetime.timezone.utc))
		else:
			start_date = None

		if "end_date" in d:
			end_date = compensate_bst(d["end_date"].replace(tzinfo=datetime.timezone.utc))
		else:
			end_date = None

		return cls(
				d["night_start_time"],
				d["night_end_time"],
				d["day_rate"],
				d["night_rate"],
				start_date=start_date,
				end_date=end_date,
				)
