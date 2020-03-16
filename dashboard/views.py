from django.shortcuts import render
from django.http import HttpResponse
from .fusioncharts import FusionCharts
from .fusioncharts import FusionTable
from .fusioncharts import TimeSeries
import requests
import json
import datetime


# Create your views here.
def home(request):
    # C44F33228431
    # C44F33228449
    data = requests.get('http://smartfarm.adaline.xyz/api/public/get_data/C44F33228449/360').text
    # schema = requests.get().text
    data_json = json.loads(data)

    # data_time_H = datetime.datetime.strptime(data_json[0:100]['time'], "%Y-%m-%d %H:%M:%S").strftime("%m")
    # data_time_year = []
    # data_time_mont = []
    # data_time_day = []
    # data_time_H = []
    # data_time_M = []
    # data_time_S = []
    # for i in data_json:
    #     data_time_year.append(datetime.datetime.strptime(i['time'], "%Y-%m-%d %H:%M:%S").strftime("%Y"))
    #     data_time_mont.append(datetime.datetime.strptime(i['time'], "%Y-%m-%d %H:%M:%S").strftime("%m"))
    #     data_time_day.append(datetime.datetime.strptime(i['time'], "%Y-%m-%d %H:%M:%S").strftime("%d"))
    #     data_time_H.append(datetime.datetime.strptime(i['time'], "%Y-%m-%d %H:%M:%S").strftime("%H"))
    #     data_time_M.append(datetime.datetime.strptime(i['time'], "%Y-%m-%d %H:%M:%S").strftime("%M"))
    #     data_time_S.append(datetime.datetime.strptime(i['time'], "%Y-%m-%d %H:%M:%S").strftime("%S"))
    # print(data_json)

    return render(request, 'dashboard/home.html', {'home': data_json})


def chart(request):
    data = requests.get(
        'https://s3.eu-central-1.amazonaws.com/fusion.store/ft/data/reference-line-in-multivariate-chart-data.json').text
    schema = requests.get(
        'https://s3.eu-central-1.amazonaws.com/fusion.store/ft/schema/reference-line-in-multivariate-chart-schema.json').text
    # print(data)
    print(schema)
    fusionTable = FusionTable(schema, data)
    timeSeries = TimeSeries(fusionTable)

    timeSeries.AddAttribute('chart', '{}')
    timeSeries.AddAttribute('caption', '{"text":"Temperature and Humidity"}')
    timeSeries.AddAttribute('yaxis',
                            '[{"plot":"Temperature","title":"Temp (in °C)","referenceline":[{"label":"Average Temperature","value":"30"}]},{"plot":"Carbon mono-oxide","title":"Humidity (%)","referenceline":[{"label":"Average Humidity","value":"60"}]}]')

    # Create an object for the chart using the FusionCharts class constructor
    fcChart = FusionCharts("timeseries", "ex1", 700, 450, "chart-1", "json", timeSeries)

    # returning complete JavaScript and HTML code, which is used to generate chart in the browsers.
    return render(request, 'dashboard/chart.html', {'output': fcChart.render()})


# Create your views here.
def chartjs(request):
    data = requests.get('http://smartfarm.adaline.xyz/api/public/get_data/C44F33228449/360').text
    # schema = requests.get().text
    data_json = json.loads(data)

    # data_time_H = datetime.datetime.strptime(data_json[0:100]['time'], "%Y-%m-%d %H:%M:%S").strftime("%m")
    # data_time_year = []
    # data_time_mont = []
    # data_time_day = []
    # data_time_H = []
    # data_time_M = []
    # data_time_S = []
    # for i in data_json:
    #     data_time_year.append(datetime.datetime.strptime(i['time'], "%Y-%m-%d %H:%M:%S").strftime("%Y"))
    #     data_time_mont.append(datetime.datetime.strptime(i['time'], "%Y-%m-%d %H:%M:%S").strftime("%m"))
    #     data_time_day.append(datetime.datetime.strptime(i['time'], "%Y-%m-%d %H:%M:%S").strftime("%d"))
    #     data_time_H.append(datetime.datetime.strptime(i['time'], "%Y-%m-%d %H:%M:%S").strftime("%H"))
    #     data_time_M.append(datetime.datetime.strptime(i['time'], "%Y-%m-%d %H:%M:%S").strftime("%M"))
    #     data_time_S.append(datetime.datetime.strptime(i['time'], "%Y-%m-%d %H:%M:%S").strftime("%S"))
    # print(data_json)

    return render(request, 'dashboard/chartjs.html', {'home': data_json})


# Create your views here.
def last_update(request):
    data = requests.get('http://smartfarm.adaline.xyz/api/public/get_data/C44F33228449/1').text
    data = data.replace('[', '')
    data = data.replace(']', '')
    return HttpResponse(data)
