from flask import Response, render_template, request
from application import app
import os
import random
import json
import requests

from .libsolvemedia import SolveMedia
from .dbconnect import Database


@app.route('/', methods = ["GET", "POST"])
@app.route('/index/', methods = ["GET", "POST"])
def index():
	payload = {
		"common_captcha_source": common_captcha_source(),
		"text_captcha_source": text_captcha_source()
	}
	# Обработка ПОСТ запросов
	if request.method == 'POST':
		if "recaptcha_invisible_btn" in request.form:
			print(request.form)
		# Обработка новой рекапчи
		elif "solvemedia_btn" in request.form:
			return SolveMedia().answer_handler(request.form["adcopy_response"],
			                            request.form["adcopy_challenge"],
			                            request.environ['REMOTE_ADDR'])

	return render_template('base.html', doc = '/index.html', payload=payload)


@app.route('/invisible_recaptcha/', methods = ["GET", "POST"])
def invisible_recaptcha():
	# Обработка ПОСТ запросов
	if request.method == 'POST':
		if "recaptcha_invisible_btn" in request.form:
			print(request.form)
			
	return render_template('base.html', doc = '/invisible_recaptcha.html')




# Функция которая возвращает рандомное изображение обычной капчи
def common_captcha_source():
	# Получаем список всех изображений и возвращаем рандомную картинку
	images_list = os.listdir('application/static/image/common_image_example/')
	return random.choice(images_list)

# Функция которая возвращает рандомный вопрос текстовой капчи
def text_captcha_source():
	# Получаем список всех изображений и возвращаем рандомную картинку
	text_captcha_list = Database().get_text_captcha()
	return random.choice(text_captcha_list)
'''
API responses
'''
@app.route('/api/', methods=["GET", "POST"])
def api():
	# Обработка ПОСТ запросов
	if request.method == 'POST':
		# Обработка обычной капчи
		if "common_captcha_btn" in request.form:
			# Проверяем капчу и ответ на соответсвие
			return common_captcha_answer(request.form["common_captcha_src"],
			                             request.form["common_captcha_answer"])
		# Обработка новой рекапчи
		elif "recaptcha_new_btn" in request.form:
			return recaptcha_v2_new_answer(request.form["g-recaptcha-response"])
		# Обработка невидимой рекапчи
		elif "recaptcha_invisible_btn" in request.form:
			print(request.form)
		# Solvemedia капча
		elif "solvemedia_btn" in request.form:
			return SolveMedia().answer_handler(request.form["adcopy_response"],
					                            request.form["adcopy_challenge"],
					                            request.environ['REMOTE_ADDR'])
		# return recaptcha_v2_new_answer(request.form["g-recaptcha-response"])
	
	# Обработка ГЕТ запросов
	elif request.method == 'GET':
		if "get_common_captcha" in request.args["captcha_type"]:
			data = {'captcha_src': "http://85.255.8.26/static/image/common_image_example/" + common_captcha_source()}
			
			js = json.dumps(data)
			
			response = Response(js, status=200, mimetype='application/json')
			response.headers['Link'] = 'http://85.255.8.26/'
			return response
		
# Обработчик капчи изображением
def common_captcha_answer(captcha_name, user_answer):
	if user_answer == captcha_name.split(".")[0]:
		data = {'request': 'OK'}
		
		js = json.dumps(data)
		
		response = Response(js, status=200, mimetype='application/json')
		response.headers['Link'] = 'http://85.255.8.26/'
		
		return response
	else:
		data = {'request': 'FAIL'}
		
		js = json.dumps(data)
		
		response = Response(js, status=200, mimetype='application/json')
		response.headers['Link'] = 'http://85.255.8.26/'
		
		return response
# Обработчик новой рекапчи версии 2
def recaptcha_v2_new_answer(g_recaptcha_response):
	# Проверяем решил ли юзер капчу
	payload = {
				"secret": "6Lf77CsUAAAAAMJ1yJWbEG1VyVYKIQZWVQJRg25t",
				"response": g_recaptcha_response,
				}
	# Отсылаем запрос на правильность капчи
	captcha_answer = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)

	if captcha_answer.json()["success"]=="true":
		data = {'request': 'OK'}
		
		js = json.dumps(data)
		
		response = Response(js, status=200, mimetype='application/json')
		response.headers['Link'] = 'http://85.255.8.26/'
		
		return response
	else:
		data = {'request': 'FAIL'}
		# Если есть ошибки - высылаем и их
		if "error-codes" in captcha_answer.json() and captcha_answer.json()["error-codes"]!=[]:
			data.update({"recaptcha_error": captcha_answer.json()["error-codes"]})
		
		js = json.dumps(data)
		
		response = Response(js, status=200, mimetype='application/json')
		response.headers['Link'] = 'http://85.255.8.26/'
		
		return response
# Обработчик невидимой капчи
def recaptcha_invisible_answer(g_recaptcha_response):
		# Проверяем решил ли юзер капчу
		payload = {
			"secret": "6LcC7SsUAAAAAEpiGi1CQO3uoQbfTCzreTBmtWmm",
			"response": g_recaptcha_response,
		}
		# Отсылаем запрос на правильность капчи
		captcha_answer = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
		
		if captcha_answer.json()["success"] == "true":
			data = {'request': 'OK'}
			
			js = json.dumps(data)
			
			response = Response(js, status=200, mimetype='application/json')
			response.headers['Link'] = 'http://85.255.8.26/'
			
			return response
		else:
			data = {'request': 'FAIL'}
			# Если есть ошибки - высылаем и их
			if "error-codes" in captcha_answer.json() and captcha_answer.json()["error-codes"] != []:
				data.update({"recaptcha_error": captcha_answer.json()["error-codes"]})
			
			js = json.dumps(data)
			
			response = Response(js, status=200, mimetype='application/json')
			response.headers['Link'] = 'http://85.255.8.26/'
			
			return response


# ERRORS
@app.errorhandler(404)
def page_not_found(e):
	return render_template('base.html', doc = 'mistakes/404.html')

@app.errorhandler(500)
def page_not_found(e):
	return render_template('base.html', doc = 'mistakes/500.html')