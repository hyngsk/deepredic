import datetime #333
import json
import ssl
import requests
import telegram
# import numpy as np
# import tensorflow as tf
from flask import Flask, request
from flask import render_template

from Scheduler import Scheduler
from datautil import getData
from upbit import Upbit

app = Flask(__name__) #hi
upbit = Upbit()
# upbit.get_hour_candles('KRW-BTC')

#https://api.telegram.org/bot1787156675:AAE6V94s-0ov58WebD4mzhsgjSkms4a0jps/setWebhook?url=https://deepredic.herokuapp.com/1787156675:AAE6V94s-0ov58WebD4mzhsgjSkms4a0jps
token = '1787156675:AAE6V94s-0ov58WebD4mzhsgjSkms4a0jps'
api_url = 'https://api.telegram.org'
bot = telegram.Bot(token)

#
# load = tf.saved_model.load('mnist/1')
# load_inference = load.signatures["serving_default"]
#
#
# @app.route('/inference', methods=['POST'])
# def inference():
#     data = request.json
#     result = load_inference(tf.constant(data['images'], dtype=tf.float32) / 255.0)
#     return str(np.argmax(result['dense_1'].numpy()))


@app.route(f'/{token}', methods=['POST'])
def telegram_response():
    print(f"{json.dumps(request.get_json(), indent=4)}")
    update = telegram.update.Update.de_json(request.get_json(force=True), bot=bot)
    print(f'\n{type(update)}\n{update}')
    chat_id = None
    text = None
    date = None


    if request.get_json().get('message').get('text') is not None:
        chat_id = request.get_json().get('message').get('from').get('id')
        text = request.get_json().get('message').get('text').split()
        date = request.get_json().get('message').get('date')

        if text[0][0] == '/':  # or text[0][1:] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
            # entities = request.get_json().get('message').get('entities')
            # print(f'length : {entities[0]["length"]}\ntype : {entities[0]["type"]}')
            if text[0] == '/start':
                send_message(chat_id, 'We\'re making chat bot. \nbut you can use \'/code {name}\' command only.')
            elif text[0] =='/help':
                send_message(chat_id, 'you can get current trade price in Upbit\nusing \'/code {currency code}\' command.')

            elif text[0] == '/code':
                try:
                    market = ['KRW-' + text[1]]
                    result = upbit.get_current_price(market)
                    send_message(chat_id, f'{text[1]}의 현재가는 {result[0]["trade_price"]}입니다.')
                except:
                    send_message(chat_id, '올바른 화폐를 입력해주세요.')
            else:
                send_message(chat_id, '구현되지 않은 명령어입니다. \ndevelper\'s email: hyngsk.o@gmail.com')
            print(f'{datetime.datetime.fromtimestamp(date)} : {text}')
        else:
            pass
    # else:
    #     send_message(chat_id, '올바르지 않은 명령어입니다. \n명령어 포맷 : 영문 소문자 \ndevelper\'s email: hyngsk.o@gmail.com')


    return '', 200


def send_message(chat_id, message):
    requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={message}')


@app.route('/data/')
def show_Data():
    data = request.args.get('data')
    if data is None or data == '':
        return 'No data parameter'
    elif data == 1:
        result = getData('Every15Minutes.csv')
    elif data == 2:
        result = getData('Every1Hour.csv')
    else:
        return '1 또는 2를 입력해주세요.'
    return result

@app.route('/')
def root():
    market = request.args.get('market')
    if market is None or market == '':
        return 'No market parameter'

    candles = upbit.get_hour_candles(market)
    if candles is None:
        return 'invalid market: {}'.format(market)

    label = market
    xlabels = []
    dataset = []
    i = 0
    for candle in candles:
        xlabels.append('')
        dataset.append(candle['trade_price'])
        i += 1
    return render_template('chart.html', **locals())


if __name__ == '__main__':
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile='newkey.crt', keyfile='newkey.key', password='hyngsk1540')

    scheduler = Scheduler()
    scheduler.scheduler('cron', "Every1Hour")
    scheduler.scheduler('cron', "Every15Minutes")
    app.debug = True

    app.run(host='0.0.0.0', port=8443, threaded=False, ssl_context=ssl_context)
