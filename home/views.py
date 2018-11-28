import django
from django.shortcuts import render
from utils import twitter_utils
from django.http import HttpResponse
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import io
import matplotlib.pyplot as plt
from utils.fusioncharts import FusionCharts

plt.rcdefaults()


def index(request):
    return render(request, 'home/upload.html')


# render looks in the templates directory
def process_input_string(request):
    print(request.POST)
    print(request.POST['query'])
    input_text = request.POST['query']
    input_query = input_text + '-filter:retweets'
    tweets = twitter_utils.get_tweets(input_query)
    data = twitter_utils.create_dataframe(tweets, input_text)
    pie_chart, pie_chart_title = pi_chart(request)
    time_series_chart, time_series_chart_title = timeseries_chart(request)

    return render(request, 'home/upload.html', {"result": data.to_html(),
                                                'pie_chart_title': pie_chart_title,
                                                'pie_chart': pie_chart,
                                                'time_series_chart_title': time_series_chart_title,
                                                'time_series_chart': time_series_chart})


def pi_chart(request):
    # Create an object for the pie3d chart using the FusionCharts class constructor
    chart_title = 'Pie Chart'
    pie3d = FusionCharts("pie3d", "ex2", "100%", "400", "pie_chart", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                         """{ 
                             "chart": {
                                 "caption": "Recommended Portfolio Split",
                                 "subCaption" : "For a net-worth of $1M",
                                 "showValues":"1",
                                 "showPercentInTooltip" : "0",
                                 "numberPrefix" : "$",
                                 "enableMultiSlicing":"1",
                                 "theme": "fusion"
                             },
                             "data": [{
                                 "label": "Equity",
                                 "value": "300000"
                             }, {
                                 "label": "Debt",
                                 "value": "230000"
                             }, {
                                 "label": "Bullion",
                                 "value": "180000"
                             }, {
                                 "label": "Real-estate",
                                 "value": "270000"
                             }, {
                                 "label": "Insurance",
                                 "value": "20000"
                             }]
                         }""")

    # returning complete JavaScript and HTML code, which is used to generate chart in the browsers.
    return pie3d.render(), chart_title


def timeseries_chart(request):
    # Create an object for the Multiseries column 2D charts using the FusionCharts class constructor
    chart_title = 'Multiseries Column 2D Chart'
    mscol2D = FusionCharts("mscolumn2d", "ex1", "600", "400", "time_series_chart", "json",
                           # The data is passed as a string in the `dataSource` as parameter.
                           """{ 
                                   "chart": {
                                   "caption": "App Publishing Trend",
                                   "subCaption": "2012-2016",
                                   "xAxisName": "Years",
                                   "yAxisName" : "Total number of apps in store",
                                   "formatnumberscale": "1",
                                   "drawCrossLine":"1",
                                   "plotToolText" : "<b>$dataValue</b> apps on $seriesName in $label",
                                   "theme": "fusion"
                               },
                       
                               "categories": [{
                                   "category": [{
                                   "label": "2012"
                                   }, {
                                   "label": "2013"
                                   }, {
                                   "label": "2014"
                                   }, {
                                   "label": "2015"
                                   },{
                                   "label": "2016"
                                   }
                                   ]
                               }],
                               "dataset": [{
                                   "seriesname": "iOS App Store",
                                   "data": [{
                                   "value": "125000"
                                   }, {
                                   "value": "300000"
                                   }, {
                                   "value": "480000"
                                   }, {
                                   "value": "800000"
                                   }, {
                                   "value": "1100000"
                                   }]
                               }, {
                                   "seriesname": "Google Play Store",
                                   "data": [{
                                   "value": "70000"
                                   }, {
                                   "value": "150000"
                                   }, {
                                   "value": "350000"
                                   }, {
                                   "value": "600000"
                                   },{
                                   "value": "1400000"
                                   }]
                               }, {
                                   "seriesname": "Amazon AppStore",
                                   "data": [{
                                   "value": "10000"
                                   }, {
                                   "value": "100000"
                                   }, {
                                   "value": "300000"
                                   }, {
                                   "value": "600000"
                                   },{
                                   "value": "900000"
                                   }]
                               }]
                           }""")

    return mscol2D.render(), chart_title
