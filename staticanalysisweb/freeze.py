from flask_frozen import Freezer
from staticanalysisweb.app import app
from local import make_index

# Stop frozen flask deleting netlify.toml
app.config['FREEZER_DESTINATION_IGNORE'] = ['netlify.toml']
freezer = Freezer(app)

# @freezer.register_generator
# def error_handlers():
#     yield "/404"

if __name__ == "__main__":
    # Update the index before we freeze
    make_index()
    freezer.freeze()
