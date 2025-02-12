from flask import render_template, url_for, redirect, Blueprint, flash,session
from app import db
from flask_login  import login_required,current_user
from app.models import Question, User
from app.quiz.forms import CorrectOption, OptCategory

quiz = Blueprint('quiz', __name__)

@login_required
@quiz.route("/category",methods=['GET','POST'])
def choose_category():
    if not current_user.is_authenticated:
        return redirect(url_for("users.login"))
    form=OptCategory()
    form.options.choices=["Current Affairs","Entertainment","Sports","Mixed Bag"]
    if form.validate_on_submit():
        session['category']=form.options.data
        print("Selected category from session:", session["category"])
        session.modified=True
        return redirect(url_for('quiz.quizques'))
    return render_template('q_category.html',title="Category",form=form)

@login_required
@quiz.route("/quiz",methods=['GET','POST'])
def quizques():
    if current_user.is_authenticated:
        if "category" not in session:
            print("No category selected.")
            flash("Please select a category first!", "warning")
            return redirect(url_for("quiz.choose_category"))
        if "question_list" not in session:
            #store id of those question belonging to current category 
            session["question_list"] = [q.id for q in Question.query.filter_by(category=session["category"]).all()]
            print("Questions:",Question.query.filter_by(category=session["category"]).all())
            session["current_question_index"] = 0  # Track progress
            session["score"] = 0
            session["correct_ans"]=""
            session.modified = True

        # If no questions exist for the selected category
        if not session["question_list"]:
            print("selected category has no questions.")
            session.pop("category")
            flash("No questions available in this category.", "danger")
            return redirect(url_for("quiz.choose_category"))

        #End quiz when all questions are answered
        if session["current_question_index"] >= len(session["question_list"]):
            print("All questions traversed.")
            return redirect(url_for("quiz.show_score"))

        # Get current question
        question_id = session["question_list"][session["current_question_index"]]
        question = Question.query.get(question_id)
        session['correct_answer']=question.correct_option
        print("Retrieved question",question)

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
                flash(f"Wrong Answer!\nCorrect Answer: {session['correct_answer']}", 'danger')

            # Move to next question
            session["current_question_index"] += 1
            session.modified = True

            return redirect(url_for("quiz.quizques"))  # Load next question

        return render_template('quiz.html', title='Quiz', question=question, form=form)
    
    flash("Please Log In/Register to continue!","warning")
    return redirect(url_for("users.login"))

@login_required
@quiz.route("/final_score")
def show_score():
    final_score = session.get('score', 0)

    # Update max score if the current score is higher
    if current_user.max_score < final_score:
        current_user.max_score = final_score
        db.session.commit()

    #Assign category
    score_categories = {0: "Novice", 5: "Beginner", 10: "Intermediate", 15: "Expert", 20: "Superstar", 25: "Legend"}
    current_user.category = score_categories.get(current_user.max_score)
    db.session.commit()

    # Remove session keys
    session.pop("score")
    session.pop("current_question_index")
    session.pop("question_list")
    session.pop("category")
    
    maxm = current_user.max_score
    return render_template('fscore.html', title="Final Score", final_score=final_score, maxm=maxm)


@login_required
@quiz.route("/leaderboard")
def ldb():
    user_lst=User.query.all()
    user_lst=sorted(user_lst,key=lambda tup:tup.max_score,reverse=True)
    return render_template('leaderboard.html', title="Leaderboard",user_lst=user_lst)