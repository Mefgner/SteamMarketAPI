from dataclasses import dataclass


@dataclass
class Locale:
	country: str
	language: str
	currency: str


class Locales:
	US = Locale('us', 'english', '1')
	UA = Locale('ua', 'ukrainian', '18')
	RU = Locale('ru', 'russian', '5')
