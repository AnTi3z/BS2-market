# BS2 market api
**Цель:** Изучение потребности в нативной реализации API для телеграмм игры Bastion Siege 2  
**Реализация:** Flask application.  
**Технологии:**  
- Python(3.8)
- Flask (2.0)
- MySQL(5.7) в качестве СУБД
- Библиотека peewee в качестве ORM
- uWSGI в качестве WSGI сервера + nginx в качестве проксирующего web-сервера
- Документация API оформлена в виде OpenAPI 3.0 спецификации (swagger)

API доступен по адресу: https://market.anti3z.ru/api/  
Документация (swagger UI):  https://market.anti3z.ru/doc/  
Пример использования API:  https://market.anti3z.ru/ (фронтенд на JavaScript с использованием библиотеки amCharts)  
