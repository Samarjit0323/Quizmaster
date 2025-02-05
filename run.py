from app import create_app,db

quiz_app=create_app() #creating the app instance

with quiz_app.app_context():
    db.create_all() #creating database tables

if __name__ == '__main__':
    quiz_app.run(debug=True) #running the app in debug mode