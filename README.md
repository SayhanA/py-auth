# Thinkers Flask Server Task Assessment

This is a **Flask-based backend** for the Thinkers Flutter Developer Task App.  
It handles **user registration, login, email verification, password reset,** and other authentication-related features.

---

## 🚀 Live Deployment
**Live link:** *https://py-auth.onrender.com*

---

## 📂 Project Structure
    ├── app.py # Main Flask app entry point
├── config.py # Configuration file (loads environment variables)
├── controllers/ # Controller functions (business logic)
│ └── user_controller.py
├── models/ # Database models
│ └── user_model.py
├── views/ # HTML templates for email
│ └── verification_email.html
├── requirements.txt # Python dependencies
└── README.md


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

git clone https://github.com/SayhanA/py-auth.git
cd your-repo

### 2️⃣ Create a virtual environment
python3 -m venv venv
source venv/bin/activate

### 3️⃣ Install dependencies
pip install -r requirements.txt

### 4️⃣ Create a .env file
MONGO_URI=<your-mongodb-uri>
MAIL_SERVER=<your-mail-server>
MAIL_PORT=<mail-port>
MAIL_USE_TLS=<True-or-False>
MAIL_USERNAME=<your-email-username>
MAIL_PASSWORD=<your-email-password>
MAIL_DEFAULT_SENDER=<default-sender-email>

▶️ Run the Server
python3 app.py

### Make sure change app.py file
comment this:

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


and then Uncomment this:
# if __name__ == '__main__':
#     app.run(debug=True)


### 📌 API Endpoints
| Method | Endpoint               | Description                                   |
| ------ | ---------------------- | --------------------------------------------- |
| POST   | `/register`            | Register a new user & send verification email |
| POST   | `/login`               | Login user                                    |
| GET    | `/verify/<token>`      | Verify email using token                      |
| POST   | `/resend-verification` | Resend email verification link                |
| GET    | `/check-verification`  | Check if email is verified                    |
| POST   | `/forgot-password`     | Send password reset email                     |
| POST   | `/verify-reset-code`   | Verify reset code                             |
| POST   | `/reset-password`      | Reset user password                           |


🛠 Technologies Used
Flask – Web framework

Flask-Mail – Email sending

Flask-CORS – Handle cross-origin requests

MongoDB – Database

dotenv – Environment variable management

📄 License
This project is for assessment purposes only.

---

Do you want me to also add **example request & response JSON** for each endpoint in this README so testers can use it right away in Postman? That would make it ready for immediate API testing.
