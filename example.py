from smapi import SteamMarketHandler
from info import Locales, Currencies
import asyncio


async def main():
	smh_obj = SteamMarketHandler(
			'https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Vulcan%20%28Field-Tested%29',
			quantity=15, language=Locales.RU, currency=Currencies.UAH,
	)

	# for x in smh_obj.get_weapon_info:
	# 	print(x, len(smh_obj.get_weapon_info))

	# print(smh_obj.filtered(name=True, nametag=True))
	# print(smh_obj.sorted(True, True))

	# task = asyncio.create_task(smh_obj.iterate_once())

	# a = input('type a: ')
	# b = input('type b: ')
	#
	# print(a + b)

	print(SteamMarketHandler.sorted(smh_obj.filtered(nametag=True), with_stickers=False, with_nametag=True))
	# print(smh_obj.sorted(with_nametag=True))

	# await task
	#
	# print(smh_obj.get_weapon_info)

	# print('Program has been finished successfully')

if __name__ == '__main__':
	asyncio.run(main())
