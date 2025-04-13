from datetime import datetime, timedelta, timezone
from math import exp, gamma, pi, sin
from random import choices

from infi.clickhouse_orm.database import Database

from ..api.models import EventRequest
from ..warehouse.models import Events
from .constants import UserState
from .user import User


class Generator:
    def __init__(
            self,
            dau: int,
            user_rps: float,
            user_age: int,
            visits_per_day: float,
            start_dt: datetime | None = None,
            users: list[User] | None = None
    ):
        self._dau = dau
        if user_rps >= 1:
            raise ValueError("ddos detected")
        self._user_rps = user_rps

        self._user_age = user_age
        self._ua_k = 3
        self._ua_lambda = self._user_age / (gamma(1 + 1 / self._ua_k))

        self._visits_per_day = visits_per_day
        start_dt = start_dt or datetime.now(timezone.utc)
        self._start_ts = start_dt.timestamp()
        self._now = self._start_ts
        self._users = users or []
        self.last_user_id = self._users and max(user.user_id for user in self._users) or 0

    def users_cnt(self, ts: float):
        return self._dau * (ts - self._now) / (24 * 60 * 60) * (1 + sin(2 * pi * (ts % (24 * 60 * 60) - 7 * 60 * 60) / (24 * 60 * 60) + pi / 2))

    def is_user_stay(self, user_created_at: float, ts: float):
        t = self._now - user_created_at
        dt = ts - self._now
        prob = exp(-1 * (pow((t + dt) / self._ua_lambda, self._ua_k) - pow(t / self._ua_lambda, self._ua_k)))
        return choices([True, False], weights=[prob, 1 - prob])[0]

    def events(self, now: datetime | None = None) -> list[EventRequest]:
        now = now or datetime.now(timezone.utc)
        day_started_at = (now - timedelta(days=1)).timestamp()
        now_ts = now.timestamp()

        users_cnt = self.users_cnt(now_ts)
        if users_cnt < 1:
            return []

        stay_users = []

        events = []
        for user in self._users:
            if self.is_user_stay(user.created_at, now_ts):
                stay_users.append(user)
                user_events = []
                for second in range(int(now_ts - self._now)):
                    step_events = user.events(now + timedelta(seconds=second))
                    if step_events:
                        user_events += step_events

                events += user_events

        dau_users = sum(1 for user in stay_users
                        if user.last_event_at and user.last_event_at >= day_started_at)
        new_users = []
        if dau_users < self._dau:
            for user_id in range(self.last_user_id + 1, self.last_user_id + 1 + int(users_cnt)):
                self.last_user_id = user_id
                new_users.append(User(
                    user_id=user_id, created_at=now, state=UserState.ACTIVE, active_since=now,
                    user_rps=self._user_rps, visits_per_day=self._visits_per_day
                ))

        self._users = new_users + stay_users
        if events:
            self._now = now_ts
        return events

    def run(
            self,
            from_dt: datetime,
            to_dt: datetime,
            db_addr: str,
            db_name: str,
            db_user: str,
            db_passwd: str,
    ):
        now = from_dt
        self._start_ts = from_dt.timestamp()
        self._now = self._start_ts
        to_ts = to_dt.timestamp()

        events = []
        db = Database(db_name=db_name, db_url=db_addr, username=db_user, password=db_passwd)

        while to_ts > self._now:
            now = now + timedelta(seconds=1)
            events += self.events(now)
            if len(events) > 50000:
                db.insert((Events(**event.model_dump(mode="json")) for event in events))
                events = []

        db.insert((Events(**event.model_dump(mode="json")) for event in events))
