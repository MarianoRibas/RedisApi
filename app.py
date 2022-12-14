from flask import Flask
from apis import auth, count, push, pop, healthCheck


def create_app():
    app = Flask (__name__)

    with app.app_context():      
        URL_PREFIX = "/api/queue"

        app.register_blueprint(auth.routes_auth, url_prefix=URL_PREFIX)
        app.register_blueprint(push.routes_push, url_prefix=URL_PREFIX)
        app.register_blueprint(pop.routes_pop, url_prefix=URL_PREFIX)
        app.register_blueprint(count.routes_count, url_prefix=URL_PREFIX)
        app.register_blueprint(healthCheck.routes_health_check, url_prefix=URL_PREFIX)
        if __name__ == '__main__':
            app.run(debug=True)

        return app