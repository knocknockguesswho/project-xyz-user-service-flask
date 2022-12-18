from pymysql import IntegrityError
from app.config.schema import Session, Users
from app.helpers.response_helper import ResponseHelper
from flask import request
from sqlalchemy.orm import Query
from sqlalchemy.exc import NoResultFound

_ERROR_DATA_WITH_ID_NOT_FOUND_ = 'cannot find todo with id '

class UpdateController:
  def __init__(self): pass

  def update_username(self, **params):
    """
    TODO: need to more research about data similarly update

    this method is protected, need to authorize first.
    Request params
      `id`: int @required

    Request form
      `username`: str @required
    """
    response_helper = ResponseHelper()
    id = params['id']
    with Session() as session:
      try:
        username = request.form['username']
        query = Query(Users, session).filter(Users.id == id)
        if query.one():
          query.update({Users.username: username}, synchronize_session=False)
          session.commit()
          response_helper.remove_data()
      except IntegrityError:
        # rollback commit if input is satisfy the error of `IntegrityError`
        session.rollback()
      except Exception as e:
        status_code = 400
        msg = str(e)
        if e.__cause__ is not None: msg = str(e.__cause__)
        if type(e) == NoResultFound:
          status_code = 404
          msg = f'{_ERROR_DATA_WITH_ID_NOT_FOUND_}{id}'
        response_helper.set_to_failed(msg,status_code)
      finally:
        return response_helper.get_response()