from flask import Flask
from flask_cors import CORS
# from app.controllers.delete_controller import DeleteController
from app.controllers.get_controller import GetController
from app.controllers.post_controller import PostController
from app.controllers.update_controller import UpdateController


app = Flask(__name__)
# TODO: need to update cors when publishing
CORS(app, origins='*')


get_controller = GetController()
post_controller = PostController()
update_controller = UpdateController()
# delete_controller = DeleteController()

# region GET METHOD
@app.route('/')
def get_user():
    return get_controller.get_user_detail()

@app.route('/check-credential')
def check_credential():
    return get_controller.check_credential()

@app.route('/get-by-id/<int:id>')
def get_by_id(id: int):
  print(type(id))
  return get_controller.get_by_id(id=id)
# endregion GET METHOD


# region POST METHOD
@app.route('/add', methods=['POST'])
def add_user():
    return post_controller.add_user()
# endregion POST METHOD


# region PUT METHOD
@app.route('/update-username/<int:id>', methods=['PUT'])
def update_username(id: int):
  return update_controller.update_username(id=id)

@app.route('/update-password/<int:id>', methods=['PUT'])
def update_password(id: int):
  return update_controller.update_password(id=id)
# endregion PUT METHOD


# region DELETE METHOD

# endregion DELETE METHOD