from dataclasses import dataclass
from enum import Enum, StrEnum


class Objects(StrEnum):
    PAGE = "page"
    BUTTON = "button"
    URL = "url"


class Pages(StrEnum):
    MAIN = "http://site/main"
    REGISTRATION = "http://site/registration"
    CATALOG = "http://site/catalog"
    PRODUCT = "http://site/catalog/product"
    CART = "http://site/cart"
    CHECKOUT = "http://site/cart/checkout"


@dataclass(frozen=True)
class Product:
    id: int
    price: float
    url: str
    add_to_cart_prob: int


class Products(Enum):
    MAIN = Product(id=1, price=100.0, url="http://site/catalog/product/1", add_to_cart_prob=10)
    RELATED = Product(id=2, price=10.0, url="http://site/catalog/product/2", add_to_cart_prob=7)
    ANALOG = Product(id=3, price=200.0, url="http://site/catalog/product/3", add_to_cart_prob=8)
    RELATED_ANALOG = Product(id=4, price=9.0, url="http://site/catalog/product/4", add_to_cart_prob=8)


PRODUCTS_BY_URL = {product.value.url: product.value for product in Products}

URLS = [
    Pages.MAIN.value,
    Pages.REGISTRATION.value,
    Pages.CATALOG.value,
    Products.MAIN.value.url,
    Products.RELATED.value.url,
    Products.ANALOG.value.url,
    Products.RELATED_ANALOG.value.url,
    Pages.CART.value,
    Pages.CHECKOUT.value
]

URLS_BY_URL = {u: i for i, u in enumerate(URLS)}


class Buttons(StrEnum):
    REGISTER = "register"
    ADD_TO_CART = "add_to_cart"
    CHECKOUT = "checkout"


class Events(StrEnum):
    VIEW = "view"
    CLICK = "click"


VISIT_FLOW = [
    [10, 5, 15,  1,  2,  1,  7, 30,  0],  # Pages.MAIN
    [10, 1, 35,  0,  0,  0,  0, 18,  0],  # Pages.REGISTRATION
    [4,  5, 38, 13,  7,  9,  8,  4,  0],  # Pages.CATALOG
    [5,  0,  0, 15, 13, 16, 15, 16,  0],  # Products.MAIN.value.url
    [6,  0,  0, 17, 18, 11, 19, 17,  0],  # Products.RELATED.value.url
    [0,  0,  0, 18, 15,  9,  0, 15,  0],  # Products.ANALOG.value.url
    [0,  0,  0, 19, 13,  0,  9, 18,  0],  # Products.RELATED_ANALOG.value.url
    [0, 13,  0,  7, 11,  5,  9,  0, 20],  # Pages.CART
    [0,  0,  0,  0,  0,  0,  0,  0,  0],  # Pages.CHECKOUT
]

VISIT_FLOW_START = [VISIT_FLOW[i][i] for i, _ in enumerate(URLS)]


class UserState(StrEnum):
    ACTIVE = 'active'
    SLEEP = 'sleep'
