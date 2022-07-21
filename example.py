import asyncio

from smapi import SteamMarketHandler
from smapi.info import Currencies, Locales


async def loop_example(sm_api_object: SteamMarketHandler):
	async for _ in sm_api_object.loop():
		for lot in sm_api_object.get_as_dataclass:
			print(lot)


async def iterate_once_example(sm_api_object: SteamMarketHandler):
	await sm_api_object.iterate_once()

	for lot in sm_api_object.get_as_dataclass:
		print(lot)


async def main():
	sm_api_object = SteamMarketHandler(
			'AK-47 | Vulcan (Field-Tested)',
			quantity=30, language=Locales.UA, currency=Currencies.UAH
	)
	for lot in sm_api_object.get_as_dataclass:
		print(lot)

	for lot in sm_api_object.get_as_dict:
		print(lot)

	for lot in sm_api_object.sorted(with_stickers=True):
		print(lot)

	for lot in sm_api_object.filtered(price=True):
		print(lot)

	for lot in sm_api_object.filtered(sm_api_object.sorted(), name=False, item_type=False,
	                                  description=False, collection=False):
		print(lot)

	await iterate_once_example(sm_api_object)

	await asyncio.sleep(30)

	task = asyncio.create_task(loop_example(sm_api_object))

	await asyncio.sleep(90)

	task.cancel()


if __name__ == '__main__':
	asyncio.run(main())
