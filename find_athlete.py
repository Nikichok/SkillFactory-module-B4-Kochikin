# импортируем модули стандартной библиотеки uuid и datetime
import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол пользователя
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения
    birthdate = sa.Column(sa.Text)
    # рост
    height = sa.Column(sa.Float)


class Athelete(Base):
    """
    Описывает структуру таблицы  для хранения данных спортсменов
    """
    # задаем название таблицы
    __tablename__ = 'athelete'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    # возраст спортсмена
    age = sa.Column(sa.Integer)
    # дата рождения пользователя
    birthdate = sa.Column(sa.Text)
    # пол спортсмена
    gender = sa.Column(sa.Text)
    # рост спортсмена
    height = sa.Column(sa.Float)
    # имя спортсмена
    name = sa.Column(sa.Text)
    # вес спортсмена
    weight = sa.Column(sa.Integer)
    # количество золотых медалей
    gold_medals = sa.Column(sa.Integer)
    # количество серебряных медалей
    silver_medals = sa.Column(sa.Integer)
    # количество бронзовых медалей
    bronze_medals = sa.Column(sa.Integer)
    # общее количество медалей
    total_medals = sa.Column(sa.Integer)
    # вид спорта
    sport = sa.Column(sa.Text)
    # страна
    country = sa.Column(sa.Text)


def connect_db():
    """
    Устанавливает соединение к базе данных и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()


def find_birthdate(user, session):
    """
    Производит поиск пользователя в таблице athelete с датой рождения ближайшей к дате рождения пользователя user

    """
	# составляем словарь дней рождения спортсменов
    athletes_list = session.query(Athelete).all()
    athlete_id_bd = {}
    for athlete in athletes_list:
	    bd = datetime.date.fromisoformat(athlete.birthdate)
	    athlete_id_bd[athlete.id] = bd
	    
	# задаем начальные условия для поиска
    user_bd = datetime.date.fromisoformat(user.birthdate)
    min_dist = None
    athlete_id = None
    athlete_bd = None

    # находим спортсмена с минимальным отличием даты рожденья
    for id_, bd in athlete_id_bd.items():
        dist = abs(user_bd - bd)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_bd = bd
    
    return athlete_id, athlete_bd


def find_height(user, session):
    """
    Ищет ближайшего по росту атлета к пользователю user
    """
	# составляем словарь роста спортсменов
    athletes_list = session.query(Athelete).all()
    atlhete_id_height = {athlete.id: athlete.height for athlete in athletes_list}

    # находим спортсмена с минимальным отличием даты рожденья
    user_height = user.height
    min_dist = None
    athlete_id = None
    athlete_height = None

    for id_, height in atlhete_id_height.items():
        if height is None:
            continue

        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_height = height
    
    return athlete_id, athlete_height


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод и выводит результаты поиска
    """
    session = connect_db()
    # просим пользователя ввести ID для поиска
    id_user = input("Введите ID пользователя для поиска: ")	
    # находим запись в таблице User, у которой поле User.id совпадает с параметром id_user
    query = session.query(User).filter(User.id == id_user)
    # проверяем наличие данного пользователя в таблице user
    if query.count():
        # находим ближайшего по дате рождения
        athelete_bd_id, athelete_birthdate = find_birthdate(query.first(), session)
        print("Ближайший спортсмен по дате рождения: {}, рожден {}".format(athelete_bd_id, athelete_birthdate))
        # находим ближайшего по росту
        athelete_height_id, athelete_height = find_height(query.first(), session)
        # вызываем функцию печати на экран результатов поиска
        print("Ближайший спортсмен по росту: {}, его рост {}".format(athelete_height_id, athelete_height))
	        
    else:
        print("Пользователь с таким ID отсутствует в таблице user :(")

if __name__ == "__main__":
    main()