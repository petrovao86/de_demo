import os
import socket
import subprocess
import time
from pathlib import Path
from typing import Optional, Union

from infi.clickhouse_orm.database import Database


class TestEnvironment:
    ch_port: Optional[int] = None
    ch_tcp_port: Optional[int] = None
    ch_user: Optional[str] = "user"
    ch_pass: Optional[str] = "pass"

    def __init__(
            self,
            compose_project_name: str = "test-de-demo",
            docker_compose_file: Union[str, Path] = None
    ):
        self.compose_project_name = compose_project_name
        self.docker_compose_file = (
                docker_compose_file and Path(docker_compose_file) or
                Path(__file__).parent.parent.parent / "docker" / "docker-compose.warehouse.yml"
        )

    def up(self):
        self.ch_port = self._get_free_port(start_port=10000)
        self.ch_tcp_port = self._get_free_port(start_port=self.ch_port)
        subprocess.run(
            [
                "docker",
                "compose",
                "--file", str(self.docker_compose_file.absolute().resolve()),
                "up",
                "--detach",
                "--build",
                "ch"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=self._env()
        )
        self.wait_ch()

    def wait_ch(self, timeout: int = 60):
        response = "0"
        waiting_started_at = time.monotonic()
        while response == "0":
            if time.monotonic() - waiting_started_at > timeout:
                raise Exception("Test clickhouse server wait timeout!")
            try:
                ch_db = Database(
                    "default", db_url=self.ch_url, username=self.ch_user, password=self.ch_pass
                )
                response = ch_db.raw(f"SELECT 1").strip()
            except Exception:  # noqa
                pass
            time.sleep(1)

        time.sleep(5)

    @staticmethod
    def _get_free_port(start_port: int):
        port = start_port + 1
        while port < 65535:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                connection_result = s.connect_ex(('127.0.0.1', port))

            if connection_result != 0:
                return port
            port += 1

    def _env(self):
        env = os.environ.copy()
        env.update({
            "CH_HTTP_PORT": str(self.ch_port),
            "CH_TCP_PORT": str(self.ch_tcp_port),
            "CLICKHOUSE_USER": self.ch_user,
            "CLICKHOUSE_PASSWORD": self.ch_pass,
            "COMPOSE_PROJECT_NAME": self.compose_project_name,
        })
        return env

    def down(self):
        subprocess.run(
            [
                "docker",
                "compose",
                "--file", str(self.docker_compose_file.absolute().resolve()),
                "down",
                "--volumes",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=self._env()
        )
        self.ch_port = None

    def stop_service(self, service):
        subprocess.run(
            [
                "docker",
                "compose",
                "--file", str(self.docker_compose_file.absolute().resolve()),
                "stop",
                service,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=self._env()
        )

    def start_service(self, service):
        subprocess.run(
            [
                "docker",
                "compose",
                "--file", str(self.docker_compose_file.absolute().resolve()),
                "start",
                service,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=self._env()
        )
        self.wait_ch()

    @property
    def ch_url(self):
        return f"http://127.0.0.1:{self.ch_port}"
