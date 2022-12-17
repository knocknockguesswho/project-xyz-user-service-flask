from multiprocessing import Process, Value
import time, sched
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
# endregion PUT METHOD


# region DELETE METHOD

# endregion DELETE METHOD



def record_loop(loop_on):
   while True:
      if loop_on.value == True:
         print("loop running")
      time.sleep(1)

if __name__ == "__main__":
   recording_on = Value('b', True)
   p = Process(target=record_loop, args=(recording_on,))
   p.start()  
   app.run(debug=True, use_reloader=False)
   p.join()
# def print_time(a='default'):
#   print('From print_time', time.time(), a)

# def print_some_times():
#   s = sched.scheduler(time.time, time.sleep)
#   print(time.time())
#   s.enter(10, 1, print_time)
#   s.enter(5, 1, print_time, argument=('keyword',))
#   s.enter(5, 2, print_time, argument=('positional',))
#   s.run()
#   print(time.time())
# print_some_times()