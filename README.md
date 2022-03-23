# api_yamdb

*Групповой проект студентов Яндекс.Практикум по курсу **"API: интерфейс взаимодействия программ"***

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

**Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.**

В каждой категории есть произведения: книги, фильмы или музыка.

Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

___

## Запуск:
1. Клонируйте репозиторий на локальную машину.

    ``git clone git@github.com:avagners/api_yamdb.git``

2. Установите виртуальное окружение.

    ``python3 -m venv venv``

3. Активируйте виртуальное окружение.

    ``venv/bin/activate``

4. Установите зависимости.

    ``pip install -r requirements.txt``

5. Выполнить миграции и загрузить тестовые данные в базу:

    ``python3 manage.py import_test_data``

6. Запустите локальный сервер.

    ``python manage.py runserver``

7. Перейдите в документацию проекта.

    **[REDOC](http://127.0.0.1:8000/redoc/)**

---
## Над проектом работали:
**[Вагнер Александр](https://github.com/KorsakovPV)** - управление пользователями: система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения через e-mail.

**[Сущева Екатерина](https://github.com/MelatoZa)** - категории, жанры и произведения: модели, представления и эндпойнты для них.

**[Стельмахов Дмитрий](https://github.com/farmat2909)** - отзывы и комментарии: модели и представления, эндпойнты, права доступа для запросов. Рейтинги произведений.