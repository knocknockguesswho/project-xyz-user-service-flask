from flask import request
from sqlalchemy.orm import Query
from sqlalchemy.exc import NoResultFound, IntegrityError
# from pymysql import IntegrityError
from app.config.schema import Session, Users
from app.helpers.response_helper import ResponseHelper
from app.helpers.auth_helper import AuthHelper
from app.helpers.error_helper import ERROR_DATA_USERNAME_NOT_FOUND

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
                
                hashed_password = AuthHelper().hash_password(password=password)
                session.add(Users(first_name=first_name, last_name=last_name,
                                  birth_date=birth_date, email=email, username=username, password=hashed_password, avatar=avatar, country_code=country_code))
                session.commit()
                response_helper.remove_data()
            except IntegrityError as e:
              # rollback commit if input is satisfy the error of `IntegrityError`
              response_helper.set_to_failed(eval(str(e.__cause__))[1], 409)
              session.rollback()
            except Exception as e:
                msg = str(e)
                status = 400
                if e.__cause__ is not None: msg = str(e.__cause__)
                response_helper.set_to_failed(msg, status)
            finally:
                return response_helper.get_response()

    def check_credential(self, **params):
        """
        Request Form
          `password`: str max 32char @required
          `username`: str max 32char @required @unique
        """
        response_helper = ResponseHelper()
        with Session() as session:
          username = request.form['username']
          password = request.form['password']
          try:
            query = Query(Users, session).filter(Users.username == username)
            data_password = query.one().password
            password_match = AuthHelper().is_password_match(password=password, b64_password=data_password)
            if password_match: response_helper.set_data(query.one().get_item())
            else: response_helper.set_to_failed('wrong password', 403)
          except Exception as e:
              status_code = 400
              msg = str(e)
              if type(e) == NoResultFound:
                msg = f'{ERROR_DATA_USERNAME_NOT_FOUND}{username}'
                status_code = 404
              response_helper.set_to_failed(msg, status_code)
          finally:
              return response_helper.get_response()