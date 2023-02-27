# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os
import pandas as pd
import glob


def multiple_files_in_one(path):
    # creating a list of files to combine
    os.chdir(path)
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    # combine all files in the list
    combined_csv = pd.DataFrame(pd.concat([pd.read_csv(f) for f in all_filenames]))

    # return data frame with all data
    return combined_csv


def time_manipulation(data_base):
    # convert two columns with strings about starting and ending time of trip into DataTime
    data_base['started_at'] = pd.to_datetime(data_base['started_at'])
    data_base['ended_at'] = pd.to_datetime(data_base['ended_at'])
    # count trip time and convert it into seconds
    data_base['time_of_ride'] = data_base.ended_at - data_base.started_at
    # add column with trip time in seconds
    data_base['time_of_seconds'] = data_base['time_of_ride'].dt.total_seconds()
    # add column with number of the month of trip
    data_base['month_of_ride'] = pd.DatetimeIndex(data_base['ended_at']).month
    # add column with number of the day of trip
    data_base['day_of_ride'] = pd.DatetimeIndex(data_base['ended_at']).dayofweek

    return data_base


def trim(data_base):
    # discarding data which we will not use in the future analyses
    clear_data = data_base.drop(
        columns=['ride_id', 'start_lat', 'start_lng', 'end_lat', 'end_lng', 'end_station_id',
                 'start_station_id', 'started_at', 'ended_at', 'time_of_ride'])
    return clear_data


def members(data_base):
    # forming  new data frames one for 'members' profile
    memebers = pd.DataFrame(data_base.loc[(data_base['member_casual'] == 'member')])

    return memebers


def casual(data_base):
    # forming  new data  for 'casual' profile

    casual = pd.DataFrame(data_base.loc[(data_base['member_casual'] == 'casual')])
    return casual


data_base = multiple_files_in_one('/Users/maksimgorskov/Downloads/byckes/')
full_data = pd.DataFrame(time_manipulation(data_base))
clean_data = trim(full_data)
mem_data = members(clean_data)
cas_data = casual(clean_data)
mem_data.to_csv('members.csv', index=False, encoding='utf-8')
cas_data.to_csv('casual.csv', index=False, encoding='utf-8')
