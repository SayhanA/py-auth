from flask import Flask
from config import Config
from models import user_model
from controllers import user_controller
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Mongo and Mail in models
user_model.set_mongo(app)
CORS(app)

# Routes
app.add_url_rule('/register', view_func=user_controller.register_user, methods=['POST'])
app.add_url_rule('/login', view_func=user_controller.login_user, methods=['POST'])
app.add_url_rule('/verify/<token>', view_func=user_controller.verify_email, methods=['GET'], endpoint='verify_email')
app.add_url_rule('/resend-verification', 
                view_func=user_controller.resend_verification_email, 
                methods=['POST'])

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
