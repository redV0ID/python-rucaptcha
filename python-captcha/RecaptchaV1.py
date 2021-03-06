import CommonCaptcha

class RecaptchaV1:
	'''
	Данный метод подходит для решения ReCaptcha V1.
	Требуется передать API ключ сайта, ссылку на изображение и,по желанию, время ожидания решения капчи
	Подробней информацию смотрите в методе 'captcha_handler'
	'''
	def __init__(self, recaptcha_api, sleep_time=5):
		'''
		Инициализация нужных переменных, создание папки для изображений и кэша
        После завершения работы - удалются временные фалйы и папки
        Основная работа просиходит через метод решения обычной капчи
		:param recaptcha_api:  АПИ ключ капчи из кабинета пользователя
		:param sleep_time: Вермя ожидания решения капчи
		'''
		self.recaptcha_api = recaptcha_api
		self.sleep_time = sleep_time
		self.common_captcha = CommonCaptcha.CommonCaptcha(recaptcha_api=self.recaptcha_api, sleep_time=self.sleep_time)
		
		
	def captcha_handler(self, recaptcha_challenge_field):
		'''
		Загрузить страницу по ссылке src из элемента noscript и найти элемент с id recaptcha_challenge_field
		в исходном коде страницы. И вот этот элемент и отправить. Ссылка сформируется уже в скрипте.
		:param recaptcha_challenge_field: элемент с id recaptcha_challenge_field в исходном коде страницы
		:return: Возвращает решение капчи
		'''
		captcha_link = "www.google.com/recaptcha/api/image?c={0}".format(recaptcha_challenge_field)
		return self.common_captcha.captcha_handler(captcha_link=captcha_link)
	