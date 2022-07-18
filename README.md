# SteamMarketAPI
> **SteamMarketAPi** is api that provides you to use the Steam Community Market for CS:GO game simplify, trought the fetching and parsing Steam Web and CSGO FLOAT APIs

## Comon Features
- Simple to use
- Asynchronous
- Fast

### Alert
> If you want to use this api heavily you should to host CSGO FLOAT API yourself
- [CSGO Float Api GitHub](https://github.com/csgofloat/inspect)

## Code Sample
> For more sample look to example.py
``` python
from smapi import SteamMarketHandler

smapi_object = SteamMarketHandler(
    'https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Vulcan%20%28Field-Tested%29',
    quantity=5  # 0 for all results
)

for lot in smapi_object.get_as_dataclass:
    print(lot)
```


### Installing
``` bash
pip3 install smapi
```
