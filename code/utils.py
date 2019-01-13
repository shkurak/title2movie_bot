from typing import List, Union, Tuple
from aiogram import types
import aiohttp
from messages import MESSAGES
from bs4 import BeautifulSoup
import ujson


HTTP_PROXY = "http://222.124.2.186:8080"
G_URL = 'https://www.google.ru/search'
HDREZKA_URL = "http://hdrezka.ag/index.php"


async def get_request(url: str, **kwargs) -> str:
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/27.0.1453.93 Safari/537.36'}
    kwargs["headers"] = header
    async with aiohttp.ClientSession() as session:
        async with session.get(url, **kwargs) as resp:
            text = await resp.text()
    return text


async def google_async(query: str) -> List[str]:
    text = await get_request(G_URL, params={'q': query})
    soup = BeautifulSoup(text, "lxml")
    urls = []
    for i, li in enumerate(soup.findAll('div', attrs={'class': 'r'})):
        link = li.find('a')
        url = link.get('href')
        urls.append(url)
    return urls


def get_imdb_title_id(urls) -> Union[None, str]:
    for url in urls:
        if url.startswith("https://www.imdb.com/title/"):
            return "https://www.imdb.com/title/" + url.split("/")[4] + "/"
    return None


async def parse_imdb(url: str) -> Tuple[str, str, str, str]:
    text = await get_request(url)
    soup = BeautifulSoup(text, "lxml")
    title = soup.title.text[:-7]
    js = ujson.loads(soup.select_one("script[type=application/ld+json]").text)
    desc = js.get("trailer", {}).get("description", None)
    if desc is None:
        mydivs = soup.find_all("div", {"class": "summary_text"})
        if mydivs:
            desc = mydivs[0].text.strip()
    original_name = js.get("name", "")
    image_url = js.get("image", None)
    return title, original_name, desc, image_url


async def hdrezka_search(query: str) -> str:
    text = await get_request(HDREZKA_URL,
                             params={"do": "search", "subaction": "search", 'q': query},
                             proxy=HTTP_PROXY)
    soup = BeautifulSoup(text, "lxml")
    return soup.findAll(attrs={'class': "b-content__inline_item-cover"})[0].find("a")["href"]


async def handle_request(text: str) -> types.MediaGroup:
    try:
        urls = await google_async(text + " imdb")
        url = get_imdb_title_id(urls)
        title, original_name, desc, image_url = await parse_imdb(url)
        film_url = await hdrezka_search(title + " " + original_name)
    except Exception as ext:
        title, original_name, desc, image_url, film_url = None, None, None, None, None

    await types.ChatActions.upload_photo()
    media = types.MediaGroup()
    if title is None or image_url is None:
        media.attach_photo('http://lorempixel.com/400/200/cats/', MESSAGES["cats"])
    else:
        if original_name in title:
            text_to_answer = title + "\n\n" + desc + "\n\n" + film_url
        else:
            text_to_answer = title + "\n\n" + original_name + "\n\n" + desc + "\n\n" + film_url
        media.attach_photo(image_url, text_to_answer)
    return media
