# Booking Service
___


## Вступление
Booking Service был создан в рамках тестового задания. 
Его цель - создать приложение, для бронирования номера с возможностью 
фильтрации по определенным критериям.

## Возможности

Для пользователя:
- Просмотр номеров
- Фильтр номеров по категориям (цена, кол-во комнат, время бронирования)
- Авторизация/регистрация
- (A) Возможность бронирования номера
- (A) Просмотр/удаление бронирования определенного номера в профиле

> (A) - для авторизованных пользователей

<br>

Для администратора:
- Создание комнаты в Django-Admin
- Одобрение/удаление заявки на бронирование комнаты (Панель управления бронированием)
- Вкладка рядом с логином администратора появляется ссылка на Django-Admin
 ---

## Технологии
- Django 4.1.7
- Django Debug Toolbar 3.8.1
- Django Rest Framework 3.14.0
- PostgreSQL 15.2
- psycopg2 2.9.5



## Установка

1. Клонируйте репозиторий с GitHub
2. Активируйте виртуальное окружение
3. Установите зависимости
4. Создайте .env, в котором укажите Ваши переменные окружения для базы данных
5. Создайте миграции для базы данных


```
1)  git clone https://github.com/iNTENSY/djangoHotel.git

2)  venv\Scripts\activate 

3)  pip install -r requirements.txt

5)  python manage.py makemigrations
    python manage.py migrate    
```

## Документация к API

### Список доступных маршрутов

```
    api/v1/apartments-admin     (!)
    api/v1/apartments           
    api/v1/booking/             (!)
    api/v1/booking/<int:pk>     (A, !) 
    api/v1/create_booking/      (A)
```

> (!) - доступно для администратора <br>
> (A) - доступно для авторизованного пользователя <br>
> Если не указан какой-либо статус для запроса, значит ответ могут получить все


## Комментарий
Тестовое задание было довольно полезным для меня, я опробовал множество вариацией выполнения
его. Из-за отсутствия практического опыта и, соответственно, работы в командном проекте
было множество проблем, которые по итогу я смог исправить.
<br>
В данном проекте имеются недостатки, но из-за отсутствия требований в ТЗ - 
я решил пойти более простым путем, не делая того, чего не было явно указано.
Такими недостатками является кеширование определенных фрагментов для оптимизации сайта,
отсутствие логики для отклоненных заявлений на бронирование, отсутствие поля администратора,
который одобрил/отклонил заявление. Отсутствие также конкретного требования для написания API - была
проделана минимальная, как мне кажется, работа для создания более структурированной и полной архитектуры. <br>

В заключении, хочу добавить, что вся backend-логика проделана Даценко Дмитрием,
а frontend-часть (на скорую руку) была проделана Табырцей Даяной

Буду рад Вашему ответу и указанием на мои ошибки в проекте!
