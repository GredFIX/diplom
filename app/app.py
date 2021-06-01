from flask import (
    Flask,
    request,
    render_template,
    session,
    redirect,
    url_for
)
import db_query as db
import hashlib
import uuid
import os

# Пароль админа хранится в переменной окружения ADMIN_PWD
ADMIN_PWD = os.environ["ADMIN_PWD"]


# Хеширование пароля в формате sha256
def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode()
                          + password.encode()).hexdigest() + ':' + salt


# Сравнение пароля из формы авторизации
# с паролем из базы данных в формате sha256
def chk_pwd(hashed_pwd, user_pwd):
    pwd, salt = hashed_pwd.split(':')
    return pwd == hashlib.sha256(salt.encode() + user_pwd.encode()).hexdigest()


# Заменяет пустые поля из базы данных на пустую строку.
# Если пустое поле с тестом, то заменяет его на "Не сдавал"
def del_none(some_dict: dict):
    for raw in some_dict:
        for key, value in raw.items():
            if value is None:
                if "test_" in key:
                    raw[key] = 'Не сдавал'
                else:
                    raw[key] = ''


# Инициализация приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = 'wdnS0iEefb5JDl5JOD'


# Обработка авторизации
# Cначала проверяется текущий статус авторизации пользователя:
# если пользователь уже авторизован, то происходит перенаправление
# в личный кабинет пользователя в зависимости от его роли.
# Следующие два условия - проверка на запрос методом POST.
# Первое - проверка на авторизацию админа и, если всё совпадает,
# то пользователю присваиваается роль админа.
# Второе - проверка на авторизацию обычного пользователя.
# Если авторизация пройдёт успешно, то пользователю присваивается
# роль в соотвествии с его данными.
# Если ни одно условие не оказалось истинно, то происходит отрисовка
# страницы авторизации.
@app.route("/index", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def auth():
    if 'login' in session:
        if session['role'] == 'admin':
            return redirect(url_for('print_admin'))
        else:
            return redirect(url_for('account'))
    elif request.method == 'POST' and request.form['login'] == 'admin' \
            and chk_pwd(ADMIN_PWD, request.form['pass']):
        session['login'] = request.form['login']
        session['role'] = 'admin'
        return redirect(url_for('print_admin'))
    elif request.method == 'POST' and db.check_auth(request.form['login']):
        res = db.check_auth(request.form['login'])
        if not chk_pwd(res[0]['pwd'], request.form['pass']):
            return render_template('login.html', title='Авторизация')
        session['login'] = request.form['login']
        session['role'] = db.check_role(session['login'])
        return redirect(url_for('account'))
    return render_template('login.html', title='Авторизация')


# Обработка выхода из аккаунта
# Очищается кэш пользователя и происходит перенаправление
# на страницу авторизации
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth'))


# Отрисовка личного кабинета
# Заполняется данными в зависимости от роли пользователя
@app.route("/account")
def account():
    if 'login' not in session:
        return redirect(url_for('auth'))
    res = db.get_info(session['login'], session['role'])
    del_none(res)
    return render_template('account.html', title='Личный кабинет',
                           info=res[0], role=session['role'])


# Отрисовка страницы с методичками
@app.route("/metodics")
def print_metodics():
    if 'login' not in session:
        return redirect(url_for('auth'))
    return render_template('metodics.html', title='Методичка')


# Отрисовка и обработка запросов на странице с тестами
# Если приходит метод GET (обычный запрос), то
# отрисовывается в зависимости от роли
# Если метод POST, то происходит изменение
# результатов теста у студента, которого выбрал
# инструктор
@app.route("/tests", methods=['GET', 'POST'])
def print_tests():
    if 'login' not in session:
        return redirect(url_for('auth'))
    if request.method == 'POST' and session['role'] == 'instructors':
        res = db.upd_test(request.form['student'],
                          request.form['test'],
                          int(request.form['mark']))
        return redirect(url_for('print_tests'))
    res = db.get_tests(session['login'], session['role'])
    del_none(res)
    return render_template('tests.html', title='Тесты',
                           role=session['role'], table=res)


# Отрисовка страницы с расписанием
@app.route("/schedule")
def print_schedule():
    if 'login' not in session:
        return redirect(url_for('auth'))
    res = db.get_schedule(session['login'], session['role'])
    del_none(res)
    return render_template('schedule.html', title='Расписание',
                           role=session['role'], table=res)


# Отрисовка страницы с контактами
@app.route("/contacts")
def print_contacts():
    if 'login' not in session:
        return redirect(url_for('auth'))
    res = db.get_contacts(session['login'], session['role'])
    del_none(res)
    return render_template('contacts.html', title='Контакты',
                           role=session['role'], table=res)


# Отрисовка и обработка запросов на странице админа:
# При получении GET-запроса отрисовывает страницу админа.
# Каждому условие при получении метода POST соответствует
# следующее изменение в базе данных:
# 1 - добавление инструктора
# 2 - добавление группы
# 3 - добавление студента
# 4 - изменение данных инструктора
# 5 - изменение данных студента (кроме группы)
# 6 - изменение данных группы (кроме инструктора)
# 7 - изменение группы у студента
# 8 - изменение инструктора у группы
# 9 - удаление инструктора
# 10 - удаление студента
# 11 - удаление группы
@app.route("/admin", methods=['GET', 'POST'])
def print_admin():
    if 'login' not in session or session['role'] != 'admin':
        return redirect(url_for('auth'))
    if request.method == 'POST':
        if request.form['type'] == "ins_inst":
            res = db.ins_inst(request.form['login'],
                              request.form['last_name'],
                              request.form['first_name'],
                              request.form['middle_name'],
                              request.form['phone'],
                              hash_password(request.form['pwd']))
            return redirect(url_for('print_admin'))
        elif request.form['type'] == "ins_group":
            res = db.ins_group(request.form['num_group'],
                               request.form['login'],
                               request.form['mon'],
                               request.form['tue'],
                               request.form['wed'],
                               request.form['thu'],
                               request.form['fri'],
                               request.form['sat'],
                               request.form['sun'])
            return redirect(url_for('print_admin'))
        elif request.form['type'] == "ins_stud":
            res = db.ins_stud(request.form['login'],
                              request.form['last_name'],
                              request.form['first_name'],
                              request.form['middle_name'],
                              request.form['phone'],
                              request.form['num_group'],
                              hash_password(request.form['pwd']))
            return redirect(url_for('print_admin'))
        elif request.form['type'] == "upd_inst":
            if request.form['field'] == 'pwd':
                hash_password(request.form['data'])
            res = db.upd_inst(request.form['login'], 
                              request.form['field'],
                              request.form['data'])
            return redirect(url_for('print_admin'))
        elif request.form['type'] == "upd_stud":
            if request.form['field'] == 'pwd':
                hash_password(request.form['data'])
            res = db.upd_stud(request.form['login'], 
                              request.form['field'],
                              request.form['data'])
            return redirect(url_for('print_admin'))
        elif request.form['type'] == "upd_group":
            res = db.upd_group(request.form['num_group'],
                               request.form['field'],
                               request.form['data'])
            return redirect(url_for('print_admin'))
        elif request.form['type'] == "chg_group":
            res = db.upd_stud(request.form['login'], 
                              "num_group",
                              request.form['data'])
            return redirect(url_for('print_admin'))
        elif request.form['type'] == "chg_inst":
            res = db.upd_group(request.form['num_group'], 
                               "lgn",
                               request.form['data'])
            return redirect(url_for('print_admin'))
        elif request.form['type'] == "del_inst":
            res = db.del_inst(request.form['login'])
            return redirect(url_for('print_admin'))
        elif request.form['type'] == "del_stud":
            res = db.del_stud(request.form['login'])
            return redirect(url_for('print_admin'))
        elif request.form['type'] == "del_group":
            res = db.del_group(request.form['num_group'])
            return redirect(url_for('print_admin'))
    inst = db.get_inst()
    num_group = db.get_group()
    stud = db.get_stud()
    del_none(inst)
    del_none(num_group)
    del_none(stud)
    return render_template('admin.html', title='Панель админа',
                           inst=inst, num_group=num_group, stud=stud)


# Обработка и отрисовка ошибки 404 (страница не найдена)
@app.errorhandler(404)
def not_found(error):
    return render_template('page404.html', title="Ошибка 404")


# Запуск приложения
if __name__ == "__main__":
    app.run(host="0.0.0.0")
