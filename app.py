from flask import Flask
from routes import login , push , pop, size, healthCheck
import controllers

app = Flask (__name__)

app.register_blueprint(login.routes_auth, url_prefix='/api/queue')
app.register_blueprint(push.routes_push, url_prefix='/api/queue')
app.register_blueprint(pop.routes_pop, url_prefix='/api/queue')
app.register_blueprint(size.routes_size, url_prefix='/api/queue')
app.register_blueprint(healthCheck.routes_health_check, url_prefix='/api/queue')


if __name__ == '__main__':
    app.run(debug=True)