import csv
import urllib.request
from datetime import date, timedelta
import matplotlib.pyplot as plt

SUCCESS = 1
FAILURE = 0
DOWNLOAD_PROCESS_MSG = "downloading..."
DOWNLOAD_SUCCESS_MSG = "download complete."
DOWNLOAD_FAILURE_MSG = "download failed."
OECD = ["Israel", "Australia", "Austria", "Belgium", "Canada", "Chile", "Colombia", "Czech Republic", "Denmark",
        "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland", "Ireland",
        "Italy", "Japan", "South Korea", "Latvia", "Lithuania", "Luxembourg", "Mexico", "Netherlands",
        "New Zealand", "Norway", "Poland", "Portugal", "Slovakia", "Slovenia", "Spain", "Sweden",
        "Switzerland", "Turkey", "United Kingdom", "United States"]

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
    {
    country_name1: {
                    date1 : {...data...}, date2 : {...data...}, ...
                   }
    country_name2: ...
    ...
    }
    access is easily done by using dict[country_name][date][data]
    (ex. dict["Israel"]["2020-02-02"]["total_tests_per_thousand"])
    :return: a dictionary of the data
    """
    data_dict = dict()
    with open(FILE_NAME) as f:
        csv_file = csv.reader(f, delimiter=",")
        topics = next(csv_file)
        for row in csv_file:
            sub_dict = generate_sub_dict(topics, row)
            country_name = row[2]  # first key
            date = row[3]  # second key
            if country_name not in data_dict:
                data_dict[country_name] = {date: sub_dict}
            else:
                data_dict[country_name][date] = sub_dict
    return data_dict


def get_oecd_dict():
    """
    generates the dictionary the corresponds to the OECD countries (37 of them)
    :return: oecd dict
    """
    oecd_dict = dict()
    data_dict = create_data_dict()
    for item in data_dict:
        if item in OECD:
            oecd_dict[item] = data_dict[item]
    return oecd_dict


def generate_all_dates(start_date, end_date):
    """
    generates all dates from start date to end date
    :param start_date: some string yyyy/mm/dd
    :param end_date: some string yyyy/mm/dd
    :return: array of all dates from start to end(including both)
    """
    dates = []
    syear, smonth, sday = start_date.split("-")
    eyear, emonth, eday = end_date.split("-")
    sdate = date(int(syear), int(smonth), int(sday))
    edate = date(int(eyear), int(emonth), int(eday))
    delta = edate - sdate
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        dates.append(str(day))
    return dates


def get_data_in_range(start_date, end_date, data, dict, country):
    """
    gets all of the data of the given country from start date to end date
    :param start_date: as a string
    :param end_date: as a string
    :param value: the data we wish to see
    :param dict: the dictionnary that contains the data
    :param country: the country in which we are interested
    :return:
    """
    result_date = []
    dates = generate_all_dates(start_date, end_date)
    for curr_date in dates:
        value = dict[country][curr_date][data]
        if len(value) > 0:
            result_date.append(float(value))
    return result_date


def get_axis_data(start_date, end_date, data, country, dict):
    """
    plots the data according to the parameters
    :param start_date: "yyyy/mm/dd"
    :param end_date: "yyyy/mm/dd"
    :param data: the data we wish to see
    :param country
    :param dict: the entire data structure (as a dictionary)
    :return: the plot itself for future use
    """
    y_data = get_data_in_range(start_date, end_date, data, dict, country)  # data itself
    x_data = generate_all_dates(start_date, end_date)  # time
    x_data = [x_data[i][2:] for i in range(len(y_data)) if y_data[i] != ""]  # remove missing data and shorten date val
    return x_data, y_data


def plot_multiple_data(country_lst, data, end_date, start_date, data_dict):
    """

    :param country_lst:
    :param data:
    :param end_date:
    :param start_date:
    :param data_dict:
    :return:
    """
    for country in country_lst:
        x_data, y_data = get_axis_data(start_date, end_date, data, country, data_dict)
        plt.plot(x_data, y_data, marker='.', linestyle="dashed")
    plt.title(data + " from " + start_date + " to " + end_date)
    plt.xlabel("date")
    plt.xticks(rotation="vertical")
    plt.ylabel(data)
    plt.yticks(rotation="horizontal")
    plt.grid()
    plt.legend(country_lst)
    plt.show()


if __name__ == '__main__':
    " note that dates should be yyyy/mm/dd "
    #download_data()

    start_date = "2020-10-01"
    end_date = "2020-10-03"
    data = "new_cases"
    country_lst = ["Israel", "United States","United Kingdom","Italy","Spain","Australia","Greece"]

    data_dict = create_data_dict()
    plot_multiple_data(country_lst, data, end_date, start_date, data_dict)
