from datetime import datetime

from ..api.models import EventRequest

from .constants import Events, Objects


def click_url(
        dt: datetime, url, user_id, href, product_id: int = 0, amount: float = 0
) -> EventRequest:
    return page_event(dt, url, user_id,
                      Events.CLICK.value, Objects.URL.value, href, product_id, amount)


def click_button(
        dt: datetime, url, user_id, button, product_id: int = 0, amount: float = 0
) -> EventRequest:
    return page_event(dt, url, user_id,
                      Events.CLICK.value, Objects.BUTTON.value, button, product_id, amount)


def view_page(
        dt: datetime, url, user_id, product_id: int = 0, amount: float = 0
) -> EventRequest:
    ind = -1
    if product_id > 0:
        ind = -2
    return page_event(dt, url, user_id,
                      Events.VIEW.value, Objects.PAGE.value, url.split("/")[ind], product_id, amount)


def page_event(
        dt: datetime, url, user_id, event, obj, obj_id, product_id: int = 0, amount: float = 0
) -> EventRequest:
    return EventRequest(
        dt=dt,
        name=event,
        user_id=user_id,
        url=url,
        obj=obj,
        obj_id=obj_id,
        product_id=product_id,
        amount=amount,
    )



