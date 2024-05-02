from flask import Flask, render_template, request
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)


# def three_zero(result):
#     result = str(result)
#     s_with_space = ''
#     flag = False
#     for i, x in enumerate(result):
#         if x == '.' or flag is True:
#             if flag is False:
#                 s_with_space += ' ' + x
#                 flag = True
#             else:
#                 s_with_space += x
#                 flag = True
#         elif i % 3 == 1:
#             s_with_space += ' '
#             s_with_space += x
#         else:
#             s_with_space += x
#     return s_with_space


def convert_currency(amount, currency_from, currency_to):
    if not amount:
        return "Задайте значение!"
    amount = str(amount)
    amount = "".join(amount.split())
    url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    response = requests.get(url)
    # Парсирование из ссылки
    root = ET.fromstring(response.content)
    rate_from = 1
    rate_to = 1
    for valute in root.findall('Valute'):
        if valute.find("CharCode").text == 'Ru':
            rate_from = 1
        elif valute.find('CharCode').text == currency_from:
            rate_from = float(valute.find('Value').text.replace(',', '.'))

        if valute.find('CharCode').text == currency_to:
            rate_to = float(valute.find('Value').text.replace(',', '.'))
    # Конвертирование
    result = round((float(amount) * rate_from / rate_to), 2)

    return result


@app.route('/', methods=['GET', 'POST'])
def home():
    currency_from = 'RU'
    currency_to = 'RU'
    # Конверт валбты
    if request.method == 'POST':
        # полчение значения из формы
        amount = request.form['amount']
        currency_from = request.form['currency_from']
        currency_to = request.form['currency_to']
        # Конверсия
        result = convert_currency(amount, currency_from, currency_to)
        # Визуализация конвертации
        return render_template('home.html', result=result, currency_from=currency_from, currency_to=currency_to)
    # Отрисовка домашней страницы
    return render_template('home.html', currency_from=currency_from, currency_to=currency_to)


if __name__ == '__main__':
    app.run(debug=True)
