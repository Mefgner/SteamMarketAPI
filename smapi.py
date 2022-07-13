from typing import Any
from dataclasses import asdict
from data_handlers import *
from info import *
import asyncio


class SteamMarketHandler:
	""""""

	def __init__(self, url: str, user_agen: str = '', quantity: int = 0, query: str = '',
	             language: Locale = Locales.US, currency: Currency = Currencies.USD) -> None:
		if not (isinstance(url, str) and
		        isinstance(user_agen, str) and
		        isinstance(quantity, int) and
		        isinstance(query, str) and
		        isinstance(language, Locale) and
		        isinstance(currency, Currency)):
			raise TypeError

		self.__DataFetcherObject = _DataParser(url, user_agen, quantity, query, language, currency)

		self._info: list[WeaponInfo] = self.__DataFetcherObject.get_parsed_info()

	async def iterate_once(self, interval: float | int = 30):
		if interval < 30:
			raise ValueError

		await asyncio.sleep(interval)
		self._info = self.__DataFetcherObject.get_parsed_info()

	async def loop(self, interval: float | int = 30.0):
		if interval < 30:
			raise ValueError

		while True:
			await self.iterate_once(interval)
			yield

	def _turn_to_dict(self):
		return [asdict(item) for item in self._info]

	def sorted(self, with_stickers: bool = True, with_nametag: bool = True) -> list[dict[str, Any]]:
		if not (isinstance(with_stickers, bool) and isinstance(with_nametag, bool)):
			raise TypeError

		if not isinstance(self, list):
			info = self._turn_to_dict()
		else:
			info = self
		sorted_info = list()

		for item in info:
			if (with_stickers and item.get('stickers')) and (with_nametag and item.get('nametag')):
				sorted_info.append(item)
			elif with_stickers and item.get('stickers'):
				sorted_info.append(item)
			elif with_nametag and item.get('nametag'):
				sorted_info.append(item)

		return sorted_info

	def filtered(self, **kwargs) -> list[dict[str, Any]]:  # __filter: tuple[bool] | list[bool]
		# if not (isinstance(__filter, tuple) or isinstance(__filter, list)):
		# 	raise TypeError
		if not isinstance(self, list):
			info = self._turn_to_dict()
		else:
			info = self

		for key in kwargs:
			if not (key in info[0] and isinstance(kwargs[key], bool)):
				raise ValueError

		for value in kwargs.values():
			if not isinstance(value, bool):
				raise ValueError

		# if not len(info[0]) == len(__filter):
		# 	raise ValueError(f'length of unfiltered - {len(info[0])} and length of filter - {len(__filter)}')

		filtered = list()
		for item in info:

			filtered_dict = dict()
			for key in kwargs:
				if kwargs[key]:
					filtered_dict.update({key: item[key]})

			filtered.append(filtered_dict)

		# for item in info:
		#
		# 	filtered_dict = dict()
		# 	for pos, field in enumerate(item):
		# 		if __filter[pos]:
		# 			filtered_dict.update({field: item[field]})
		#
		# 	filtered.append(filtered_dict)

		return filtered

	@property
	def get_weapon_info(self) -> list[WeaponInfo]:
		return self._info

	@property
	def get_weapon_info_as_dict(self) -> list[dict[str, Any]]:
		return self._turn_to_dict()
