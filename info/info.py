from dataclasses import dataclass


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
	price: float
	stickers: list[Sticker]
	nametag: str
	lookup_link: str
	img_link: str
	wear: float
	paint_seed: int
	paint_index: int
