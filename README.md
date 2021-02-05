<h1 align="center">
	Universal Checker Bot
</h1>
<p align="center">
<img src="https://img.shields.io/badge/aiogram-blue"> <img src="https://img.shields.io/badge/gevent-green"> <img src="https://img.shields.io/badge/flask-yellow"> <img src="https://img.shields.io/badge/mcstatus-purple"> <img src="https://img.shields.io/badge/icmplib-pink"> <img src="https://img.shields.io/badge/requests-black">
</p>

Данный бот служит для получения различной информации о хосте с нескольких нод. 
Часто возникают случаи, когда необходимо посмотреть, как поведет себя тот или инной ресурс с различных IP адресов. Например - посмотреть задержку или заблокирован ли порт для определенного региона.

 ### Работает это таким образом:

* На удаленные сервера устанавливается API-сервер
* На ещё один сервер(или рядом) устанавливается бот
* В настройках бота (в файле `nodes.py`) указываются адреса серверов API
* В зависимости от команды бот получает информацию с указанных нод
* Архитектура не отменяет того, что в боте есть команды, которые выполняются на хосте где установлен бот.

Все команды, которые есть сейчас, можно посмотреть [в самом боте](https://t.me/unicheckbot), для этого напишите в нём /start 

### Установка
* Установите git, docker и docker-compose
* Склонируйте репозиторий: `git clone https://github.com/catspace-dev/unicheckbot`
#### Установка API сервера
* Настройте параметры в `api.env`
* Запустите `docker-compose -f docker-compose-api.yml --env-file api.env up -d`
* В боте по пути `apps/tgbot/tgbot/nodes.py` добавьте ноду как указано в примере и перезапустите бота.
#### Установка бота
* Настройте параметры в `tgbot.env`
* Запустите `docker-compose -f docker-compose-tgbot.yml --env-file tgbot.env up -d`
