from flask import render_template, Blueprint
main=Blueprint('main',__name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html',title='Home')

@main.route('/about')
def about():
    return render_template('about.html',title='About')

@main.route('/contact')
def contact():
    return render_template('contact.html',title='Contact')