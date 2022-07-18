from setuptools import setup, find_packages

setup(
		name='smapi',
		version='0.0.5',
		description='Fetching and parsing info from Steam Community Market and CSGO Float Apis',
		license='MIT',
		author='Mefgner',
		author_email='mefgner@gmail.com',
		url='https://github.com/Mefgner/SteamMarketAPI',
		packages=['smapi', 'smapi/data_handlers', 'smapi/info'],
		install_requires=['requests', 'bs4'],
		zip_safe=False
)
