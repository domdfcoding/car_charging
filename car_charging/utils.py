#!/usr/bin/env python3
#
#  utils.py
"""
General utility functions.
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

# 3rd party
from domdf_python_tools.dates import is_bst
from domdf_python_tools.paths import PathPlus

__all__ = ["compensate_bst", "configure_locale"]

json_datafile = PathPlus("car_charging.json")


def compensate_bst(date: datetime.datetime) -> datetime.datetime:
	"""
	Apply a one hour offset to the time if it falls within British Summer Time.
	"""

	if is_bst(date.timetuple()):
		return date + datetime.timedelta(hours=1)

	return date


def configure_locale() -> None:
	"""
	Setup the :mod`locale` module to display 4 decimal places.
	"""

	locale.setlocale(locale.LC_ALL, '')

	# Set locale to have 4 decimal places (hundredth of a pence)
	locale._override_localeconv["int_frac_digits"] = 4  # type: ignore[attr-defined]
	locale._override_localeconv["frac_digits"] = 4  # type: ignore[attr-defined]
