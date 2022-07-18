from setuptools import setup
import os
import smapi


dist_dir = os.listdir('dist/')
for file in dist_dir:
	os.replace(f'dist/{file}', f'old_dist/{file}')

setup(
		name='smapi',
		keywords=['smapi', 'steam', 'community', 'market', 'csgo', 'cs:go', 'listings', 'float', 'api'],
		version=smapi.__version__,
		description='Fetching and parsing info from Steam Community Market and CSGO Float Apis',
		long_description=open('README.md', encoding='utf-8').read(),
		long_description_content_type='text/markdown',
		license='MIT',
		author='Mefgner',
		author_email='mefgner@gmail.com',
		url='https://github.com/Mefgner/SteamMarketAPI',
		packages=['smapi', 'smapi/data_handlers', 'smapi/info'],
		install_requires=['requests', 'bs4'],
		python_requires='>=3.7',
		zip_safe=False
)
