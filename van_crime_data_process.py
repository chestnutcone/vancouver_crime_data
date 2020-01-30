# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 19:36:14 2020

@author: Oliver
"""

import pandas as pd
import utm
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("crimedata_csv_all_years.csv")
print("original shape", df.shape)
total_cases = df.YEAR.value_counts()
total_cases.name = "Total Cases"
non_zero = df[(df.X != 0)]
non_zero.dropna(inplace=True)
print('non zero shape', non_zero.shape)
utm_locations = non_zero.iloc[:,-2:]
utm_locations['zone_number'] = [10]*utm_locations.shape[0]
utm_locations['zone_letter'] = ["N"]*utm_locations.shape[0]
utm_input = list(zip(utm_locations.X, utm_locations.Y,
                     utm_locations.zone_number, utm_locations.zone_letter))

lat_lon = [utm.to_latlon(*x) for x in utm_input]

non_zero['lat'] = [x[0] for x in lat_lon]
non_zero['lon'] = [x[1] for x in lat_lon]

# non_zero.to_pickle("vancouver_crime_data_years_cleaned.pickle")
non_zero = pd.read_pickle("vancouver_crime_data_years_cleaned.pickle")
non_zero = non_zero.sort_values(["YEAR", "MONTH", "DAY", "HOUR", "MINUTE"])

cleaned_cases = non_zero.YEAR.value_counts()
cleaned_cases.name = "With Location"
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,6))
total_cases.plot.bar(ax=ax, color='red')
cleaned_cases.plot.bar(ax=ax, color='blue')
ax.legend()
ax.set_title("Crime Data Points")
ax.set_xlabel("Year")
ax.set_ylabel("Counts")

aggregate_monthly = non_zero.MONTH.value_counts().sort_index()
cases_per_day = aggregate_monthly.divide([31,28.25,31,30,31,30,31,31,30,31,30,31])

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,6))
ax = cases_per_day.plot.bar(ax=ax)
ax.set_title("Cases per Day")
ax.set_xlabel("Month")
ax.set_ylabel("Cases")

aggregate_hourly = non_zero.HOUR.value_counts().sort_index()
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,6))
ax = aggregate_hourly.plot.bar(ax=ax)
ax.set_title("Cases per Hour")
ax.set_xlabel("Month")
ax.set_ylabel("Hour")

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,6))
aggregate_type = non_zero.TYPE.value_counts()
aggregate_type.name = ""
ax = aggregate_type.plot.pie(autopct="%.1f", pctdistance=0.8, ax=ax)
ax.set_title("Types of Crime")


yearly_types_of_crime = []

for i in range(2003,2020):
    yearly_types_of_crime.append(non_zero.loc[non_zero['YEAR'] == i].TYPE.value_counts())
yearly_types_df = pd.concat((yearly_types_of_crime), axis=1)
yearly_types_df.columns = [i for i in range(2003, 2020)]
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,6))
ax = yearly_types_df.T.plot.line(ax=ax)
ax.set_title("Types of Crime Over Time", fontsize=18)
ax.legend(bbox_to_anchor=(1.05, 1.05), fontsize=18)




    
    
