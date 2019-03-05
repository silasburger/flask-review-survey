from flask import Flask, session, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)


@app.route('/instructions')
def survey_start_view():
    """ view function that shows the survey title, instructions, and start button."""

    session['responses'] = []

    return render_template('start.html', survery_title=satisfaction_survey.title, survey_description=satisfaction_survey.instructions)


@app.route('/question/<int:question_num>')
def question_view(question_num):
    """ view funtion that shows the first question in the survey"""

    response = request.args['answer']

    responses = session['responses']

    render_template('question.html')
