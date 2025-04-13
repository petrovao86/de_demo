from pathlib import Path

from de_demo.api_clients.metabase.main import MetabaseAPIClient


def migrate(addr: str,
            email: str, user_name: str, passwd: str,
            locale: str, site_name: str,
            engine: str, name: str,
            db_host: str, db_port: int, db_user: str, db_passwd: str, db_name: str
            ):
    api = MetabaseAPIClient(addr)
    prop = api.get_session_properties()
    if not prop.has_user_setup:
        api.setup_user(
            user_name=user_name,
            email=email,
            passwd=passwd,
            locale=locale,
            site_name=site_name,
            token=prop.setup_token,
        )
        api.add_database(
            name=name,
            engine=engine,
            db_host=db_host,
            db_port=db_port,
            db_user=db_user,
            db_passwd=db_passwd,
            db_name=db_name,

        )
        add_cards(api)


def add_cards(api: MetabaseAPIClient):
    cards = sorted((Path(__file__).parent / "cards").glob("*.json"))
    for card in cards:
        api.create_raw_card(card.read_bytes())
