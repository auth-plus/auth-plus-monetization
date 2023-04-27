from flask import Flask
from flask_wtf.csrf import CSRFProtect

from src.config.envvar import get_env
from src.core import Core


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    csrf = CSRFProtect()
    csrf.init_app(app)
    app.config.from_mapping()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route("/health")
    def health():
        return "Ok"

    @app.route("/ledger/receive_credit")
    def receive_credit():
        core = Core()
        charge = core.pre_paid.receive_credit.receive_credit()
        return charge

    return app


if __name__ == "__main__":
    env = get_env()
    app = create_app()
    print(env["app"]["port"])
    app.run(debug=True, port=8081)
