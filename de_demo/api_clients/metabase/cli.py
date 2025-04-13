from pathlib import Path

from .main import MetabaseAPIClient


class MetabaseCli:
    def __init__(self, addr: str, user: str | None = None, passwd: str | None = None):
        self._client = MetabaseAPIClient(addr=addr, user=user, passwd=passwd)

    def dump_card(self, card_id: int):
        print(self._client.get_card(card_id).model_dump_json(indent=4))

    def create_card(self, path: str):
        card_path = Path(path)
        self._client.create_raw_card(card_path.read_bytes())
