from app.config.schema import Session, Users
from app.helpers.response_helper import ResponseHelper
from app.helpers.auth_helper import AuthHelper
from flask import request
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Query

from utils import default_or_int


class GetController:
    def __init__(self): pass

    def get_user_detail(self, **params):
        """
        Request Query Params
          `limit`: digit string @optional - `?limit=10` (default is 10) - `per_page`
          `last_id`: digit string @optional - `?last_id=0` (default is 0)
        """
        response_helper = ResponseHelper()
        limit = default_or_int(10, request.args.get('limit'))
        last_id = default_or_int(0, request.args.get('last_id'))
        with Session() as session:
            try:
                query = Query(Users, session).filter(Users.id > last_id)
                response_helper.set_data([data.get_item()
                                         for data in query.limit(limit).all()])
            except Exception as e:
                response_helper.set_to_failed(str(e), 400)
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
            else:
              response_helper.message = 'wrong password'
              response_helper.status = 403
              response_helper.remove_data()
          except Exception as e:
              status_code = 400
              if type(e) == NoResultFound: status_code = 404
              response_helper.set_to_failed(str(e), status_code)
          finally:
              return response_helper.get_response()
