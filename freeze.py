from flask_frozen import Freezer
from app import app
from local import make_index

freezer = Freezer(app)

# @freezer.register_generator
# def error_handlers():
#     yield "/404"

if __name__ == "__main__":
    # Update the index before we freeze
    make_index()
    freezer.freeze()
