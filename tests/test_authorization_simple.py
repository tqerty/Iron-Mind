# Три кавычки — большой комментарий на весь файл: pytest его не выполняет, только люди читают.
"""
Простые тесты авторизации под ваш проект Iron Mind (Flask + SQLite).
Как запустить в терминале из папки проекта:
pytest tests/test_authorization_simple.py -v
"""

# uuid — модуль, который умеет выдать случайную строку; нам нужна уникальная, чтобы логин не был «занят».
import uuid

# pytest — программа-тестировщик; декоратор @pytest.fixture ниже из этого модуля.
import pytest

# create_app — функция, которая собирает ваше веб-приложение Flask (как в run.py / приложении).
from app import create_app

# insert_user — кладёт одну строку в таблицу users в файле users.db.
from database.logic_db import insert_user

# secure — делает из пароля «хеш» для базы; check_password — проверяет пароль против хеша.
from database.security import secure, check_password


# def — объявление функции; имя test_* нужно pytest, чтобы он нашёл это как тест.
def test_password_hash_roundtrip():
    # """ ... """ — короткое описание теста для человека; pytest может показывать его при падении.
    """Проверяем: хеш от пароля потом принимает тот же пароль и отвергает чужой."""

    # raw — переменная, в ней пароль в открытом виде, как вводит пользователь (строка).
    raw = "password12"

    # hashed — результат secure: длинная строка, которую вы храните в БД, а не сам пароль.
    hashed = secure(raw)

    # assert — «обязательно должно быть True», иначе тест красный и pytest показывает ошибку.
    assert check_password(raw, hashed) is True

    # Вторая проверка: неправильный пароль не должен подходить к этому хешу.
    assert check_password("wrong_one", hashed) is False


# @pytest.fixture — помечаем функцию ниже: pytest сам вызовет её и подставит результат в тесты как аргумент.
@pytest.fixture
def client_with_user():
    # """ ... """ — что делает эта «фикстура» целиком.
    """Поднимаем приложение, создаём одного пользователя в БД, отдаём клиент и логин/пароль."""

    # app — объект Flask-приложения после create_app().
    app = create_app()

    # Включаем режим тестов у Flask: так принято помечать приложение при pytest.
    app.config["TESTING"] = True

    # login — строка логина; "u" + случайные буквы/цифры, чтобы каждый запуск теста был с новым логином.
    login = "u" + uuid.uuid4().hex[:10]

    # password — пароль пользователя в открытом виде только в тесте; в БД пойдёт хеш.
    password = "password12"

    # insert_user — записываем в БД имя, логин и уже ЗАХЕШИРОВАННЫЙ пароль (как у вас при регистрации).
    insert_user("Тест", login, secure(password))

    # with — контекстный менеджер: test_client() создаёт клиент и корректно его закрывает после блока.
    with app.test_client() as client:
        # yield — «отдай тесту client, login, password; когда тест закончится, выполнение вернётся сюда».
        yield client, login, password


# Тест принимает client_with_user — pytest сам вызовет фикстуру с тем же именем и подставит кортеж.
def test_get_autorization_guest_sees_message(client_with_user):
    # Описание: что именно проверяем человеческим языком.
    """Гость (без входа) открывает GET /autorization и видит ваше сообщение про отсутствие доступа."""

    # Распаковка: client — виртуальный браузер, _ и _ — логин/пароль нам здесь не нужны, поэтому подчёркивания.
    client, _, _ = client_with_user

    # client.get — как ввести в адресной строке /autorization и нажать Enter (метод GET).
    r = client.get("/autorization")

    # Статус 200 — «ответ получен», у вас даже без доступа возвращается 200 и текст.
    assert r.status_code == 200

    # Проверяем, что в HTML/тексте ответа есть ваша фраза для гостя.
    assert "У вас нет доступа" in r.get_data(as_text=True)


def test_post_wrong_password_shows_error(client_with_user):
    """Отправляем форму входа с НЕВЕРНЫМ паролем — должна быть ошибка «не нашлись»."""

    # Берём client и login из фикстуры; пароль не нужен — подставим свой неверный.
    client, login, _ = client_with_user

    # client.post — как нажать «Войти» в форме: метод POST на URL, data — поля формы по именам.
    r = client.post("/autorization", data={"login": login, "password": "not_the_password"})

    # У вас при ошибке входа тоже 200, но другой шаблон — это нормально для вашего кода.
    assert r.status_code == 200

    # Ищем текст проблемы, который вы передаёте в errors.html.
    assert "не нашлись" in r.get_data(as_text=True)


def test_post_ok_no_login_error(client_with_user):
    """Правильный логин и пароль — не должно быть сообщения «не нашлись»."""

    # Берём и клиент, и правильный логин, и правильный пароль из фикстуры.
    client, login, password = client_with_user

    # POST с верными данными — имитация успешного входа.
    r = client.post("/autorization", data={"login": login, "password": password})

    # Снова ожидаем успешный HTTP-код страницы после входа.
    assert r.status_code == 200

    # После успешного входа вы рендерите page.html, там не должно быть текста ошибки входа.
    assert "не нашлись" not in r.get_data(as_text=True)


def test_response_without_login_is_401():
    """Без session['login'] маршрут /response должен вернуть 401 — как у вас в if в начале view."""

    # Создаём приложение отдельно (этот тест не использует фикстуру с пользователем).
    app = create_app()

    # Тестовый режим Flask.
    app.config["TESTING"] = True

    # with app.test_client() — только клиент, без yield: удобно для одного блока запросов.
    with app.test_client() as client:
        # POST на /response с полем responsible — как в вашем request.form['responsible'].
        r = client.post("/response", data={"responsible": "привет"})

    # 401 — «не авторизован»; вы сами возвращаете этот код без логина.
    assert r.status_code == 401
