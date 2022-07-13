from bs4 import BeautifulSoup as bs
from .data_fetcher import _DataFetcher
from info import *


class _DataParser(_DataFetcher):
	""""""

	def _get_info(self) -> dict[str, [str, int]] | list[dict]:
		test = self._get_steam_market_page(0, 1)
		if not test['success']:
			raise RuntimeError

		total_count = test['total_count']
		if self._quantity > total_count or self._quantity == 0:
			self._quantity = total_count

		if self._quantity <= 100:
			return self._get_steam_market_page(0, self._quantity)
		elif self._quantity > 100:
			json_list = list()
			start, count = 0, 0

			while True:
				if total_count >= 100:
					count = 100
				elif total_count < 100:
					count = total_count
				total_count -= count

				json_list.append(self._get_steam_market_page(start, count))

				start = count
				if total_count == 0:
					return json_list

	def _parse(self, raw: dict) -> list[WeaponInfo]:
		listing = raw['listinginfo']
		assets = raw['assets']
		listing_info_keys: list = [x for x in listing]
		assets_keys: list = [x for x in assets['730']['2']]

		weapons_list = list()
		while True:
			# name: str
			# weapon_type: str
			# rarity: str
			# description: str
			# collection: str
			# price: Price
			stickers: list[Sticker] | None = list()
			# nametag: str | None
			# lookup_link: str
			# icon_link: str
			# weapon_wear: float
			# paint_seed: int
			# paint_index: int

			sticker_icon_links: list[str]
			sticker_names: list[str] | str
			sticker_slots: list[int] = list()
			sticker_wears: list[float] = list()

			# sticker_name: str
			# sticker_icon_link: str
			# sticker_slot: int
			# sticker_wear: float

			listing_info_key = listing_info_keys.pop(0)

			current_listing = listing[listing_info_key]
			current_listings_asset = current_listing['asset']

			listing_id = listing_info_key
			asset_id = current_listings_asset['id']

			lookup_link_form = current_listings_asset['market_actions'][0]['link']
			lookup_link = lookup_link_form.replace('%listingid%', listing_id).replace('%assetid%', asset_id)

			float_api_response = self._get_float_api_page(lookup_link)

			float_api_response_body = float_api_response['iteminfo']
			float_api_stickers = float_api_response_body['stickers']

			if not float_api_stickers == []:
				for sticker in float_api_stickers:
					sticker_slots.append(sticker['slot'])
					sticker_wears.append(sticker.get('wear', 0.0))

			weapon_wear = float_api_response_body['floatvalue']

			paint_seed = float_api_response_body['paintseed']
			paint_index = float_api_response_body['paintindex']

			converted_price = current_listing['converted_price']
			converted_fee = current_listing['converted_fee']
			price_float = (converted_price + converted_fee) / 100
			price = Price(price_float, self._currency_tag)

			assets_key = assets_keys.pop(0)

			current_assets = assets['730']['2'][assets_key]

			icon_token = current_assets['icon_url_large']
			icon_link = f'https://community.cloudflare.steamstatic.com/economy/image/{icon_token}'

			descriptions = current_assets['descriptions']
			description_html = descriptions[2]['value']
			raw = bs(description_html, 'html.parser').text
			collection = descriptions[4]['value']

			if (len(descriptions) == 7 and descriptions[6]['value'] != ' ') or len(descriptions) == 8:
				html_with_stickers = descriptions[len(descriptions) - 1]['value']
				raw_stickers = bs(html_with_stickers, 'html.parser')
				tag_with_stickers = raw_stickers.find('center')
				sticker_icons = tag_with_stickers.find_all('img')
				sticker_icon_links = [x['src'] for x in sticker_icons]
				raw_sticker_names = tag_with_stickers.text
				sticker_names = raw_sticker_names.split(':', 1)[1]
				sticker_names = sticker_names.strip()
				sticker_names = sticker_names.split(',')
				sticker_names = [line.strip() for line in sticker_names]

				while True:
					sticker_icon_link = sticker_icon_links.pop(0)
					sticker_name = sticker_names.pop(0)
					sticker_slot = sticker_slots.pop(0)
					sticker_wear = sticker_wears.pop(0)

					sticker = Sticker(sticker_name, sticker_icon_link, sticker_slot, sticker_wear)
					stickers.append(sticker)

					if sticker_icon_links == [] and sticker_names == [] and sticker_slots == [] and sticker_wears == []:
						break
					elif sticker_icon_links == [] or sticker_names == [] or sticker_slots == [] or sticker_wears == []:
						raise RuntimeError(raw_sticker_names)  # ([sticker_icon_links, sticker_names, sticker_slots, sticker_wears])
			else:
				stickers = None

			name = current_assets['market_name']
			weapon_type_form = current_assets['type']
			if '—' in weapon_type_form:  # for Ukrainian language
				weapon_type, rarity = weapon_type_form.split('—')
			elif ',' in weapon_type_form:  # for Russian language
				weapon_type, rarity = weapon_type_form.split(',')
			else:  # for English language
				weapon_type, rarity = weapon_type_form.split(' ', 1)

			weapon_type = weapon_type.strip()
			rarity = rarity.strip().capitalize()

			nametag = current_assets.get('fraudwarnings', [None])[0]

			if nametag is not None:
				nametag = nametag.split(':')[1]
				nametag = nametag.strip()
				if "''" in nametag:
					nametag = nametag[2:-2]
				else:
					nametag = nametag[1:-1]

			weapon_info = WeaponInfo(name, weapon_type, rarity, description, collection, price, stickers,
			                         nametag, lookup_link, icon_link, weapon_wear, paint_seed, paint_index)

			weapons_list.append(weapon_info)

			if listing_info_keys == [] and assets_keys == []:
				return weapons_list

	def get_parsed_info(self) -> list[WeaponInfo]:
		raw_data = self._get_info()

		parse_result = list()
		if isinstance(raw_data, list):
			for item in raw_data:
				parse_result.extend(self._parse(item))
		else:
			parse_result.extend(self._parse(raw_data))

		return parse_result  # parse_result[0] if len(parse_result) == 1 else parse_result

	def __init__(self, url: str, user_agen: str = '', quantity: int = 0, query: str = '',
	             language: Locale = Locales.US, currency: Currency = Currencies.USD) -> None:
		if not (isinstance(url, str) and
		        isinstance(user_agen, str) and
		        isinstance(quantity, int) and
		        isinstance(query, str) and
		        isinstance(language, Locale) and
		        isinstance(currency, Currency)):
			raise TypeError

		self._url = url
		if not user_agen == '':
			self._user_agent = user_agen
		self._quantity = quantity
		self._filter = query
		self._language = language.language
		self._currency = currency.currency_api
		self._currency_tag = currency.currency_tag