#!/usr/bin/env python3
#
#  __init__.py
"""
Utilities for reading car charger consumption via InfluxDB.
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

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2023 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.0.0"
__email__: str = "dominic@davis-foster.co.uk"

# stdlib
import datetime
from typing import Any, Dict, List, Tuple

# 3rd party
import scipy.ndimage  # type: ignore[import]

# this package
from car_charging.influxdb import tele_period
from car_charging.tariff import Tariff
from car_charging.utils import compensate_bst

__all__ = ["calculate_charging_periods"]


def calculate_charging_periods(
		consumption_data: List[Dict[str, Any]],
		tariffs: List[Tariff],
		) -> List[Tuple[float, datetime.datetime, datetime.datetime, float]]:
	"""
	Detect car charging periods from electricity consumption data.

	:param consumption_data:
	:param tariffs:
	"""

	all_values = []
	period_start_times = []

	for period in consumption_data:
		all_values.append(period["value"])
		period_start_times.append(datetime.datetime.fromisoformat(period["start_time"]))

	period_rates = []
	for the_date in period_start_times:
		the_date = compensate_bst(the_date)
		the_time = the_date.time()
		for tariff in tariffs:
			if tariff.start_date is None and tariff.end_date is not None and the_date < tariff.end_date:
				break
			elif tariff.start_date is not None and tariff.start_date <= the_date and tariff.end_date is None:
				break
			elif tariff.start_date is not None and tariff.end_date is not None and tariff.start_date <= the_date < tariff.end_date:
				break
		else:
			print(tariffs)
			print("No matching tariff for", the_date)
			print(tariffs[1].start_date)
			exit(1)

		# if tariff.night_start_time > tariff.night_end_time:
		# 	if the_time >= tariff.night_start_time:
		# 		the_rate = tariff.night_rate
		# 	elif the_time < tariff.night_end_time:
		# 		the_rate = tariff.night_rate
		# 	else:
		# 		the_rate = tariff.day_rate
		# else:
		# 	if tariff.night_start_time <= the_time < tariff.night_end_time :
		# 		the_rate = tariff.night_rate
		# 	else:
		# 		the_rate = tariff.day_rate

		# period_rates.append(the_rate)
		period_rates.append(tariff.get_rate(the_time))

	groups = scipy.ndimage.find_objects(scipy.ndimage.label(all_values)[0])
	charging_sums = [sum(all_values[x[0]]) / 1000 for x in groups]
	charging_start_ends: List[Tuple[datetime.datetime, datetime.datetime]] = [
			(period_start_times[x[0]][0], period_start_times[x[0]][-1] + tele_period) for x in groups
			]  # 20 second teleperiod
	charging_costs = []

	for x in groups:
		rates_in_group = period_rates[x[0]]
		consumptions_in_group = all_values[x[0]]
		cost_for_group = sum([r * (c / 1000) for r, c in zip(rates_in_group, consumptions_in_group)])
		charging_costs.append(cost_for_group)

	charging_periods: List[Tuple[float, datetime.datetime, datetime.datetime, float]] = []

	# Ignore gaps of 1 teleperiod
	for total, (start, end), price in zip(charging_sums, charging_start_ends, charging_costs):

		if charging_periods:
			last_period = charging_periods[-1]  # (total, start, end, price)

			if start - tele_period == last_period[2]:  # 2 = end time
				# merge this period into the previous one
				charging_periods[-1] = (
						last_period[0] + total,
						last_period[1],  # 1 = start time
						end,
						last_period[3] + price,  # 3 = price
						)
				continue

		charging_periods.append((total, start, end, price))

	return charging_periods
