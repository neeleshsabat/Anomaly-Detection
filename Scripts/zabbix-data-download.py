import requests
import json
import time
import pandas as pd
import datetime

'''
10328, 10333, 10325, 10326, 10343 '''
zabbix_url = "http://10.194.74.40/zabbix/api_jsonrpc.php"
zabbix_user = "Admin"
zabbix_password = "zabbix"
host_id = "10328"
from_ist_time = datetime.datetime.strptime('2023-05-15 23:30:00', '%Y-%m-%d %H:%M:%S')
to_ist_time = datetime.datetime.strptime('2023-05-16 23:30:00', '%Y-%m-%d %H:%M:%S')
from_time = int(from_ist_time.timestamp())
to_time = int(to_ist_time.timestamp())

# from_time = int(time.time()) - 3600  # 1 hour ago
# to_time = int(time.time())  # current time

# Authenticate with the Zabbix API
auth_data = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": zabbix_user,
        "password": zabbix_password
    },
    "id": 1
}

response = requests.post(zabbix_url, json=auth_data)
auth_token = response.json()["result"]

# Fetch the item IDs for the host
item_request = {
    "jsonrpc": "2.0",
    "method": "item.get",
    "params": {
        "output": ["itemid"],
        "hostids": host_id,
        "sortfield": "name",
        "sortorder": "ASC"
    },
    "auth": auth_token,
    "id": 2
}

response = requests.post(zabbix_url, json=item_request)
item_data = response.json()["result"]


# Fetch the names of the items for the host
item_names = {}
for item in item_data:
    item_id = item["itemid"]
    name_request = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": ["name"],
            "selectApplications": ["name"],
            "selectHosts": ["name"],
            "itemids": item_id
        },
        "auth": auth_token,
        "id": 3
    }
    response = requests.post(zabbix_url, json=name_request)
    name_data = response.json()["result"]
   
    try:
        application_name = name_data[0]["applications"][0]["name"]
    except:
        application_name = "None"
    try:
        host_name = name_data[0]["hosts"][0]["name"]
    except:
        host_name = "Nohostname"
    itemname = name_data[0]["name"]
    item_names[item_id] = host_name + "_" + application_name + "_" + itemname
    
    

# Fetch the time series data for the items
history_request = {
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
        "output": ["clock", "value", "itemid"],
        "history": 0,  # numeric (float or integer) value
        "hostids": host_id,
        "sortfield": "clock",
        "sortorder": "ASC",
        "time_from": from_time,
        "time_till": to_time
    },
    "auth": auth_token,
    "id": 4
}

response = requests.post(zabbix_url, json=history_request)
history_data = response.json()["result"]

history_request_character = {
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
        "output": ["clock", "value", "itemid"],
        "history": 1,  # character
        "hostids": host_id,
        "sortfield": "clock",
        "sortorder": "ASC",
        "time_from": from_time,
        "time_till": to_time
    },
    "auth": auth_token,
    "id": 4
}

response = requests.post(zabbix_url, json=history_request_character)
history_data_character = response.json()["result"]

history_request_log = {
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
        "output": ["clock", "value", "itemid"],
        "history": 2,  # log
        "hostids": host_id,
        "sortfield": "clock",
        "sortorder": "ASC",
        "time_from": from_time,
        "time_till": to_time
    },
    "auth": auth_token,
    "id": 4
}

response = requests.post(zabbix_url, json=history_request_log)
history_data_log = response.json()["result"]

history_request_numeric_unsigned = {
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
        "output": ["clock", "value", "itemid"],
        "history": 3,  # numeric unsigned
        "hostids": host_id,
        "sortfield": "clock",
        "sortorder": "ASC",
        "time_from": from_time,
        "time_till": to_time
    },
    "auth": auth_token,
    "id": 4
}

response = requests.post(zabbix_url, json=history_request_numeric_unsigned)
history_data_numeric_unsigned = response.json()["result"]

history_request_text = {
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
        "output": ["clock", "value", "itemid"],
        "history": 4,  # numeric unsigned
        "hostids": host_id,
        "sortfield": "clock",
        "sortorder": "ASC",
        "time_from": from_time,
        "time_till": to_time
    },
    "auth": auth_token,
    "id": 4
}

response = requests.post(zabbix_url, json=history_request_text)
history_data_text = response.json()["result"]

# Writing the time series data to a file
# print("Creating a file for time series data")
# if len(history_data) > 0:
#     print(f"Time\t\tItem name\tValue")
#     with open("output1.txt", "w") as f:
#         f.write(f"Time\t\tItem name\tValue\n")
#         for history_item in history_data:
#             timestamp = int(history_item["clock"])
#             timestamp_str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(timestamp))
#             value = history_item["value"]
#             item_id = history_item["itemid"]
#             item_name = item_names[item_id]
#             f.write(f"{timestamp_str}\t{item_name}\t{value}\n")
# else:
#     print("No data found")

