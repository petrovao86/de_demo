from datetime import datetime, timedelta, timezone

import pytest

from de_demo.apps.events.generator.constants import Products, UserState
from de_demo.apps.events.generator.requests import view_page
from de_demo.apps.events.generator.user import User

NOW = datetime.now(timezone.utc)


@pytest.fixture(scope="function")
def leave_site(monkeypatch):
    def patched_serve_site(*_, **__):
        return None

    with monkeypatch.context() as m:
        m.setattr(User, '_serve_site', patched_serve_site)
        yield


@pytest.fixture(scope="function")
def stay_on_site(monkeypatch):
    def patched_serve_site(*_, **__):
        return [view_page(
            dt=NOW,
            url=Products.ANALOG.value.url,
            user_id=1,
            product_id=Products.ANALOG.value.id,
            amount=Products.ANALOG.value.price,
        )]

    with monkeypatch.context() as m:
        m.setattr(User, '_serve_site', patched_serve_site)
        yield


@pytest.fixture(scope="function")
def probably_active_user(monkeypatch):
    def patched_is_probably_active(*_, **__):
        return True

    with monkeypatch.context() as m:
        m.setattr(User, '_is_probably_active', patched_is_probably_active)
        yield


@pytest.fixture(scope="function")
def probably_inactive_user(monkeypatch):
    def patched_is_probably_active(*_, **__):
        return False

    with monkeypatch.context() as m:
        m.setattr(User, '_is_probably_active', patched_is_probably_active)
        yield


def test_probably_active_user(probably_active_user, stay_on_site):
    active_user = User(
        user_id=1,
        created_at=NOW,
        visits_per_day=2,
        last_event=view_page(
            dt=NOW,
            url=Products.MAIN.value.url,
            user_id=1,
            product_id=Products.MAIN.value.id,
            amount=Products.MAIN.value.price,
        ),
        state=UserState.ACTIVE
    )
    assert active_user._is_rate_limit((NOW+timedelta(seconds=1)).timestamp(), user_rps=0.5)
    assert not active_user._is_rate_limit((NOW+timedelta(seconds=2)).timestamp(), user_rps=0.5)
    assert active_user._is_active((NOW + timedelta(seconds=2)).timestamp())
    assert active_user.state == UserState.ACTIVE
    assert active_user.active_since == NOW.timestamp()

    active_user = User(
        user_id=1,
        created_at=NOW,
        visits_per_day=2,
        last_event=view_page(
            dt=NOW,
            url=Products.MAIN.value.url,
            user_id=1,
            product_id=Products.MAIN.value.id,
            amount=Products.MAIN.value.price,
        ),
        state=UserState.ACTIVE
    )
    e = active_user.events(NOW+timedelta(seconds=10), user_rps=0.5)
    assert e is not None
    assert active_user.state == UserState.ACTIVE
    assert active_user.active_since == NOW.timestamp()

    inactive_user = User(
        user_id=1,
        created_at=NOW,
        visits_per_day=2,
        last_event=view_page(
            dt=NOW,
            url=Products.MAIN.value.url,
            user_id=1,
            product_id=Products.MAIN.value.id,
            amount=Products.MAIN.value.price,
        ),
        state=UserState.SLEEP
    )

    assert inactive_user._is_rate_limit((NOW + timedelta(seconds=1)).timestamp(), user_rps=0.5)
    assert not inactive_user._is_rate_limit((NOW + timedelta(seconds=2)).timestamp(), user_rps=0.5)
    assert inactive_user._is_active((NOW + timedelta(seconds=2)).timestamp())
    assert inactive_user.state == UserState.SLEEP
    assert inactive_user.active_since == NOW.timestamp()

    inactive_user = User(
        user_id=1,
        created_at=NOW,
        visits_per_day=2,
        last_event=view_page(
            dt=NOW,
            url=Products.MAIN.value.url,
            user_id=1,
            product_id=Products.MAIN.value.id,
            amount=Products.MAIN.value.price,
        ),
        state=UserState.SLEEP
    )

    e = inactive_user.events(NOW + timedelta(seconds=10), user_rps=0.5)
    assert e is not None
    assert inactive_user.state == UserState.ACTIVE
    assert inactive_user.active_since == (NOW + timedelta(seconds=10)).timestamp()


