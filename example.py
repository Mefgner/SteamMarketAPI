from smapi import SteamMarketHandler
from info import Locales, Currencies
import asyncio


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
			'https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Vulcan%20%28Field-Tested%29',
			quantity=30, language=Locales.US, currency=Currencies.USD,
	)
	for lot in sm_api_object.get_as_dataclass:
		print(lot)

	for lot in sm_api_object.get_as_dict:
		print(lot)

	for lot in sm_api_object.sorted(with_stickers=True):
		print(lot)

	for lot in sm_api_object.filtered(price=True):
		print(lot)

	for lot in SteamMarketHandler.filtered(sm_api_object.sorted(), price=True, nametag=True, stickers=True):
		print(lot)

	await iterate_once_example(sm_api_object)

	await asyncio.sleep(30)

	task = asyncio.create_task(loop_example(sm_api_object))

	await asyncio.sleep(90)

	task.cancel()

if __name__ == '__main__':
	asyncio.run(main())
