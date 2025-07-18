from flask import Flask
from app.main.config.dev_config import Config
from init_db import db
from flask import send_from_directory
from auth import auth_bp
# from app.main.controllers.cart import api
from app.main.controllers import blueprint
from app.main.models import user, artworks, roles, orders, cart, order_items, wishlist, reviews, payments
from flask_cors import CORS
from flask_jwt_extended import JWTManager
jwt = JWTManager()
# manage.py or app/__init__.py
from app.main.controllers.enums import enum_bp



from init_db import mail, bcrypt
def create_app():
   
    app = Flask(__name__,  static_folder='static', static_url_path='/static')
    app.config.from_object(Config)
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True) 
    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(blueprint, url_prefix='/api')
    app.register_blueprint(auth_bp)
    app.register_blueprint(enum_bp, url_prefix='/api')
    # app.register_blueprint(api, url_prefix='/api')
   
    @app.route('/static/uploads/<path:filename>')
    def serve_uploads(filename):
        return send_from_directory('static/uploads', filename)

    return app

app = create_app()
print("ROUTES:")
for rule in app.url_map.iter_rules():
         print(rule)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)





