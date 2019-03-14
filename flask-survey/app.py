from flask import Flask, session, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)


@app.route('/')
def choose_survey_view():
    """view function that shows a form to select which survey to take."""
    return render_template('choose-survey.html', surveys=surveys)


@app.route('/', methods=["POST"])
def pick_survey():
    """we choose the survey based on the response and add it to the session."""
    survey_key = request.form.get('survey')
    survey = surveys[survey_key]
    session['CURRENT_SURVEY_KEY'] = survey_key
    return render_template('start.html', survey_title=survey.title, survey_instructions=survey.instructions)


@app.route('/questions/<int:question_num>', methods=["POST"])
def question_view(question_num):
    """view funtion that shows the first question in the survey"""
    survey_key = session.get('CURRENT_SURVEY_KEY')
    survey = surveys[survey_key]
    if question_num > 0:
        question_response = request.form['question_response']
        responses = session['responses']
        responses.append(question_response)
        session['responses'] = responses
    else:
        session["responses"] = []
    
    if question_num >= len(survey.questions):
        return render_template('thank.html', survey_title=survey.title)

    choices = survey.questions[question_num].choices
    question = survey.questions[question_num].question

    return render_template('question.html', question=question, choices=choices, question_num=question_num)
