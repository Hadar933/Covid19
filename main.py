import csv
import urllib.request
from datetime import date
import pandas as pd

SUCCESS = 1
FAILURE = 0
DOWNLOAD_PROCESS_MSG = "downloading..."
DOWNLOAD_SUCCESS_MSG = "download complete."
DOWNLOAD_FAILURE_MSG = "download failed."

URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
FILE_NAME = "data_" + str(date.today()) + ".csv"


def download_data():
    try:
        print(DOWNLOAD_PROCESS_MSG)
        urllib.request.urlretrieve(URL, FILE_NAME)
        print(DOWNLOAD_SUCCESS_MSG, "File name is: ", FILE_NAME)
        return SUCCESS
    except Exception as e:
        print(e, DOWNLOAD_FAILURE_MSG)
        return FAILURE


def generate_sub_dict(topics, line):
    sub_dict = dict()
    for topic, item in zip(topics, line):
        sub_dict[topic] = item
    return sub_dict


def create_data_dict():
    """
    this function generates a dictionary, in which the key is a location (ex. israel,usa,etc...) and the value
    is the entire data set, that is relevant to the given country.
    the structure of the data is as followed:
    {country_name: [
                    {iso:__,continent:__,location:__,date:__,...}
                    ,{...},
                    ...,
                    {...}
                ]
    }
    which means: the most general KEY is COUNTRY_NAME. the value is an ARRAY of DICTIONARIES, where each dict represents
    a DIFFERENT DATE
    :return:
    """
    data_dict = dict()
    with open(FILE_NAME) as f:
        csv_file = csv.reader(f, delimiter=",")
        topics = next(csv_file)
        for row in csv_file:
            sub_dict = generate_sub_dict(topics, row)
            country_name = row[2]
            if country_name not in data_dict:
                data_dict[country_name] = [sub_dict]
            else:
                data_dict[country_name].append(sub_dict)
    return data_dict

if __name__ == '__main__':
    # download_data()
    data_dict = create_data_dict()
    print(data_dict["Israel"])
    # for item in data_dict['Israel']:
    #     print(item)

