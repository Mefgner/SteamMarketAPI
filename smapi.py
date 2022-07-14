from typing import Any
from dataclasses import asdict
from data_handlers import *
from info import *
import asyncio


class SteamMarketHandler:
	"""The class that provides you to automatize using of Community Market in Steam for CSGO the game."""

	def __init__(self, url: str, user_agen: str = '', quantity: int = 0, query: str = '',
	             language: Locale = Locales.US, currency: Currency = Currencies.USD) -> None:
		"""Intializator of Steam Market Handler class
		
		:param str url: Link to listing in Steam Community Market
		:param str user_agent: User agent for data gathering from internet, leave empty for using default value of it
		:param int quantity: Count of all lots that will be parsed, leave 0 to parse all items
		:param str query: Specified filter for gather data from Steam Market, use it if you want to get specific stickers just entered name of it
		:param Locale language: Language settings that you can pick from Locales class
		:param Currency currency: Currency settings that you can pick from Currencies class
		:raises TypeError: If some type doesn't match"""
		if not (isinstance(url, str) and
		        isinstance(user_agen, str) and
		        isinstance(quantity, int) and
		        isinstance(query, str) and
		        isinstance(language, Locale) and
		        isinstance(currency, Currency)):
			raise TypeError

		self.__DataFetcherObject = _DataParser(url, user_agen, quantity, query, language, currency)

		self._info: list[WeaponInfo] = self.__DataFetcherObject.get_parsed_info()

	async def iterate_once(self, interval: float | int = 0.0):
		"""Gather information in internet in corontine and puts it in itself
		
		:param float | int interval: Interval before information will be gathered"""

		await asyncio.sleep(interval)
		self._info = self.__DataFetcherObject.get_parsed_info()

	async def loop(self, interval: float | int = 30.0):
		"""Stars loop that will gather information with interval
		
		:param float | int interval: Interval before information will be gathered, min value is 30 seconds
		:raises ValueError: If interval less than 30 sesonds"""
		
		if interval < 30:
			raise ValueError

		while True:
			await self.iterate_once(interval)
			yield

	def _turn_to_dict(self) -> list[dict[str, Any]]:
		"""Returns list with dicts instead of WeaponInfo dataclasses
		
		:return: List with dicts
		:rtype: list"""
		return [asdict(item) for item in self._info]

	def sorted(self, with_stickers: bool = True, with_nametag: bool = True) -> list[dict[str, Any]]:
		"""Returns list of dicts only witch contains stickers or nametag
		
		Instead of self argument you can put list with dicts in not initialised class to use it with formated function
		
		:param bool with_stickers: Looking for lots only with stickers
		:param bool with_nametag: Looking for lots olny with nametag
		:return: List with dicts instead of WeaponInfo dataclasses
		:rtype list[dict[str, Any]]:
		:raises TypeError: If some types doesn't match"""
		if not ( isinstance(with_stickers, bool) and isinstance(with_nametag, bool)):
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

	def filtered(self, **kwargs) -> list[dict[str, Any]]:
		"""Returns only fields that you chose
		
		Instead of self argument you can put list with dicts in not initialiaed class to use it with sorted function in case if you left stickers or nametag fields
		
		:params dict[str, bool] **kwargs: To choose the fields that you want to leave just enter their name and set True value
		:return: List of dict instead of WeaponInfo dataclasses
		:rtype list[dict[str, Any]]:
		:raises TypeError: If value in **kwargs isn't bool type
		:raises ValueError: If WeaponInfo doesn't contains names of **kwargs"""

		if not isinstance(self, list):
			info = self._turn_to_dict()
		else:
			info = self

		for key in kwargs:
			if not (key in info[0] and isinstance(kwargs[key], bool)):
				raise ValueError

		for value in kwargs.values():
			if not isinstance(value, bool):
				raise TypeError

		filtered = list()
		for item in info:

			filtered_dict = dict()
			for key in kwargs:
				if kwargs[key]:
					filtered_dict.update({key: item[key]})

			filtered.append(filtered_dict)

		return filtered

	@property
	def get_weapon_info(self) -> list[WeaponInfo]:
		"""Returns info of all lots
		
		:return: List with WeaponInfo dataclasses
		:rtype list[WeaponInfo]:"""
		return self._info

	@property
	def get_weapon_info_as_dict(self) -> list[dict[str, Any]]:
		"""Returns info of all lots in dict form
		
		:return: List with dict representation of WeaponInfo dataclasses
		:rtype list[dict[str, Any]]:"""
		return self._turn_to_dict()
