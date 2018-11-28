import django
from django.shortcuts import render
from utils import twitter_utils
from django.http import HttpResponse
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import io
import matplotlib.pyplot as plt; plt.rcdefaults()

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

    return render(request, 'home/upload.html', {"result": data.to_html()})

def pi_chart(request):
	fig = Figure()
	canvas = FigureCanvas(fig)

	labels = 'positive', 'negative', 'zero'
	sentiiments = twitter_utils.create_list_pie(tweets)
	colors = ['yellowgreen', 'lightcoral', 'lightskyblue']
	plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
