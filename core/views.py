import time

from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from core.questions import result_question_1, result_question_2, result_question_3, result_question_4, \
    result_question_5, result_question_6, save_data, capturar_links, montar_csv

URLS = {1:'https://www.rottentomatoes.com/browse/tv-list-1',
       2:'http://www.imdb.com/chart/boxoffice',
       3:'https://www.climatempo.com.br/previsao-do-tempo/15-dias/cidade/264/teresina-pi',
       4:'http://example.webscraping.com',
       5:"http://www.portaltransparencia.gov.br/copa2014/api/rest/empreendimento"}

PATHS = {1:'files/rotten.txt',
         2:'files/imdb.txt',
         3:'files/clima.txt',
         4:'files/countries.txt',
         5:'files/copa.txt'}


def index(request):
    return render(request, 'index.html')


def question1(request):
    results = result_question_1(PATHS[1]).values()
    montar_csv(list(results), 'core/static/files/rotten.csv')
    return render(request, 'question1.html', {'results':results})


def question2(request):
    results = result_question_2(PATHS[2]).values()
    montar_csv(list(results),'core/static/files/imdb.csv')
    return render(request, 'question2.html', {'results':results})


def question3(request):
    results = sorted(result_question_3(PATHS[3]).values(), key=lambda r: r['date'])
    montar_csv(list(results),'core/static/files/clima_tempo.csv')
    return render(request, 'question3.html', {'results':results})


def question4(request):
    results = sorted(result_question_4(PATHS[4]).values(), key=lambda x:x['country'])
    montar_csv(list(results), 'core/static/files/example_ws.csv')
    return render(request, 'question4.html', {'results':results})


def question5(request):
    total = result_question_5(PATHS[5])
    results = list(sorted(result_question_6(PATHS[5]).values(), key=lambda r: r['valor'], reverse=True))
    results.append({'cidade':'TOTAL','valor':str(total)})
    montar_csv(list(results), 'core/static/files/gasto_copa_2014.csv')
    return render(request, 'question5.html', {'results':results, 'total':total})


def saveData(request,q_id):
    print('ok')
    q_id = int(q_id)
    # next = request.META.get('HTTP_REFERER', '/')
    save = save_data(URLS[q_id], PATHS[q_id])
    return JsonResponse({'done':True})


def saveDataQ4(request):
    next = request.META.get('HTTP_REFERER', '/')
    links = capturar_links()
    print(links)
    for i in range(0, len(links)):
        save_data(URLS[4]+links[i], PATHS[4], 'a')
        time.sleep(.500)
    return redirect(next)




