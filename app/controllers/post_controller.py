from pymysql import IntegrityError
from app.config.schema import Session, Users
from app.helpers.response_helper import ResponseHelper
from flask import request

from utils import default_or_str


class PostController:
    def __init__(self): pass

    def add_user(self, **params):
        """
        Request Form
          `first_name`: str max 50char @required
          `last_name`: str max 50char @required
          `password`: str max 32char @required
          `username`: str max 32char @required @unique
          `email`: str max 50char @required @unique
          `avatar`: str max 512char @required
          `birth_date`: date string @required `YYYY-mm-dd`
          `country_code`: str max 2char @required
        """
        response_helper = ResponseHelper()
        with Session() as session:
            try:
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                email = request.form['email']
                username = request.form['username']
                password = request.form['password']
                avatar = default_or_str(None, request.form['avatar'])
                birth_date = request.form['birth_date']
                country_code = request.form['country_code']
                session.add(Users(first_name=first_name, last_name=last_name,
                                  birth_date=birth_date, email=email, username=username, password=password, avatar=avatar, country_code=country_code))
                session.commit()
                response_helper.remove_datas()
            except IntegrityError:
              # rollback commit if input is satisfy the error of `IntegrityError`
              session.rollback()
            except Exception as e:
                if e.__cause__ is not None: response_helper.set_to_failed(str(e.__cause__), 400)
                else: response_helper.set_to_failed(str(e), 400)
            finally:
                return response_helper.get_response()
