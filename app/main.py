from app import app
from app import db
from core.blueprint import core
#from auth.blueprint import auth
#from importation.blueprint import imp

from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')


app.register_blueprint(core, url_prefix='/core')

#app.register_blueprint(auth, url_prefix='/auth')
#app.register_blueprint(imp, url_prefix='/imp')


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', port=80, debug=True, use_reloader=True)
