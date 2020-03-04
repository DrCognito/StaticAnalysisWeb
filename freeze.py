from flask_frozen import Freezer
from app import app

freezer = Freezer(app)

# @freezer.register_generator
# def error_handlers():
#     yield "/404"

if __name__ == '__main__':
    freezer.freeze()