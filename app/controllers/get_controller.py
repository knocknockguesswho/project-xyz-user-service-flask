from flask import request
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Query
from app.config.schema import Session, Users
from app.helpers.response_helper import ResponseHelper
from app.helpers.error_helper import ERROR_DATA_ID_NOT_FOUND, ERROR_DATA_USERNAME_NOT_FOUND

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

    def get_by_id(self, **params):
      response_helper = ResponseHelper()
      id = params['id']
      with Session() as session:
        try:
          query = Query(Users, session).filter(Users.id == id)
          response_helper.set_data(query.one().get_item())
        except Exception as e:
            status_code = 400
            msg = str(e)
            if e.__cause__ is not None: msg = str(e.__cause__)
            if type(e) == NoResultFound:
              msg = f'{ERROR_DATA_ID_NOT_FOUND, ERROR_DATA_USERNAME_NOT_FOUND}{id}'
              status_code = 404
            response_helper.set_to_failed(msg, status_code)
        finally:
            return response_helper.get_response()

    def get_by_username(self, **params):
      response_helper = ResponseHelper()
      with Session() as session:
        username = params['username']
        try:
          query = Query(Users, session).filter(Users.username == username)
          response_helper.set_data(query.one().get_item())
        except Exception as e:
          status_code = 400
          msg = str(e)
          if e.__cause__ is not None: msg = str(e.__cause__)
          if type(e) == NoResultFound:
            msg = f'{ERROR_DATA_USERNAME_NOT_FOUND}{username}'
            status_code = 404
          response_helper.set_to_failed(msg, status_code)
        finally:
          return response_helper.get_response()