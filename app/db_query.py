import psycopg2
import psycopg2.extras


# Создание соединения с базой данных
def conn():
    con = psycopg2.connect(
        database="dr_sch_db",
        user="admin",
        host="db",
        password="admin",
        port="5432"
    )
    return con


# Проверка типа учетной записи
def check_role(login: str):
    if login[0] == 't':
        return "instructors"
    elif login[0] == 's':
        return "students"
    else:
        return False


# Проверка совпадения логина
def check_auth(login: str):
    table = check_role(login)
    if not table:
        return False
    con = conn()
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        f"SELECT pwd FROM {table} WHERE lgn = %(login)s",
        {"login": login},
    )
    return cur.fetchall()


# Получить данные пользователя
def get_info(login: str, role: str):
    con = conn()
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if role == "instructors":
        cur.execute(
            """SELECT last_name, first_name, middle_name, phone
            FROM instructors
            WHERE lgn = %(login)s""",
            {"login": login},
        )
    else:
        cur.execute(
            """SELECT last_name, first_name, middle_name, num_group, phone
            FROM students
            WHERE lgn = %(login)s""",
            {"login": login},
        )
    return cur.fetchall()


# Получить результаты теста
def get_tests(login: str, role: str):
    con = conn()
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if role == "instructors":
        cur.execute(
            """SELECT st.lgn, last_name, first_name,
                      middle_name, st.num_group, test_1, test_2, test_3
            FROM students st JOIN schedule s ON st.num_group = s.num_group
            WHERE s.lgn = %(login)s""",
            {"login": login},
        )
    else:
        cur.execute(
            """SELECT test_1, test_2, test_3
            FROM students
            WHERE lgn = %(login)s""",
            {"login": login},
        )
    return cur.fetchall()


# Получить расписание
def get_schedule(login: str, role: str):
    con = conn()
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if role == "instructors":
        cur.execute(
            """SELECT num_group, mon, tue,	wed, thu, fri, sat,	sun
            FROM schedule
            WHERE lgn = %(login)s""",
            {"login": login},
        )
    else:
        cur.execute(
            """SELECT mon, tue,	wed, thu, fri, sat,	sun
            FROM schedule s JOIN students st ON s.num_group = st.num_group
            WHERE st.lgn = %(login)s""",
            {"login": login},
        )
    return cur.fetchall()


# Получить контакты
def get_contacts(login: str, role: str):
    con = conn()
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if role == "instructors":
        cur.execute(
            """SELECT st.num_group, last_name, first_name, middle_name, phone
            FROM students st JOIN schedule s ON st.num_group=s.num_group
            WHERE s.lgn=%(login)s""",
            {"login": login},
        )
    else:
        cur.execute(
            """SELECT i.last_name, i.first_name, i.middle_name, i.phone
            FROM instructors i JOIN schedule s ON i.lgn=s.lgn
            JOIN students st ON st.num_group=s.num_group
            WHERE st.lgn=%(login)s""",
            {"login": login},
        )
    return cur.fetchall()


# Получить данные по инструкторам
def get_inst() -> dict:
    con = conn()
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
            """SELECT lgn, last_name, first_name, middle_name
            FROM instructors
            """
        )
    return cur.fetchall()


# Получить данные по группам
def get_group() -> dict:
    con = conn()
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
            """SELECT num_group
            FROM schedule
            """
        )
    return cur.fetchall()


# Получить данные по студентам
def get_stud() -> dict:
    con = conn()
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
            """SELECT lgn, last_name, first_name, middle_name
            FROM students
            """
        )
    return cur.fetchall()


# Удалить студента
def del_stud(login: str):
    con = conn()
    cur = con.cursor()
    cur.execute(
        "DELETE FROM students WHERE lgn = %(login)s",
        {"login": login}
    )
    con.commit()
    return "OK"


# Удалить инструктора
def del_inst(login: str):
    con = conn()
    cur = con.cursor()
    cur.execute(
        "DELETE FROM instructors WHERE lgn = %(login)s",
        {"login": login}
    )
    con.commit()
    return "OK"


# Удалить инструктора
def del_group(num_group: str):
    con = conn()
    cur = con.cursor()
    cur.execute(
        "DELETE FROM schedule WHERE num_group = %(num_group)s",
        {"num_group": num_group}
    )
    con.commit()
    return "OK"


# Обновить результаты теста
def upd_test(login: str, test: str, mark: int):
    con = conn()
    cur = con.cursor()
    cur.execute(
        f"UPDATE students SET {test}=%(mark)s WHERE lgn = %(login)s",
        {"login": login, "mark": mark}
    )
    con.commit()
    return "OK"


# Добавить инструктора
def ins_inst(login: str, last_name: str, first_name: str,
             middle_name: str, phone: str, pwd: str):
    con = conn()
    cur = con.cursor()
    cur.execute(
        """INSERT INTO instructors (lgn, last_name, first_name,
        middle_name, phone, pwd)
        VALUES (%(login)s, %(last_name)s, %(first_name)s,
                %(middle_name)s, %(phone)s, %(pwd)s)""",
        {"login": login, "last_name": last_name, "first_name": first_name,
         "middle_name": middle_name, "phone": phone, "pwd": pwd}
    )
    con.commit()
    return "OK"


# Добавить группу с расписанием
def ins_group(num_group: str, login: str, mon: str, tue: str,
              wed: str, thu: str, fri: str, sat: str, sun: str):
    con = conn()
    cur = con.cursor()
    cur.execute(
        """INSERT INTO schedule (num_group, lgn, mon, tue,	wed, thu, fri, sat,	sun)
        VALUES (%(num_group)s, %(login)s, %(mon)s, %(tue)s,
                %(wed)s, %(thu)s, %(fri)s, %(sat)s, %(sun)s)""",
        {"num_group": num_group, "login": login, "mon": mon, "tue": tue,
         "wed": wed, "thu": thu, "fri": fri, "sat": sat, "sun": sun}
    )
    con.commit()
    return "OK"


# Добавить студента
def ins_stud(login: str, last_name: str, first_name: str, middle_name: str,
             phone: str, num_group: str, pwd: str):
    con = conn()
    cur = con.cursor()
    cur.execute(
        """INSERT INTO students (lgn, last_name, first_name,
                                 middle_name, phone, num_group, pwd)
        VALUES (%(login)s, %(last_name)s, %(first_name)s,
                %(middle_name)s, %(phone)s, %(num_group)s, %(pwd)s)""",
        {"login": login, "last_name": last_name, "first_name": first_name,
         "middle_name": middle_name, "num_group": num_group,
         "phone": phone, "pwd": pwd}
    )
    con.commit()
    return "OK"


# Обновить данные инструктора
def upd_inst(login: str, field: str, data: str):
    con = conn()
    cur = con.cursor()
    cur.execute(
        f"UPDATE instructors SET {field}=%(data)s WHERE lgn = %(login)s",
        {"login": login, "data": data}
    )
    con.commit()
    return "OK"


# Обновить данные студента
def upd_stud(login: str, field: str, data: str):
    con = conn()
    cur = con.cursor()
    cur.execute(
        f"UPDATE students SET {field}=%(data)s WHERE lgn = %(login)s",
        {"login": login, "data": data}
    )
    con.commit()
    return "OK"


# Обновить данные группы
def upd_group(num_group: str, field: str, data: str):
    con = conn()
    cur = con.cursor()
    cur.execute(
        f"UPDATE schedule SET {field}=%(data)s"
        + "WHERE num_group = %(num_group)s",
        {"num_group": num_group, "data": data}
    )
    con.commit()
    return "OK"
