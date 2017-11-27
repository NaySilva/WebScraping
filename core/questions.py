# -*-coding: utf-8 -*-
from pprint import pprint

import requests
import re
import codecs
from bs4 import BeautifulSoup
import json
import time
from functools import reduce


def download(url, num_retries=2):
    print('Downloading: ', url)
    page = None
    try:
        response = requests.get(url)
        page = response.text
        if response.status_code == 429:
            print('Ip bloqueado\nAguardando o desbloqueio...')
            time.sleep(30)
            print('Tentando reconectar')
            return download(url)
        if response.status_code >= 400:
            print('Download error:', response.text)
            if num_retries and 500 <= response.status_code < 600:
                return download(url, num_retries - 1)
    except requests.exceptions.RequestException as e:
        print('Download error: ', e)
    return page

def save_data(link, path, action='w'):
    html = download(link)
    file = open(path, action, encoding='utf8')
    file.write(html)
    file.close()
    return path


def result_question_1(path):
    html = open(path, 'r', encoding='utf8')
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', id='tv-list-21')
    series = table.find_all('tr')
    result = {}
    for serie in series:
        title = serie.find('td', class_='middle_col').text.replace('\n', '')
        review = serie.find('td', class_='left_col').text.replace('\n', '')
        result.update({title: {'title':title,
                               'review':review}})
    print(json.dumps(result, indent=4))
    return result


def result_question_2(path):
    html = open(path, 'r', encoding='utf8')
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='chart full-width').tbody
    lines = table.find_all('tr')
    result = {}
    for line in lines:
        title = line.find('td', class_='titleColumn').text.strip()
        billed = line.find_all('td', class_='ratingColumn')
        weeks = line.find('td', class_='weeksColumn').text.strip()
        result.update({title: {'title': title,
                                 'weekend': billed[0].text.strip(),
                                'gross': billed[1].text.strip(),
                                 'weeks': weeks.strip()}})
    print(json.dumps(result, indent=4))
    return result


def result_question_3(path):
    html = open(path, 'r', encoding='utf8')
    soup = BeautifulSoup(html, 'html.parser')
    result = {}
    for i in range(5):
        i = str(i)
        date = soup.find(attrs={'data-id': i}).text.split()[-1]
        tempMax = soup.find(id='tempMax' + i).text
        tempMin = soup.find(id='tempMin' + i).text
        result.update({date: {'date':'/'.join(date.split('/')[::-1]),'tempMax': tempMax, 'tempMin': tempMin}})
    # days2 = soup.find_all(id=re.compile('^resumeDay-'))[:5]
    print(json.dumps(result, indent=4))
    return result


def result_question_5(path):
    xml = codecs.open(path, "r", "utf-8").read()
    soup = BeautifulSoup(xml, 'xml')
    empreendimentos = soup.find_all('empreendimento')
    total = 0
    for empreendimento in empreendimentos:
        porc = float(empreendimento.valorPercentualExecucaoFisica.text) if empreendimento.valorPercentualExecucaoFisica else 100.00
        if empreendimento.valorTotalPrevisto:
            valor = float(empreendimento.valorTotalPrevisto.text) * porc / 100.00
            total += valor
    return round(total, 2)


def result_question_6(path):
    xml = codecs.open(path, "r", "utf-8").read()
    soup = BeautifulSoup(xml, 'xml')

    empreendimentos = soup.find_all('copa:empreendimento')
    result = {}
    total = 0
    for empreendimento in empreendimentos:
        sede = empreendimento.cidadeSede
        cidade = sede.descricao.text
        cidade += '-' + sede.sigla.text if cidade not in ['Nacional', 'Internacional'] else ''
        porc = int(empreendimento.valorPercentualExecucaoFisica.text) if empreendimento.valorPercentualExecucaoFisica else 100
        if empreendimento.valorTotalPrevisto:
            valor = float(empreendimento.valorTotalPrevisto.text) * porc / 100
            result.update({cidade: {'cidade':cidade,
                                    'valor': result.get(cidade,{'valor':0})['valor']+ valor}})
    for d in result.values(): d.update({'valor': str(round(d.get('valor'), 2))})
    print(result)
    return result


def convert_to_number(text):
    # 3.699,99 -> 3699.99
    return int(text.replace(',', ''))


def montar_item_dict(soup):
    country = soup.find(id='places_country__row').find('td', class_='w2p_fw').text
    population = convert_to_number(soup.find(id='places_population__row').find('td', class_='w2p_fw').text)
    area = convert_to_number(soup.find(id='places_area__row').find('td', class_='w2p_fw').text.split()[0])
    return {country: {'country':country,
                      'dens_pop': str(round(population / area, 2)) if area != 0 else '0.00'}}


def capturar_links():
    links = []
    for i in range(0, 26):
        url = 'http://example.webscraping.com/places/default/index/' + str(i)
        html = download(url)
        soup = BeautifulSoup(html, 'html5lib')
        links.extend(map(lambda l: l.get('href'), soup.find('tbody').find_all('a')))
        time.sleep(.500)
    return links


def result_question_4(path):
    dens_pop = {}
    htmls = open(path, 'r', encoding='utf8')
    soup = BeautifulSoup(htmls, 'html.parser')
    contries = soup.find_all('body')
    for country in contries: dens_pop.update(montar_item_dict(country))
    print(json.dumps(dens_pop, indent=4))
    return dens_pop


def montar_csv(results, path):
    file = open(path, 'w', encoding='utf8')
    titles = ';'.join(results[0].keys()) + '\n'
    file.write(titles)
    for result in results:
        line = ';'.join(result.values()) + '\n'
        file.write(line)
    file.close()


