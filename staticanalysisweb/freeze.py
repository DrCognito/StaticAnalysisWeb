from flask_frozen import Freezer
from staticanalysisweb.app import app
from staticanalysisweb.local import make_index
from staticanalysisweb import CONFIG

# Stop frozen flask deleting netlify.toml
app.config['FREEZER_DESTINATION_IGNORE'] = ['netlify.toml']
app.config['FREEZER_DESTINATION'] = CONFIG['FREEZER_DESTINATION']
freezer = Freezer(app)

# @freezer.register_generator
# def error_handlers():
#     yield "/404"

if __name__ == "__main__":
    # Update the index before we freeze
    make_index()
    freezer.freeze()
