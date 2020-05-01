from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config


blueprints = [
    # 'clover.suite:suite',
    # 'clover.interface:interface',
    # 'clover.environment:environment',
]


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    app.app_context().push()

    return app

db = SQLAlchemy()
app = create_app()
