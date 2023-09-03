#!/usr/bin/env python3
#
#  outputs.py
"""
Functions to output as CSV or to print to the terminal.
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
import locale
from typing import List, Tuple

# 3rd party
from domdf_python_tools.dates import is_bst

__all__ = ["console", "csv"]


def csv(charging_periods: List[Tuple[float, datetime.datetime, datetime.datetime, float]]) -> str:
	"""
	Format the charging periods as comma-separated values.

	:param charging_periods:
	"""

	output = []
	output.append('kWh,"Cost (p)",Start,End')

	for (total, start, end, price) in reversed(charging_periods):
		# if total > 0.005:
		if total > 0.01:
			if is_bst(start.timetuple()):
				start += datetime.timedelta(hours=1)
			if is_bst(end.timetuple()):
				end += datetime.timedelta(hours=1)

			output.append(f'{total},{price:.2f},"{start:%a %d %B %Y %X}","{end:%a %d %B %Y %X}"')

	return '\n'.join(output)


def console(charging_periods: List[Tuple[float, datetime.datetime, datetime.datetime, float]]) -> None:
	"""
	Print the charging periods to the terminal.

	:param charging_periods:
	"""

	for (total, start, end, price) in charging_periods:
		# if total > 0.005:
		if total > 0.01:
			if is_bst(start.timetuple()):
				start += datetime.timedelta(hours=1)
			if is_bst(end.timetuple()):
				end += datetime.timedelta(hours=1)

			if price >= 100:
				price_formatted = locale.currency(price / 100)
			else:
				price_formatted = f"{price:.2f} p"

			print(
					f"{total:0.3f}",
					"kWh",
					price_formatted,
					f"{start:%a %d %B %Y %X} - {end:%a %d %B %Y %X} ({end-start})"
					)
