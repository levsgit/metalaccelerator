# МеталлАкселератор

Веб-приложение для приема и обработки заявок от стартапов в сфере металлургии.

## Описание

МеталлАкселератор - это платформа, которая помогает инновационным проектам в металлургической отрасли найти инвестиции и поддержку. Проект включает в себя:

- Главную страницу с информацией о фонде
- Форму подачи заявок от стартапов
- Административную панель для просмотра заявок

## Технологии

- Python 3.x
- Flask
- SQLAlchemy
- HTML/CSS/JavaScript

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/metal-accelerator.git
cd metal-accelerator
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите приложение:
```bash
python app.py
```

## Структура проекта

```
metal-accelerator/
├── app.py              # Основной файл приложения
├── models.py           # Модели базы данных
├── requirements.txt    # Зависимости проекта
├── static/            # Статические файлы (CSS, JS, изображения)
│   ├── css/
│   ├── js/
│   └── images/
└── templates/         # HTML шаблоны
    ├── index.html
    ├── apply.html
    └── applications.html
```

## Лицензия

MIT 