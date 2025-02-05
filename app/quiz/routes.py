from flask import render_template, url_for, redirect, Blueprint, flash,session
from app import db
from flask_login  import login_required,current_user
from app.models import Question, User
from app.quiz.forms import CorrectOption

quiz = Blueprint('quiz', __name__)

@login_required
@quiz.route("/quiz",methods=['GET','POST'])
def quizques():
    
    if current_user.is_authenticated:
        if "current_question" not in session:
            session["current_question"] = 1
        if "score" not in session:
            session["score"] = 0
        session.modified=True

        # Get current question
        question = Question.query.filter_by(id=session['current_question']).first()

        if not question:
            if current_user.max_score<session['score']:
                current_user.max_score=session['score']
                db.session.commit()
            if current_user.max_score==0:
                current_user.category="Novice"
            elif current_user.max_score==5:
                current_user.category="Beginner"
            elif current_user.max_score==10:
                current_user.category="Intermediate"
            elif current_user.max_score==15:
                current_user.category="Expert"
            elif current_user.max_score==20:
                current_user.category="Superstar"
            else:
                current_user.category="Legend"
            return redirect(url_for("quiz.show_score"))

        # Initialize form and set choices dynamically
        form = CorrectOption()
        form.options.choices = [('A', question.option1),('B', question.option2),('C', question.option3),('D', question.option4)]

        # Handle form submission
        if form.validate_on_submit():
            selected_option = dict(form.options.choices)[form.options.data]  # Get text of selected answer
            if selected_option == question.correct_option:
                flash("Correct Answer!", 'success')
                session['score'] += 5  # Update session score
            else:
                flash("Wrong Answer!", 'danger')

            # Move to next question
            session['current_question'] += 1
            return redirect(url_for("quiz.quizques"))  # Reload next question

        return render_template('quiz.html', title='Quiz', question=question, form=form)
    flash("Please Log In/Register to continue!","warning")
    return redirect(url_for(endpoint="users.login"))

@login_required
@quiz.route("/final_score")
def show_score():
    final_score=session.get('score',0)
    session.pop("score", None)
    session.pop("current_question", None)
    maxm=current_user.max_score
    return render_template('fscore.html', title="Final Score",final_score=final_score,maxm=maxm)

@login_required
@quiz.route("/leaderboard")
def ldb():
    user_lst=User.query.all()
    user_lst=sorted(user_lst,key=lambda tup:tup.max_score,reverse=True)
    return render_template('leaderboard.html', title="Leaderboard",user_lst=user_lst)