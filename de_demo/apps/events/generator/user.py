from datetime import datetime, timedelta, timezone
from math import exp, gamma, pow
from random import choices, expovariate

from ..api.models import EventRequest

from .constants import (
    Buttons, Pages, PRODUCTS_BY_URL, URLS, URLS_BY_URL, UserState, VISIT_FLOW,
    VISIT_FLOW_START
)

from .requests import click_button, click_url, view_page


def get_next_url(last_url: str) -> str | None:
    ind = URLS_BY_URL[last_url]
    next_weights = [weight for i, weight in enumerate(VISIT_FLOW[ind]) if i != ind]
    next_urls = [url for i, url in enumerate(URLS) if i != ind]
    next_weights.append(100 - sum(next_weights))
    next_urls.append(None)
    return choices(next_urls, next_weights)[0]


def get_start_url() -> str:
    return choices(URLS, VISIT_FLOW_START)[0]


class User:
    def __init__(
            self,
            user_id: int,
            created_at: datetime,
            visits_per_day: float,
            user_rps: float,
            last_event: EventRequest | None = None,
            state: UserState = UserState.SLEEP,
            active_since: datetime | None = None,
    ):
        self.user_id = user_id
        self.created_at = (created_at or datetime.now(timezone.utc)).timestamp()
        self.state = state

        self.last_event = last_event
        self.last_event_at = self.last_event and self.last_event.dt.timestamp()

        self.cart_amount = 0
        self.active_since = active_since and active_since.timestamp() or self.created_at
        self.visits_per_day = visits_per_day
        self.vpd_k = 2
        self.vpd_lambda = (24*60*60)/(self.visits_per_day*gamma(1+1/self.vpd_k))
        if user_rps >= 1:
            raise ValueError("bot detected: user rps gte 1")
        self.user_rps = user_rps

    def events(self, dt: datetime) -> list[EventRequest] | None:
        ts = dt.timestamp()
        if self._is_rate_limit(ts):
            return None
        if not self._is_active(ts):
            return None

        events = self._serve_site(dt)

        if events is None:
            self.state = UserState.SLEEP
            return None

        if self.state == UserState.SLEEP:
            self.active_since = ts
            self.state = UserState.ACTIVE

        return events

    def _is_rate_limit(self, ts: float) -> bool:
        if self.last_event_at is None:
            return False
        return ts - self.last_event_at < (1 / self.user_rps)

    def _is_active(self, ts: float):
        if self._is_probably_active(ts) and self.state == UserState.SLEEP:
            return True
        return self.state == UserState.ACTIVE

    def _is_probably_active(self, ts: float):
        t = self.last_event_at or self.created_at - self.active_since
        dt = ts - (self.last_event_at or self.created_at)
        prob = exp(-1 * (pow((t + dt) / self.vpd_lambda, self.vpd_k) - pow(t / self.vpd_lambda, self.vpd_k)))
        return choices([False, True], weights=[prob, 1-prob])[0]

    def _serve_site(self, dt: datetime) -> list[EventRequest] | None:
        last_url = self.last_event and str(self.last_event.url)

        if last_url:
            next_url = get_next_url(last_url)
        else:
            next_url = get_start_url()

        if next_url is None:
            self._set_last_event(None)
            return None
        events = []
        if next_url == Pages.CHECKOUT.value and last_url == Pages.CART.value and self.cart_amount == 0:
            return events
        elif next_url == Pages.CHECKOUT.value and last_url == Pages.CART.value and self.cart_amount > 0:
            events += [
                click_button(
                    dt - timedelta(seconds=1), last_url, self.user_id,
                    Buttons.CHECKOUT.value, amount=self.cart_amount
                ),
                view_page(dt, next_url, self.user_id, amount=self.cart_amount)
            ]
            self._set_last_event(events[-1])
            self.cart_amount = 0
        elif next_url in PRODUCTS_BY_URL:
            product = PRODUCTS_BY_URL.get(next_url)
            if last_url:
                events.append(click_url(
                    dt - timedelta(seconds=1), last_url, self.user_id, next_url, product.id,
                    product.price
                ))
            events.append(view_page(dt, next_url, self.user_id, product.id, product.price))

            if choices(
                    [True, False], [product.add_to_cart_prob, 100 - product.add_to_cart_prob]
            )[0]:
                events.append(click_button(
                    dt + timedelta(seconds=1), next_url, self.user_id,
                    Buttons.ADD_TO_CART.value, product.id, product.price
                ))
                self.cart_amount += product.price

            self._set_last_event(events[-1])
        elif next_url == Pages.CART.value:
            if last_url:
                events.append(click_url(
                    dt - timedelta(seconds=1), last_url, self.user_id,
                    next_url, amount=self.cart_amount
                ))
            events.append(view_page(dt, next_url, self.user_id, amount=self.cart_amount))
            self._set_last_event(events[-1])
        elif next_url:
            events.append(view_page(dt, next_url, self.user_id))
            self._set_last_event(events[-1])

        return events

    def _set_last_event(self, e: EventRequest | None):
        self.last_event = e
        if e:
            self.last_event_at = e.dt.timestamp()
