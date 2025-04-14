from pathlib import Path

from .main import MetabaseAPIClient


class MetabaseCli:
    """Управление объектами Metabase."""
    @staticmethod
    def dump_card(card_id: int, addr: str, user: str | None = None, passwd: str | None = None):
        """Вывести json-конфигурацию карточки metabase."""
        api = MetabaseAPIClient(addr=addr, user=user, passwd=passwd)
        print(api.get_card(card_id).model_dump_json(indent=4))

    @staticmethod
    def create_card(path: str, addr: str, user: str | None = None, passwd: str | None = None):
        """Создать карточку в metabase из json-файла конфигурации."""
        card_path = Path(path)
        api = MetabaseAPIClient(addr=addr, user=user, passwd=passwd)
        api.create_raw_card(card_path.read_bytes())
