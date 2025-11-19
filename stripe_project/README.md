# Stripe Django Payment Project

## 🚀 Функциональность

- ✅ Просмотр товаров с кнопкой оплаты
- ✅ Stripe Checkout Session для отдельных товаров
- ✅ Система заказов с несколькими товарами
- ✅ Скидки и налоги для заказов
- ✅ Мультивалютность (USD, EUR)
- ✅ Django Admin панель
- ✅ Docker контейнеризация
- ✅ Stripe Payment Intent

## 📦 Установка и запуск

### Локальная разработка

1. **Клонируйте репозиторий**
```bash
git clone <your-repo-url>
cd stripe_project

2. **Создайте виртуальное окружение**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac

venv\Scripts\activate     # Windows

3. **Установите зависимости**
```bash
pip install -r requirements.txt

4. **Настройте переменные окружения**
```bash
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
STRIPE_SECRET_KEY=sk_test_your_secret_key

5. **Примените миграции**
```bash
python manage.py makemigrations
python manage.py migrate

6. **Создайте суперпользователя**
```bash
python manage.py createsuperuser

7. **Запустите сервер**
```bash
python manage.py runserver
