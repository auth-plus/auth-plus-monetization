import os
from flask import Flask, request
from flask_wtf.csrf import CSRFProtect
from src.config.envvar import get_env

from src.core import Core


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config["SECRET_KEY"] = "TEST-MONETIZATION"
    csrf = CSRFProtect()
    csrf.init_app(app)
    app.config.from_mapping()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    @app.route("/health")
    def health():
        return "Ok"

    @app.route("/account", methods=["POST"])
    def create_account():
        request_data = request.get_json()
        print(request_data)
        external_id = request_data["external_id"]
        type = request_data["type"]
        core = Core()
        charge = core.account_create.create(external_id, type)
        return charge

    return app


if __name__ == "__main__":
    env = get_env()
    app = create_app()

    print(env["app"]["port"])
    app.run(debug=True, port=8081)
