import requests


class _DataFetcher(object):
	""""""

	_url: str
	_user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
	                   '(KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
	_quantity: int
	_filter: str
	_country: str
	_language: str
	_currency: str

	def _get_page(self, link: str, params: dict['str', [str, int]] = None):
		if not (isinstance(link, str) and
		        isinstance(params, dict)):
			raise TypeError

		response = requests.get(link, params=params, headers={'user-agent': self._user_agent})

		if not response.status_code == 200:
			raise ConnectionError

		return response

	def _get_json(self, link: str, params: dict['str', [str, int]] = None) -> dict[str, [str, int]]:
		if not (isinstance(link, str) and
		        isinstance(params, dict)):
			raise TypeError

		response = self._get_page(link, params)
		return response.json()

	def _get_steam_market_page(self, start: int, count: int) -> dict[str, [str, int]]:
		if not (isinstance(start, int) and
		        isinstance(count, int)):
			raise TypeError

		# link = f'{self._url}/render/?filter={self._filter}&start={start}&count={count}' \
		#        f'&country={self._country}&language={self._language}&currency={self._currency}'

		link = f'{self._url}/render/'

		return self._get_json(link, params={
				'filter': self._filter, 'start': start, 'count': count,
				'country': self._country, 'language': self._language, 'currency': self._currency
		})

	def _get_float_api_page(self, lookup_link: str):
		if not isinstance(lookup_link, str):
			raise TypeError

		link = 'https://api.csgofloat.com/'

		return self._get_json(link, params={
				'url': lookup_link
		})

	# def get_icon(self, token: str):
	# 	if not isinstance(token, str):
	# 		raise TypeError
	#
	# 	link = f'https://community.cloudflare.steamstatic.com/economy/image/{token}'
	# 	response = self._get_page(link)
	#
	# 	return response.content
