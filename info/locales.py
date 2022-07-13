from dataclasses import dataclass


@dataclass
class Currency:
	currency_api: str
	currency_tag: str


@dataclass
class Locale:
	language: str


class Locales:
	US = Locale('english')
	UA = Locale('ukrainian')
	RU = Locale('russian')


class Currencies:
	USD = Currency('1', '$')
	UAH = Currency('18', '₴')
	RUB = Currency('5', '₽')
