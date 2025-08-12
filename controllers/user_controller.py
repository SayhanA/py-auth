from flask import request, jsonify, url_for
from models.user_model import create_user, find_user_by_email, verify_user, verify_user_by_token, mail, generate_reset_code, find_user_by_reset_code, clear_reset_code, update_password
from flask_mail import Message
from flask import render_template

def register_user():
    data = request.json
    if not data or not all(k in data for k in ("name", "email", "password")):
        return jsonify({"error": "Name, email, and password are required"}), 400

    if find_user_by_email(data["email"]):
        return jsonify({"error": "User already exists"}), 409

    verification_token = create_user(data["name"], data["email"], data["password"])

    # Send verification email with HTML template
    verification_url = url_for('verify_email', token=verification_token, _external=True)

    msg = Message(
        "Verify Your Email - Thinkers Flutter Developer Task App",
        recipients=[data["email"]]
    )

    msg.html = render_template("verification_email.html", verification_url=verification_url)

    # Plain text fallback
    msg.body = f"""
    Welcome to Thinkers Flutter Developer Task App!
    
    Please verify your email by clicking the following link:
    {verification_url}
    
    If you didn't request this, please ignore this email. The link will expire in 24 hours.
    
    Thinkers Flutter Developer Team
    https://yourwebsite.com
    """

    try:
        mail.send(msg)
        return jsonify({"message": "User registered successfully! Please check your email to verify your account."}), 201
    except Exception as e:
        # Log the error and inform the user
        print(f"Failed to send verification email: {str(e)}")
        return jsonify({"message": "User registered successfully! We couldn't send the verification email. Please contact support."}), 201
    
def login_user():
    data = request.json
    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"error": "Email and password are required"}), 400

    user = verify_user(data["email"], data["password"])
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    if not user.get("isVerified", False):
        return jsonify({"error": "User is not verified. Please check your email."}), 403

    return jsonify({
        "message": "Login successful",
        "user": {
            "name": user["name"],
            "email": user["email"],
            "isVerified": user.get("isVerified", False)
        }
    }), 200

def verify_email(token):
    if verify_user_by_token(token):
        return render_template('verify_success.html'), 200

    return render_template('verify_failed.html'), 400
    return jsonify({"error": "Invalid or expired verification token"}), 400

def resend_verification_email():
    data = request.json
    if not data or "email" not in data:
        return jsonify({"error": "Email is required"}), 400

    user = find_user_by_email(data["email"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.get("isVerified", False):
        return jsonify({"error": "Email is already verified"}), 400

    # Generate new token and send email
    verification_token (data["email"])
    verification_url = url_for('verify_email', token=verification_token, _external=True)
    
    msg = Message(
        "Verify Your Email - Thinkers Flutter Developer Task App",
        recipients=[data["email"]]
    )
    
    msg.html = render_template('resendVerification_email.html', verification_url=verification_url, message_text="Here's your new verification link:")
    
    msg.body = f"""
    Verify your email by clicking this link:
    {verification_url}
    
    Thinkers Flutter Developer Team
    """
    
    try:
        mail.send(msg)
        return jsonify({"message": "Verification email resent successfully"}), 200
    except Exception as e:
        print(f"Failed to resend verification email: {str(e)}")
        return jsonify({"error": "Failed to resend verification email"}), 500
         
def check_verification_status():
    email = request.args.get('email')
    
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400

    user = find_user_by_email(email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "email": user["email"],
        "isVerified": user.get("isVerified", False),
        "message": "User is verified" if user.get("isVerified", False) else "User is not verified"
    }), 200
    
def forgot_password():
    data = request.json
    if not data or "email" not in data:
        return jsonify({"error": "Email is required"}), 400

    user = find_user_by_email(data["email"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    otp = generate_reset_code(data["email"])
    if not otp:
        return jsonify({"error": "Failed to generate OTP"}), 500

    msg = Message(
        "Your Password Reset Code - Thinkers App",
        recipients=[data["email"]]
    )
    msg.html = f"""
    <p>Your password reset code is:</p>
    <h2 style="color:#6C63FF;">{otp}</h2>
    <p>This code will expire in 10 minutes.</p>
    """
    msg.body = f"Your password reset code is: {otp} (expires in 10 minutes)"

    try:
        mail.send(msg)
        return jsonify({"message": "Password reset code sent"}), 200
    except Exception as e:
        print(f"Failed to send reset email: {str(e)}")
        return jsonify({"error": "Failed to send reset code"}), 500

    data = request.json
    if not data or "new_password" not in data:
        return jsonify({"error": "New password is required"}), 400

    user = find_user_by_reset_token(token)
    if not user:
        return jsonify({"error": "Invalid or expired reset token"}), 400

    update_password(user["email"], data["new_password"])
    return jsonify({"message": "Password updated successfully"}), 200


def verify_reset_code():
    data = request.json
    if not data or "code" not in data:
        return jsonify({"error": "Code is required"}), 400

    user = find_user_by_reset_code(data["code"])
    if not user:
        return jsonify({"error": "Invalid or expired code"}), 400

    return jsonify({"message": "Code verified", "email": user["email"]}), 200


def reset_password():
    data = request.json
    if not data or "code" not in data or "new_password" not in data:
        return jsonify({"error": "Code and new password are required"}), 400

    user = find_user_by_reset_code(data["code"])
    if not user:
        return jsonify({"error": "Invalid or expired code"}), 400

    update_password(user["email"], data["new_password"])
    clear_reset_code(user["email"])
    return jsonify({"message": "Password updated successfully"}), 200
