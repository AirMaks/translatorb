from flask import Flask
from flask import jsonify
from flask import request
import requests
import json
import re
from flask_sslify import SSLify
import misc

import telebot
import os
import logging



# https://api.telegram.org/bot913766617:AAEYW61FFoCJJjqFNJCfeABZU4Z6i3fvkXc/deleteWebhook
# https://api.telegram.org/bot913766617:AAEYW61FFoCJJjqFNJCfeABZU4Z6i3fvkXc/setWebhook?url=https://romanmaksimov555.pythonanywhere.com/
token = misc.token
chat_id = misc.chat_id
URL = 'https://api.telegram.org/bot' + token +'/'

bot = telebot.TeleBot(token)




def send_message(chat_id, text):
	

	url = URL + 'sendMessage'
	
	answer = {'chat_id': chat_id, 'text': text}
	r = requests.post(url, json=answer)
	return r.json()

if "HEROKU" in list(os.environ.keys()):
	app = Flask(__name__)
	sslify = SSLify(app)
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)


    @app.route("/", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200
    @app.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://translatorb.herokuapp.com/") # этот url нужно заменить на url вашего Хероку приложения
        return "?", 200
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 80))


    @app.route('/', methods=['POST', 'GET'])
	def index():
	
	chat_id = misc.chat_id
	

	if request.method == 'POST':
		r = request.get_json()
		message = r['message']['text']

		
		# print(yandexTranslate)

		if message:
			yandexTranslate = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20200218T130639Z.26ca672f010fc8ba.2bb4b9b862526292d5221536e002ed46ea41359d&text=' + message + '&lang=en'
			r = requests.post(yandexTranslate, data={}) 
			answer = json.loads(r.text)['text'][0]
			send_message(chat_id, answer)

	return '<h1>Superman welcome</h1>'
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.  
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)




if __name__ == '__main__':
	# pass
	# getTranslatedText()
	app.run()