# Create a Pandas dataframe for the time series data
print("Creating a pandas dataframe for time series data")
df = pd.DataFrame(columns=["Timestamp"] + list(item_names.values()))
if len(history_data) > 0:
    for history_item in history_data:
        timestamp = int(history_item["clock"])
        utc_datetime = datetime.datetime.utcfromtimestamp(timestamp)
        ist_offset = datetime.timedelta(hours=5, minutes=30, seconds=0)
        ist_datetime = utc_datetime + ist_offset
        timestamp_str = ist_datetime.strftime("%Y-%m-%dT%H:%M")
        #timestamp_str = time.strftime("%Y-%m-%dT%H:%M", time.gmtime(timestamp))
        value = history_item["value"]
        item_id = history_item["itemid"]
        item_name = item_names[item_id]
        if timestamp_str not in df['Timestamp']:
            df.loc[timestamp_str] = [timestamp_str] + [None] * len(item_names)
        if df.loc[timestamp_str, item_name] is None:
            df.loc[timestamp_str, item_name] = value

if len(history_data_character) > 0:
    for history_item in history_data_character:
        timestamp = int(history_item["clock"])
        utc_datetime = datetime.datetime.utcfromtimestamp(timestamp)
        ist_offset = datetime.timedelta(hours=5, minutes=30, seconds=0)
        ist_datetime = utc_datetime + ist_offset
        timestamp_str = ist_datetime.strftime("%Y-%m-%dT%H:%M")
        #timestamp_str = time.strftime("%Y-%m-%dT%H:%M", time.gmtime(timestamp))
        value = history_item["value"]
        item_id = history_item["itemid"]
        item_name = item_names[item_id]
        if timestamp_str not in df['Timestamp']:
            df.loc[timestamp_str] = [timestamp_str] + [None] * len(item_names)
        if df.loc[timestamp_str, item_name] is None:
            df.loc[timestamp_str, item_name] = value

if len(history_data_log) > 0:
    for history_item in history_data_log:
        timestamp = int(history_item["clock"])
        utc_datetime = datetime.datetime.utcfromtimestamp(timestamp)
        ist_offset = datetime.timedelta(hours=5, minutes=30, seconds=0)
        ist_datetime = utc_datetime + ist_offset
        timestamp_str = ist_datetime.strftime("%Y-%m-%dT%H:%M")
        #timestamp_str = time.strftime("%Y-%m-%dT%H:%M", time.gmtime(timestamp))
        value = history_item["value"]
        item_id = history_item["itemid"]
        item_name = item_names[item_id]
        if timestamp_str not in df['Timestamp']:
            df.loc[timestamp_str] = [timestamp_str] + [None] * len(item_names)
        if df.loc[timestamp_str, item_name] is None:
            df.loc[timestamp_str, item_name] = value

if len(history_data_numeric_unsigned) > 0:
    for history_item in history_data_numeric_unsigned:
        timestamp = int(history_item["clock"])
        utc_datetime = datetime.datetime.utcfromtimestamp(timestamp)
        ist_offset = datetime.timedelta(hours=5, minutes=30, seconds=0)
        ist_datetime = utc_datetime + ist_offset
        timestamp_str = ist_datetime.strftime("%Y-%m-%dT%H:%M")
        #timestamp_str = time.strftime("%Y-%m-%dT%H:%M", time.gmtime(timestamp))
        value = history_item["value"]
        item_id = history_item["itemid"]
        item_name = item_names[item_id]
        if timestamp_str not in df['Timestamp']:
            df.loc[timestamp_str] = [timestamp_str] + [None] * len(item_names)
        if df.loc[timestamp_str, item_name] is None:
            df.loc[timestamp_str, item_name] = value

if len(history_data_text) > 0:
    for history_item in history_data_text:
        timestamp = int(history_item["clock"])
        utc_datetime = datetime.datetime.utcfromtimestamp(timestamp)
        ist_offset = datetime.timedelta(hours=5, minutes=30, seconds=0)
        ist_datetime = utc_datetime + ist_offset
        timestamp_str = ist_datetime.strftime("%Y-%m-%dT%H:%M")
        #timestamp_str = time.strftime("%Y-%m-%dT%H:%M", time.gmtime(timestamp))
        value = history_item["value"]
        item_id = history_item["itemid"]
        item_name = item_names[item_id]
        if timestamp_str not in df['Timestamp']:
            df.loc[timestamp_str] = [timestamp_str] + [None] * len(item_names)
        if df.loc[timestamp_str, item_name] is None:
            df.loc[timestamp_str, item_name] = value

        


# Write the dataframe to an Excel file
excel_filename = "zabbix_data3.xlsx"
df.to_excel(excel_filename, index=False)