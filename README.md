# SteamMarketAPI
> API that provides you to use the Steam Community Market for CS:GO game simplify.
``` python
from smapi import SteamMarketHandler

smapi_object = SteamMarketHandler(
    'https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Vulcan%20%28Field-Tested%29',
    quantity=30
)

for lot in sm_api_object.get_as_dataclass:
    print(lot)
```
