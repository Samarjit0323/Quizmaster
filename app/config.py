import os
class Config:
    SECRET_KEY=os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI="sqlite:///instance/site.db"
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get("EMAIL_USER")
    MAIL_PASSWORD=os.environ.get("EMAIL_PASS")

    from app import db
    SESSION_TYPE="sqlalchemy"
    SESSION_SQLALCHEMY=db
    SESSION_PERMANENT=False
    #Non-permanent session: A cookie is stored in the browser and is deleted 
    # when the browser or tab is closed (no expiry). 
    # Also known as a session cookie or non-persistent cookie