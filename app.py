from flask import Flask
from routes import auth , push , pop, size, healthCheck
import controllers

app = Flask (__name__)

PREFIX = "/api/queue"

app.register_blueprint(auth.routes_auth, url_prefix=PREFIX)
app.register_blueprint(push.routes_push, url_prefix=PREFIX)
app.register_blueprint(pop.routes_pop, url_prefix=PREFIX)
app.register_blueprint(size.routes_size, url_prefix=PREFIX)
app.register_blueprint(healthCheck.routes_health_check, url_prefix=PREFIX)


if __name__ == '__main__':
    app.run(debug=True)