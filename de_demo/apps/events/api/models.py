from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl, NonNegativeFloat, NonNegativeInt


class EventRequest(BaseModel):
    dt: datetime = Field(description="event datetime")
    name: str = Field(description="event name e.g. 'view', 'click'")
    user_id: NonNegativeInt = Field(description="event user_id")
    url: HttpUrl = Field(description="event location")
    obj: str = Field(description="event object, e.g. 'page', 'button', 'url', 'recommendation'")
    obj_id: str = Field(default="", description="event object id, if present, e.g., "
                                                "checkout for button or url value for url")
    product_id: NonNegativeInt = Field(default=0, description="product_id if product related event")
    amount: NonNegativeFloat = Field(default=0.0, description="event amount if necessary, "
                                                              "e.g., recommendation price, "
                                                              "product price, "
                                                              "or cart amount")
    exp: dict[str, str] | None = Field(default=None, description="event experiment variants")