def test_probably_active_leave_site(probably_active_user, leave_site):
    active_user = User(
        user_id=1,
        created_at=NOW,
        visits_per_day=2,
        last_event=view_page(
            dt=NOW,
            url=Products.MAIN.value.url,
            user_id=1,
            product_id=Products.MAIN.value.id,
            amount=Products.MAIN.value.price,
        ),
        state=UserState.ACTIVE
    )

    e = active_user.events(NOW+timedelta(seconds=10), user_rps=0.5)
    assert e is None
    assert active_user.state == UserState.SLEEP
    assert active_user.active_since == NOW.timestamp()

    inactive_user = User(
        user_id=1,
        created_at=NOW,
        visits_per_day=2,
        last_event=view_page(
            dt=NOW,
            url=Products.MAIN.value.url,
            user_id=1,
            product_id=Products.MAIN.value.id,
            amount=Products.MAIN.value.price,
        ),
        state=UserState.SLEEP
    )

    e = inactive_user.events(NOW + timedelta(seconds=10), user_rps=0.5)
    assert e is None
    assert inactive_user.state == UserState.SLEEP
    assert inactive_user.active_since == NOW.timestamp()


def test_probably_inactive_user(probably_inactive_user, stay_on_site):
    active_user = User(
        user_id=1,
        created_at=NOW,
        visits_per_day=2,
        last_event=view_page(
            dt=NOW,
            url=Products.MAIN.value.url,
            user_id=1,
            product_id=Products.MAIN.value.id,
            amount=Products.MAIN.value.price,
        ),
        state=UserState.ACTIVE
    )
    assert active_user._is_rate_limit((NOW+timedelta(seconds=1)).timestamp(), user_rps=0.5)
    assert not active_user._is_rate_limit((NOW+timedelta(seconds=2)).timestamp(), user_rps=0.5)
    assert active_user._is_active((NOW + timedelta(seconds=2)).timestamp())
    assert active_user.state == UserState.ACTIVE
    assert active_user.active_since == NOW.timestamp()

    active_user = User(
        user_id=1,
        created_at=NOW,
        visits_per_day=2,
        last_event=view_page(
            dt=NOW,
            url=Products.MAIN.value.url,
            user_id=1,
            product_id=Products.MAIN.value.id,
            amount=Products.MAIN.value.price,
        ),
        state=UserState.ACTIVE
    )
    e = active_user.events(NOW+timedelta(seconds=10), user_rps=0.5)
    assert e is not None
    assert active_user.state == UserState.ACTIVE
    assert active_user.active_since == NOW.timestamp()

    inactive_user = User(
        user_id=1,
        created_at=NOW,
        visits_per_day=2,
        last_event=view_page(
            dt=NOW,
            url=Products.MAIN.value.url,
            user_id=1,
            product_id=Products.MAIN.value.id,
            amount=Products.MAIN.value.price,
        ),
        state=UserState.SLEEP
    )

    assert inactive_user._is_rate_limit((NOW + timedelta(seconds=1)).timestamp(), user_rps=0.5)
    assert not inactive_user._is_rate_limit((NOW + timedelta(seconds=2)).timestamp(), user_rps=0.5)
    assert not inactive_user._is_active((NOW + timedelta(seconds=2)).timestamp())
    assert inactive_user.state == UserState.SLEEP
    assert inactive_user.active_since == NOW.timestamp()

    inactive_user = User(
        user_id=1,
        created_at=NOW,
        visits_per_day=2,
        last_event=view_page(
            dt=NOW,
            url=Products.MAIN.value.url,
            user_id=1,
            product_id=Products.MAIN.value.id,
            amount=Products.MAIN.value.price,
        ),
        state=UserState.SLEEP
    )

    e = inactive_user.events(NOW + timedelta(seconds=10), user_rps=0.5)
    assert e is None
    assert inactive_user.state == UserState.SLEEP
    assert inactive_user.active_since == NOW.timestamp()
