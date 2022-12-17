from app.config.schema import Session, Todos
from app.helpers.response_helper import ResponseHelper
from sqlalchemy.orm import Query

class DeleteController:
  def __init__(self): pass

  def delete_one_by_id(self, **params):
    """
    Request Args
      `id`: int @required
    """
    response_helper = ResponseHelper()
    id = params['id']
    with Session() as session:
      try:
        Query(Todos, session).filter(Todos.id == id).delete(synchronize_session=False)
        response_helper.remove_datas()
      except Exception as e:
        response_helper.set_to_failed(str(e),400)
      finally:
        session.commit()
        return response_helper.get_response()

  def delete_all_todo(self, **param):
    response_helper = ResponseHelper()
    with Session() as session:
      try:
        Query(Todos, session).filter(Todos.id > 0).delete(synchronize_session=False)
        response_helper.remove_datas()
      except Exception as e:
        response_helper.set_to_failed(str(e),400)
      finally:
        session.commit()
        return response_helper.get_response()