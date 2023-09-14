from flask import Flask, send_file
from flask_msearch import Search
from application.api import *
from application.security import *
from application.model import *
from application.config import *
from application.cache import *
from flask_cors import CORS

from application import workers
from application import tasks
celery = None
def create_app():
    app = Flask (__name__, template_folder="templates", static_folder = "static")
    app.config.from_object(LocalDevelopmentConfig)
    CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True}})
    init_db(app)
    Search().init_app(app)
    init_security(app)
    add_resources()
    init_api(app)
    init_cache(app)
    celery = workers.celery
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.Task = workers.ContextTask
    
    app.app_context().push()
    return app, celery

app, celery = create_app()

@app.route('/favicon.ico')
def favicon():
    return send_file('favicon.ico')

@app.route('/api/login', methods=['OPTIONS'])
def handle_options():
    response = app.make_default_options_response()
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/api/register', methods=['OPTIONS'])
def handle_options_register():
    response = app.make_default_options_response()
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

from flask_login import logout_user

@app.route('/api/logout', methods=['GET'])
def logout():
    logout_user()
    return { "message":'Logged out successfully'}, 200

@app.route('/api/isloggedin', methods=['GET'])
def is_logged_in():
    if current_user.is_authenticated:
        user_data = {
            "user_id": current_user.id,
            "email": current_user.email,
            "role": current_user.roles[0].name  # Assuming a user has only one role
            # Add other user data fields as needed
        }
        return {"isloggedin": True, "user_data": user_data}
    else:
        return {"isloggedin": False}
    
@app.route("/api/export/<venue_id>", methods=["GET"])
@auth_required('session')
def export_csv(venue_id):
    job = tasks.export_venue_summary.delay(venue_id, current_user.id)
    return str(job), 200

# from application.tasks import *

# @app.route('/testing/<int:user_id>', methods=['GET'])
# def testing(user_id):
#     data = data_for_daily_reminder(user_id)
#     return(data)
#     # generate_content_for_venue_export_and_send_mail(data, "himadri@him.com")
#     return str(True)

@app.errorhandler(404)
def pagenotfound():
    return "Page not found. Please return to the homepage."

@app.errorhandler(403)
def not_allowed():
    return "You are not allowed to access this page. Please return to the homepage."

from application.controllers import *

if __name__ == '__main__':
    app.run(debug=True)

