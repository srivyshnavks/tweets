import django
from django.shortcuts import render
from utils import twitter_utils
from django.http import HttpResponse
import numpy as np
import io
from utils.fusioncharts import FusionCharts


def index(request):
    return render(request, 'home/upload.html')


# render looks in the templates directory
def process_input_string(request):
    print(request.POST)
    print(request.POST['query'])
    input_text = request.POST['query']
    input_query = input_text + '-filter:retweets'
    tweets = twitter_utils.get_tweets(input_query)
    data, sent, users = twitter_utils.create_dataframe(tweets, input_text)
    pie_chart = pi_chart(request, sent)
    source_chart = sources(request, users)

    return render(request, 'home/upload.html', {"result": data.to_html(),
                                                'pie_chart': pie_chart, 'source_chart': source_chart})


def pi_chart(request, sent):
    # Create an object for the pie3d chart using the FusionCharts class constructor
    pie3d = FusionCharts("pie3d", "ex2", "100%", "400", "pie_chart", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                         """{ 
                             "chart": {
                                 "caption": "Sentiment Analysis",
                                 "subCaption" : "Positive, Negative or Neutral",
                                 "showValues":"1",
                                 "showPercentInTooltip" : "0",
                                 "numberPrefix" : "",
                                 "enableMultiSlicing":"1",
                                 "theme": "fusion"
                             },
                             "data": [{
                                 "label": "Negative",
                                 "value": """ + str(sent[0]) + """
                             }, {
                                 "label": "Neutral",
                                 "value": """ + str(sent[1]) + """
                             }, {
                                 "label": "Positive",
                                 "value": """ + str(sent[2]) + """
                             }]
                         }""")

    # returning complete JavaScript and HTML code, which is used to generate chart in the browsers.
    return pie3d.render()


def sources(request, users):
    # Create an object for the pie3d chart using the FusionCharts class constructor
    others = 100 - (users[0][1] + users[1][1] + users[2][1])
    pie3d = FusionCharts("pie3d", "ex3", "100%", "400", "source_chart", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                         """{ 
                             "chart": {
                                 "caption": "Sources of Tweets",
                                 "subCaption" : "Tweeted from different devices",
                                 "showValues":"1",
                                 "showPercentInTooltip" : "0",
                                 "numberPrefix" : "",
                                 "enableMultiSlicing":"1",
                                 "theme": "fusion"
                             },
                             "data": [{
                                 "label": """ + """\"""" + str(users[0][0]).replace('for ', '') + """\"""" + """,
                                     "value": """ + str(users[0][1]) + """
                                 }, {
                                     "label": """ + """\"""" + str(users[1][0]).replace('for ', '') + """\"""" + """,
                                     "value": """ + str(users[1][1]) + """
                                 }, {
                                     "label": """ + """\"""" + str(users[2][0]).replace('for ', '') + """\"""" + """,
                                     "value": """ + str(users[2][1]) + """
                                 }, {
                                     "label": "Others",
                                     "value": """ + str(others) + """
                                 }]
                             }""")

    # returning complete JavaScript and HTML code, which is used to generate chart in the browsers.
    return pie3d.render()
