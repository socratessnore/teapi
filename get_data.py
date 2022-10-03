import requests
import re
from datetime import datetime, timedelta


class Authenticator:
    USERNAME = None
    PASSWORD = None

    AUTH_TOKEN = None
    COOKIES = None

    REQUEST = None

    BASE_URL = "https://energiaonline.turkuenergia.fi/"

    # Authentication
    INITIAL_REQUEST_URL = BASE_URL + "eServices/Online/IndexNoAuth"
    LOGIN_REQUEST_URL = BASE_URL + "eServices/Online/Login"
    LOGOUT_REQUEST_URL = BASE_URL + "eServices/Online/Logout"

    # Excel
    EXCEL_GENERATE_URL = (
        BASE_URL
        + "Reporting/CustomerConsumption/GenerateExcelFile?start={}&end={}&selectedTimeSpan=day"
    )
    EXCEL_DOWNLOAD_URL = (
        BASE_URL + "Reporting/CustomerConsumption/DownloadExcelFile?identifier={}"
    )

    def __init__(self, username, password, excel_name):
        self.USERNAME = username
        self.PASSWORD = password
        self.EXCEL_NAME = excel_name

        self.REQUEST = requests.Session()

    def logout(self):
        request = self.REQUEST.get(self.INITIAL_REQUEST_URL)

        if request.status_code == 200:
            return True

    def _refresh_form_token(self):
        request = self.REQUEST.get(self.INITIAL_REQUEST_URL)

        if request.status_code == 200:
            auth_token = re.search(
                b'name="__RequestVerificationToken" .*? value="(.*?)"', request.content
            )
            if auth_token:
                self.AUTH_TOKEN = auth_token.group(1)
                return True

    def _cookie_string(self):
        cookies = self.REQUEST.cookies.get_dict()
        cookie_string = ""
        for key in cookies:
            cookie_string = "{}{}={};".format(cookie_string, key, cookies[key])
        return cookie_string

    def _login_request(self):

        # POST Auth credentials with form value to login endpoint as FormData
        payload = {
            "__RequestVerificationToken": self.AUTH_TOKEN,
            "UserName": self.USERNAME,
            "Password": self.PASSWORD,
        }

        response = self.REQUEST.post(
            self.LOGIN_REQUEST_URL,
            headers={"Cookie": self._cookie_string()},
            data=payload,
        )

        if response.status_code == 200:
            return True

    def authenticate(self):
        if self._refresh_form_token():
            if self._login_request():
                return True

    def _fetch_excel_identifier(self):
        first_day = datetime.today() - timedelta(days=1)
        today = datetime.now().strftime("%Y-%m-%d")

        response = self.REQUEST.post(
            self.EXCEL_GENERATE_URL.format(first_day, first_day),
            headers={"Cookie": self._cookie_string()},
        )

        if response.status_code == 200:
            return response.json()["identifier"]

    def save_excel_to_file(self):
        excel_identifier = self._fetch_excel_identifier()

        response = self.REQUEST.get(
            self.EXCEL_DOWNLOAD_URL.format(excel_identifier),
            headers={"Cookie": self._cookie_string()},
        )

        if response.status_code == 200:
            output = open(self.EXCEL_NAME, "wb+")
            output.write(response.content)
            output.close()
            return self.EXCEL_NAME
