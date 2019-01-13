# Movie2Title
The telegram bot [@title2movie_bot](https://web.telegram.org/#/im?p=@title2movie_bot) gives you a link where you can watch any movie you wish in response of your message with a title of a movie.

### Install
* Download repository
* Inside repository run 
```docker build -t title2movie_bot .```
### Run
* After installation run 
```docker run -idt title2movie_bot python ./bot.py --api_token <your_bot_api_token>```
* In case you wish specify proxy 
```docker run -idt title2movie_bot python ./bot.py --api_token <your_bot_api_token> --proxy <proxy_server>```
