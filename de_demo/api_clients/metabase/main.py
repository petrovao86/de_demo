from httpx import Client, URL

from .models import (
    AddDatabaseRequest, CardResponse, DatabaseSettings, SessionPropertiesResponse, SessionRequest,
    SetupRequest, SitePreferences, UserInfo, User
)


class MetabaseApiException(Exception):
    pass


class MetabaseAPIClient:
    def __init__(self, addr: str, user: str | None = None, passwd: str | None = None):
        self._client = Client()
        self._addr = addr
        if user and passwd:
            self.post_session(username=user, password=passwd)

    def _get(self, url, params=None):
        response = self._client.get(url, params=params)

        if response.status_code == 200:
            json_response = response.json()
        else:
            raise MetabaseApiException(response.text)

        if 'errors' in json_response:
            raise MetabaseApiException(json_response['errors'])

        return json_response

    def _post(self, url, params=None, headers=None, content=None):
        response = self._client.post(
            url,
            params=params,
            headers=headers,
            content=content
        )
        if response.status_code == 200:
            json_response = response.json()
        else:
            raise MetabaseApiException(response.text)

        if 'errors' in json_response:
            raise MetabaseApiException(json_response['errors'])

        return json_response

    def get_session_properties(self) -> SessionPropertiesResponse:
        return SessionPropertiesResponse.model_validate(self._get(
            url=URL(self._addr).join("/api/session/properties"),
        ))

    def setup_user(
            self, user_name: str, email: str, passwd: str, locale: str, site_name: str, token: str
    ):
        req = SetupRequest(
            invite=UserInfo(email=email, first_name=user_name, last_name=user_name),
            prefs=SitePreferences(site_locale=locale,
                                  site_name=site_name),
            token=token,
            user=User(email=email, first_name=user_name, last_name=user_name, password=passwd)
        )
        return self._post(
            url=URL(self._addr).join("/api/setup"),
            headers={"Content-Type": "application/json"},
            content=req.model_dump_json()
        )

    def add_database(self,
                     db_host: str, db_port: int, db_user: str, db_passwd: str,  db_name: str,
                     name: str, engine: str):
        req = AddDatabaseRequest(
            name=name,
            engine=engine,
            details=DatabaseSettings(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_passwd,
                dbname=db_name,
            )
        )
        return self._post(
            url=URL(self._addr).join("/api/database"),
            headers={"Content-Type": "application/json"},
            content=req.model_dump_json()
        )

    def post_session(self, username: str, password: str):
        req = SessionRequest(
            username=username,
            password=password
        )
        return self._post(
            url=URL(self._addr).join("/api/session/"),
            headers={"Content-Type": "application/json"},
            content=req.model_dump_json()
        )

    def get_card(self, card_id: int) -> CardResponse:
        return CardResponse.model_validate(self._get(
            url=URL(self._addr).join("/api/card/").join(str(card_id)),
        ))

    def create_raw_card(self, json: bytes):
        return self._post(
            url=URL(self._addr).join("/api/card/"),
            headers={"Content-Type": "application/json"},
            content=json
        )
