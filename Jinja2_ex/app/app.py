from flask import Flask, abort, render_template
from flask import Flask, request, jsonify, abort
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

BASE_DIR = Path(__file__).parent
app = Flask(__name__)


app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'flask2.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UsersModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
    birth_date = db.Column(db.String(32))
    phone = db.Column(db.String(32))

    def __init__(self, login):
        self.login = login

    def __repr__(self):
        return f'Login ({self.login})'

    def to_dict(self):
        return {
            "id": self.id,
            "login": self.login,
            "last_name": self.last_name,
            "name": self.name,
            "surname": self.surname,
            "birth_date": self.birth_date,
            "phone": self.phone,
        }

    def to_list(self):
        return [self.id, self.login, self.last_name, self.name, self.surname, self.birth_date, self.phone]

# 'login', 'last_name', 'name', 'surname', 'birth_date', 'phone'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/names")
def names():
    # names = list()
    # with open("files/names.txt", encoding="utf-8") as f:
    #     for raw_line in f:
    #         names.append(raw_line.strip())
    # return "<br>".join(names)

    # name = "Владимир"
    # return render_template("names.html", name=name)

    entities = list()
    res = UsersModel.query.all()
    for entity in res:
        entities.append(entity.name)
    # with open("files/names.txt", encoding="utf-8") as f:
    #     for raw_line in f:
    #         entities.append(raw_line.strip())
    return render_template('names.html', entities=entities)


@app.route("/table")
def table():
    entities = list()
    res = UsersModel.query.all()
    for row in res:
        entities.append({'last_name': row.last_name,
                         'name': row.name,
                         'surname': row.surname})
    # entities = list()
    # with open("files/humans.txt", encoding="utf-8") as f:
    #     for raw_line in f:
    #         data = raw_line.strip().split(';')
    #         entities.append({'last_name': data[0],
    #                          'name': data[1],
    #                          'surname': data[2]})
    return render_template('table.html', entities=entities)


@app.route("/about")
def about():
    return "О нас"


@app.route("/users")
def users_list():
    entities = list()
    res = UsersModel.query.all()
    for row in res:
        entities.append({'login': row.login, 'last_name': row.last_name,
                         'name': row.name, 'surname': row.surname,
                         'birth_date': row.birth_date, 'phone': row.phone})
    # with open('files/users.txt', encoding="utf-8") as f:
    #     for raw_line in f:
    #         data = raw_line.strip().split(';')
    #         # entities.append({'login': data[0], 'last_name': data[1],
    #         #                  'name': data[2], 'surname': data[3],
    #         #                  'birth_date': data[4], 'phone': data[5]})
    #         entities.append(dict(
    #             zip(('login', 'last_name', 'name', 'surname', 'birth_date', 'phone'), data)))
    # # return render_template('users_list.html', entities=entities)
    return render_template('users_list.html', **{'entities': entities})


@app.route("/users/<login>")
def user_info(login):
    # item = None
    res = UsersModel.query.filter(UsersModel.login == login).all()
    if len(res) > 0:
        item = {'login': res[0].login, 'last_name': res[0].last_name, 'name': res[0].name,
                'surname': res[0].surname, 'birth_date': res[0].birth_date, 'phone': res[0].phone}
    # with open('files/users.txt', encoding="utf-8") as f:
    #     for raw_line in f:
    #         data = raw_line.strip().split(';')
    #         if data[0] == login:
    #             item = {'login': data[0], 'last_name': data[1], 'name': data[2],
    #                     'surname': data[3], 'birth_date': data[4], 'phone': data[5]}
    #             break
    # if item is None:
    else:
        abort(404, f'User login {login} not found')
    return render_template('user_info.html', item=item)


if __name__ == "__main__":
    app.run(debug=True)
