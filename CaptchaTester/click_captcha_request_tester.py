import requests
import ClickCaptcha

"""
Этот пример показывает то как нужно работать с модулем для распознования обычной капчи,
на примере нашего сайта.
"""

#pass your api key from your RuCaptcha Account
RUCAPTCHA_KEY = ""
#pass link to recaptcha image as parameter
link = ""
clickcaptcha_link = "http://85.255.8.26/{0}".format(link)
#create an object and let it do the wordk
click_captcha = ClickCaptcha(RUCAPTCHA_KEY)
coordinates = click_captcha.captcha_handler(clickcaptcha_link)
print(coordinates)