from pymysql import IntegrityError
from app.config.schema import Session, Users
from app.helpers.response_helper import ResponseHelper
from app.helpers.auth_helper import AuthHelper
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

  def update_password(self, **params):
    '''
    Request form
      `old_password`: str @required
      `new_password`: str @required
    '''
    id = params['id']
    response_helper = ResponseHelper()
    with Session() as session:
      try:
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        query = Query(Users, session).filter(Users.id == id)
        # 1. match old password from input with stored one, if match do the next phase otherwise set to failed
        stored_password = query.one().password
        password_match = AuthHelper().is_password_match(password=old_password, b64_password=stored_password)
        if password_match:
          # 2. update stored password with new password from input
          query.update({Users.password: AuthHelper().hash_password(new_password)}, synchronize_session=False)
          session.commit()
          response_helper.remove_data()
        else: response_helper.set_to_failed('wrong password', 403)
      except Exception as e:
        status_code = 400
        msg = str(e)
        if e.__cause__ is not None: msg = str(e.__cause__)
        elif type(e) == NoResultFound:
          status_code = 404
          msg = f'{_ERROR_DATA_WITH_ID_NOT_FOUND_}{id}'
        response_helper.set_to_failed(msg,status_code)
      finally:
        return response_helper.get_response()