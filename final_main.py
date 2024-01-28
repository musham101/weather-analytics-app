import pandas as pd
import numpy as np
import os, sys
from datetime import datetime

class Color:
    BLUE = '\033[94m'
    RED = '\033[91m'
    END = '\033[0m'

def show_chart(data):
    for _, value in data.iterrows():
        day = int(value['GST'].day)
        formatted_day = '{:02d}'.format(day)
        max_temp = int(value['Max TemperatureC'])
        min_temp = int(value['Min TemperatureC'])
        max_ouput = '+' * max_temp
        min_output = '+' * min_temp
        print(str(formatted_day) + ' ' + Color.BLUE + min_output + Color.END + Color.RED + max_ouput + Color.END + ' ' +  str(min_temp) + 'C - ' + str(max_temp) + 'C')

    pass

def get_stats(data, target, column, filter):
    if column == 'temp' and filter == 'yearly':
        if target == 'max':
            max_value = 0
            row_no = 0
            max_value = data[['Max TemperatureC', 'Mean TemperatureC', 'Min TemperatureC']].max().max()
            row_no = np.where(data[['Max TemperatureC', 'Mean TemperatureC', 'Min TemperatureC']] == max_value)[0]
            return max_value, row_no[0]

        elif target == 'min':
            min_value = 0
            row_no = 0
            min_value = data[['Max TemperatureC', 'Mean TemperatureC', 'Min TemperatureC']].min().min()
            row_no = np.where(data[['Max TemperatureC', 'Mean TemperatureC', 'Min TemperatureC']] == min_value)[0]
            return min_value, row_no[0]
    elif column == 'hum' and filter == 'yearly':
        max_value = 0
        row_no = 0
        max_value = data[['Max Humidity', ' Mean Humidity', ' Min Humidity']].max().max()
        row_no = np.where(data[['Max Humidity', ' Mean Humidity', ' Min Humidity']] == max_value)[0]
        return max_value, row_no[0]
    elif column == 'temp' and filter == 'monthly':
        if target == 'max':
            max_value = 0
            max_value = data[['Mean TemperatureC']].max().max()
            return max_value

        elif target == 'min':
            min_value = 0
            min_value = data[['Mean TemperatureC']].min().min()
            return min_value
    elif column == 'hum' and filter == 'monthly':
        max_value = 0
        max_value = data[[' Mean Humidity']].max().max()
        return max_value

    

def read_weater_data(folder_name):
    final_data = []

    for file_name in os.listdir(folder_name):
        data = pd.read_csv(folder_name + '/' + file_name)
        final_data.append(data)
    
    result = pd.concat(final_data)

    return result

def filter_data(data, query):
    data['GST'] = pd.to_datetime(data['GST'])
    query_lst = query.split('/')
    if len(query_lst) > 2 or len(query_lst) < 1:
        print("ERROR: invalid year or month entered")
    else:
        if len(query_lst) == 1:
            filtered_data = data[(data['GST'].dt.year == int(query_lst[0]))]
            return filtered_data
        else:
            filtered_data = data[(data['GST'].dt.year == int(query_lst[0])) & (data['GST'].dt.month == int(query_lst[1]))]
            return filtered_data

def report_generator(data, query):
    query_lst = query.split('/')
    if len(query_lst) > 2 or len(query_lst) < 1:
        print("ERROR: invalid year or month entered")
    else:
        if len(query_lst) == 1:
            value, row = get_stats(data, 'max', 'temp', 'yearly')
            date = data['GST'].iloc[row]
            day_date = date.strftime('%B %d')
            print('Highest: ' + str(value) + 'C on ' + day_date)

            value, row = get_stats(data, 'min', 'temp', 'yearly')
            date = data['GST'].iloc[row]
            day_date = date.strftime('%B %d')
            print('Lowest: ' + str(value) + 'C on ' + day_date)

            value, row = get_stats(data, 'max', 'hum', 'yearly')
            date = data['GST'].iloc[row]
            day_date = date.strftime('%B %d')
            print('Humid: ' + str(value) + "% on " + day_date)
        elif len(query_lst) == 2:
            value = get_stats(data, 'max', 'temp', 'monthly')
            print('Highest Average: ' + str(value) + 'C')

            value = get_stats(data, 'min', 'temp', 'monthly')
            print('Lowest Average: ' + str(value) + 'C')

            value = get_stats(data, 'max', 'hum', 'monthly')
            print('Average Humidity: ' + str(value) + '%')

            show_chart(data)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python file_name.py arg1 arg2")
    else:
        query = sys.argv[1]
        folder_name = sys.argv[2]

        data = read_weater_data(folder_name)

        data = filter_data(data, query)

        report_generator(data, query)






