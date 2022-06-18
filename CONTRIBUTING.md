# Разработка сервиса

## Рабочее окружение
Для начала разработки необходимо настроить рабочее окружение. Нам понадобятся следующие системные зависимости: 
- [python](https://www.python.org/downloads/) версии 3.7 или выше (чистый python, не anaconda)
- инструмент для коммит-хуков [pre-commit](https://pre-commit.com/)

Настройка окружения:
1. Настроить репозиторий
    ```shell script
    git clone git@github.com:SergeyAbdorin/aiohttp-template-service.git service_name
    cd service_name
    ```
2. Установить зависимости. Зависимости установятся в виртуальное окружение.
    ```shell script
    pip install -r requirements.txt
    ```
3. Настроить commit хуки.
    ```shell script
    pre-commit install --install-hooks
    ```

## Тестирование
Для запуска юнит тестов из виртуального окружения используется команда:
```shell script
PYTHONPATH="$PWD/src" pytest
```
Или через коммит хуки:
```shell script
git add . && pre-commit run test
```

Запуск линтера:
```shell script
git add . && pre-commit run lint --all-files
```

## Коммит хуки
Коммит хуки будут срабатывать автоматически при коммитах, но можно их запустить и в ручную:
```shell script
pre-commit run lint --all-files
```
pre-commit работает только на тех файлах, которые проиндексированы гитом, поэтому если хотим, чтобы вручную скрипты запускались на последней версии исходников нужно прописать:
```shell script
git add .
```
Или можно скомбинировать эти команды для простоты:
```shell script
git add . && pre-commit run lint --all-files
```

## Изменение API

После внесения изменений в схему API нужно:
- откорректировать версию и запустить скрипт [tools/apispec/generate.py](tools/apispec/generate.py).
    Результатом будет файл swagger.yaml в соответствующей папке в [public/docs](./public/docs).
- добавить ссылку в [index.html](./public/index.html) на `api_view.html` новой версии
