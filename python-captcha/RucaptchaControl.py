import requests

class RuСaptchaControl:
    def __init__(self, recaptcha_api):
        self.get_url = "http://rucaptcha.com/res.php"
        self.RECAPTCHA_KEY = recaptcha_api

    def get_balance(self):
        answer = requests.get(self.get_url+"?action=getbalance&json=1&key={0}".format(self.RECAPTCHA_KEY))
        print("Your balance is: ", answer.json()["request"], " rub.")
        return answer.json()

    def complaint_on_result(self, reported_id):
        answer = requests.get(self.get_url + "?action=reportbad&json=1&id={0}&key={1}".format(reported_id,
                                                                                              self.RECAPTCHA_KEY))
        if answer.json()["request"] == "OK_REPORT_RECORDED":
            print("Your report was sent successfully")
            return True
        else:
            print("Smth went wrong. Error: ",answer.json()["request"])
            return (False, answer.json()["request"])

