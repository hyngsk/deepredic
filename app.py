import datetime  # 333
import json
import logging
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

app = Flask(__name__)  # hi
app.config['JSON_AS_ASCII'] = False

upbit = Upbit()
# upbit. get_hour_candles('KRW-BTC')

# https://api.telegram.org/bot1787156675:AAE6V94s-0ov58WebD4mzhsgjSkms4a0jps/setWebhook?url=https://deepredic.herokuapp.com/1787156675:AAE6V94s-0ov58WebD4mzhsgjSkms4a0jps

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
@app.errorhandler(405)
def method_not_allowed(error):
    app.logger.info('\n' + '*' * 30 + f'\n{str(request.headers)}\n' + '*' * 30)
    app.logger.error(error)
    return '', 405


@app.errorhandler(404)
def page_not_found(error):
    app.logger.info('\n' + '*' * 30 + f'\n{str(request.headers)}\n' + '*' * 30)
    app.logger.error(error)
    return '', 404


@app.route(f'/{token}', methods=['POST'])
def telegram_response():
    app.logger.info('\n' + '*' * 30 + f'\n{str(request.headers)}\n' + '*' * 30)
    app.logger.info(f"{json.dumps(request.get_json(), indent=4)}")
    # update = telegram.update.Update.de_json(request.get_json(force=True), bot=bot)
    # logging.info(f'\n{type(update)}\n{update}')
    chat_id = None
    text = None
    date = None
    if request.get_json() is None:
        return '', 200

    if request.get_json().get('message').get('text') is not None:
        chat_id = request.get_json().get('message').get('from').get('id')
        text = request.get_json().get('message').get('text').split()
        date = request.get_json().get('message').get('date')

        if text[0][0] == '/':  # or text[0][1:] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
            # entities = request.get_json().get('message').get('entities')
            # print(f'length : {entities[0]["length"]}\ntype : {entities[0]["type"]}')
            if text[0] == '/start':
                send_message(chat_id, 'We\'re making chat bot. \nbut you can use \'/code {name}\' command only.')
            elif text[0] == '/help':
                send_message(chat_id,
                             'you can get current trade price in Upbit\nusing \'/code {currency code}\' command.')

            elif text[0] == '/code':
                try:
                    market = ['KRW-' + text[1]]
                    result = upbit.get_current_price(market)
                    send_message(chat_id, f'{text[1]}??? ???????????? {result[0]["trade_price"]}?????????.')
                except:
                    send_message(chat_id, '????????? ????????? ??????????????????.')
            else:
                send_message(chat_id, '???????????? ?????? ??????????????????. \ndevelper\'s email: hyngsk.o@gmail.com')
            # logging.info(f'{datetime.datetime.fromtimestamp(date)} : {text}')
        else:
            pass
    # else:
    #     send_message(chat_id, '???????????? ?????? ??????????????????. \n????????? ?????? : ?????? ????????? \ndevelper\'s email: hyngsk.o@gmail.com')

    return '', 200


def send_message(chat_id, message):
    requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={message}')


@app.route('/data/')
def show_Data():
    app.logger.info('\n' + '*' * 30 + f'\n{str(request.headers)}\n' + '*' * 30)
    data = request.args.get('data')
    if data is None or data == '':
        return 'No data parameter'
    elif data == "1":
        result = getData('Every15Minutes.csv').sort_values(by=['Time'], axis=0, ascending=False)
        result = result[['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'EMA5', 'EMA10', 'EMA20', 'EMA60', 'MACD',
                 'MACDsignal',
                 'MACD-S']]
    elif data == "2":
        result = getData('Every1Hour.csv').sort_values(by=['Time'], axis=0, ascending=False)
        result = result[['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'EMA5', 'EMA10', 'EMA20', 'EMA60', 'MACD',
                 'MACDsignal',
                 'MACD-S']]
    else:
        return '1 ?????? 2??? ??????????????????.'
    return render_template('table.html', stocklist=list(result.values))


@app.route('/')
def root():
    # if str(request.user_agent) != "ELB-HealthChecker/2.0":
    app.logger.info('\n' + '*' * 30 + f'\n{str(request.host)} {str(request.host_url)}\n' + '*' * 30)
    app.logger.info('\n' + '*' * 30 + f'\n{str(request.headers)}\n' + '*' * 30)
    market = request.args.get('market')
    app.logger.info(f'requested market : {market}')
    # print(str(request.user_agent))

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

    scheduler = Scheduler()
    app.logger.info(scheduler.scheduler('cron', "Every1Hour"))
    app.logger.info(scheduler.scheduler('cron', "Every15Minutes"))
    app.debug = True
    app.run(host='0.0.0.0', port=443, threaded=False)
else:
    gunicorn_logger = logging.getLogger('CustomGunicornLogger')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    scheduler = Scheduler()
    app.logger.info(scheduler.scheduler('cron', "Every1Hour"))
    app.logger.info(scheduler.scheduler('cron', "Every15Minutes"))
