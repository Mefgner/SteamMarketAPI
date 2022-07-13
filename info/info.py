from dataclasses import dataclass


@dataclass
class Price:
	value: float | int
	tag: str

	def __str__(self):
		return f'{self.value}{self.tag}'

	def __float__(self):
		return float(self.value) if not isinstance(self.value, float) else self.value

	def __int__(self):
		return int(self.value) if not isinstance(self.value, int) else self.value


@dataclass
class Sticker:
	name: str
	img_link: str
	slot: int
	wear: float


@dataclass
class WeaponInfo:
	name: str
	weapon_type: str
	rarity: str
	description: str
	collection: str
	price: Price
	stickers: list[Sticker]
	nametag: str
	lookup_link: str
	img_link: str
	wear: float
	paint_seed: int
	paint_index: int
