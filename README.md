# SteamMarketAPI
> **SteamMarketAPi** is api that provides you to use the Steam Community Market for CS:GO game simplify, trought the fetching and parsing lots info from Steam Community Market and CSGO Float APIs

## Common Features
- Simple to use
- Asynchronous
- Fast

### Alert
> If you want to use this api heavily you should to host CSGO FLOAT API yourself
- [CSGO Float Api GitHub](https://github.com/csgofloat/inspect)

## Code Sample
> For more samples look to [examples](https://github.com/Mefgner/SteamMarketAPI/blob/main/example.py)
``` python
from smapi import SteamMarketHandler

smapi_object = SteamMarketHandler(
    'https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Vulcan%20%28Field-Tested%29',
    quantity=30
)

for lot in smapi_object.get_as_dataclass:
    print(lot)
```


### Installing
``` bash
pip3 install smapi
```
