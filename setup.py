from setuptools import setup, find_packages

setup(
    name = 'event_handler',
    packages = find_packages(),
    version = '0.0.1',
    author = 'Igor Rozhkov',
    author_email = 'rozhkovigor@yandex.ru',
    url = 'https://github.com/mrmegapolys/event_handler/',
    install_requires = ['requests', 'gspread', 'oauth2client', 'bitrix24-python3-client'],
    license = 'MIT',
)