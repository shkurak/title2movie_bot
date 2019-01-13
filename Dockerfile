FROM python:3
ADD code/ /
RUN pip install -U aiogram
RUN pip install aiohttp
RUN pip install BeautifulSoup4
RUN pip install lxml
RUN pip install ujson
RUN pip install argparse