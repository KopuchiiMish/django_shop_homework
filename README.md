# Django Shop Project

## Рекомендуемое разрешение экрана для проекта 1920х1080

### Установка:

- Убедитесь, что у вас установлен python 3.11 или более новая версия
- Убедитесь, что у вас установлен PostgreSQL и запущен локальный сервер для базы данных
- Клонировать репозиторий
- Установить зависимости командой ```pip install -r requirements.txt```
- В файле .env.sample заполнить данные для работы с проектом и переименовать его в .env
- Запустить через команду ```python3 manage.py runserver```
- Опционально можно заполнить данные из data.json командой ```python3 manage.py loaddata data.json```
- Для создания роли модератора запустить команду ```python manage.py cm```, зайти в админку под администратором и
  выдать разрешение 'change_product' для модератора

### Используемые технологии:

- HTML-вёрстка
- CSS на основе шаблонов bootstrap
- Два вида кеширования(низкоуровневый для выборки категорий из БД, на уровне контроллера - страниц с контактами и
  карточки товара)
- Кастомный шаблонный тег
- Кастомный шаблонный фильтр
- Кастомная команда для заполнения БД по таблицам продуктов и категорий из файла, кастомная команда для создания
  суперпользователя, кастомная команда для создания модератора
- Разграничение ролей пользователей на уровне шаблонов и контроллеров:
    - Анонимный пользователь может просматривать блоги, продукты и категории
    - Зарегистрированный пользователь может просматривать, редактировать и удалять только свои продукты или блоги и
      просматривать категории
    - Модератор может просматривать и редактировать продукты(менять категорию продукта, признак публикации и описание)
    - Администратор может просматривать, редактировать и удалять любые продукты, блоги и категории(в админке)
- Используются формсеты для продуктов(версии)