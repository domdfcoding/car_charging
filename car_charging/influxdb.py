#!/usr/bin/env python3
#
#  influxdb.py
"""
Interface to InfluxDB.
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
from typing import List

# 3rd party
from influxdb_client import InfluxDBClient  # type: ignore[import]

# this package
from car_charging import consumption
from car_charging.config import Config

__all__ = ["update_consumption_data"]

tele_period = datetime.timedelta(seconds=20)


def update_consumption_data(config: Config) -> List[consumption.Consumption]:
	"""
	Update the cached consumption data from InfluxDB.

	:param config:
	"""

	influxdb_config = config.influxdb
	json_datafile = config.datafile

	consumption_data: List[consumption.Consumption]

	if json_datafile.is_file():
		consumption_data = consumption.from_json(json_datafile)
		latest_period = consumption_data[-1]["start_time"]
	else:
		consumption_data = []
		latest_period = datetime.datetime(year=2022, month=9, day=18, tzinfo=datetime.timezone.utc)
		# latest_period = datetime.datetime(year=2023, month=8, day=14)

	with InfluxDBClient(
			url=influxdb_config["host"], token=influxdb_config["token"], org=influxdb_config["org"]
			) as client:

		query = f"""
	from(bucket: "telegraf")
	|> range(start: {latest_period.isoformat()}, stop: {(datetime.datetime.now()-datetime.timedelta(hours=1)).isoformat().split('.')[0]}Z)
	|> filter(fn: (r) => r["topic"] == "{influxdb_config["topic"]}")
	|> filter(fn: (r) => r["_field"] == "{influxdb_config["field"]}")
	|> aggregateWindow(every: 20s, fn: sum, createEmpty: false)
	"""

		# print(query)

		tables = client.query_api().query(query)
		# output = tables.to_json(indent=5)

		for x in tables[0]:
			# print(x)
			consumption_data.append({
					"value": x.values.get("_value"),
					"start_time": x.values.get("_time"),
					})

		consumption.to_json(consumption_data, json_datafile)

	return consumption_data
