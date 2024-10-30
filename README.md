# Сервис-клиент

## Что это?

Это асинхронный клиент для криптобиржи Deribit (https://docs.deribit.com/), который каждую минуту через сокет забирает
с биржи текущую цену btc_usd и eth_usd (index price валюты) после
чего сохраняет в базу данных тикер валюты, текущую цену и время в UNIX timestamp.

Сервис имет API для обработки сохраненных данных. API имеет следующую функциональноть:

- Получение всех сохраненных данных по указанной валюте
- Получение последней цены валюты
- Получение цены валюты с фильтром по дате

## Стэк

- Ключевые библиотеки: asyncio, websockets
- Фреймворки: FastAPI
- База данных: SQLite
- ORM для работы с базой: SQLAlchemy
- Тестирование: pytest
- Контейнеризация: Docker

## Доступные эндпоинты API

- Получение всех сохраненных данных по указанной валюте

  - `/index_prices/all?ticker={ticker}`

  - Method: GET

  - `ticker` - валюта (btc_usd, eth_usd, ... )

---

- Получение последней цены валюты

  - `/index_prices/latest?ticker={ticker}`)

  - Method: GET

  - `ticker` - валюта (btc_usd, eth_usd, ... )

---

- Получение цены валюты с фильтром по дате

  - `/index_prices/date?ticker={ticker}&date={date}`

  - Method: GET

  - `ticker` - валюта (btc_usd, eth_usd, ... )

  - `date` - дата в формате DD.MM.YYYY

---

## Развертывание

### Docker

1. Клонируем репозиторий

```bash
git clone git@github.com:sitdoff/Deribit.git
```

2. Переходим в папку проекта и запускаем сборку контейнера, а так же запуск контейнера, командой

```bash
docker build --tag=sitdoff/deribit . \
  && docker run -it \
  -v deribit_db:/code/data \
  -p 8000:8000 \
  --name sitdoff-derebit \
  sitdoff/deribit:latest
```

3. API будет доступен по адрессу http://localhost:8000/, документация API - http://localhost:8000/docs
