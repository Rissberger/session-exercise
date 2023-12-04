from flask import Flask, request, redirect, render_template, url_for, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

# Key for session management
app.config['SECRET_KEY'] = 'secret'

debug = DebugToolbarExtension(app)
responses = []


@app.route('/initialize', methods=['POST'])
def initialize_survey():
    session["responses"] = []
    return redirect('/questions/0')

@app.route('/')
def show_start_page():
  
    return render_template("start.html", survey=survey)

@app.route('/start', methods=["POST"])
def start_survey():
    """Clear the session and redirect to the first question."""
    session["responses"] = []
    return redirect('/questions/0')

@app.route('/questions/<int:qid>')
def show_question(qid):
    """Show current survey question."""
    responses = session.get("responses", [])

    # Redirect to thank you page if survey is completed
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thankyou')

    # Redirect to correct question if trying to access questions out of order
    if qid != len(responses):
        flash(f"You're trying to access an invalid question: {qid}")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[qid]
    return render_template('question.html', question=question, qid=qid)

@app.route('/answer', methods=['POST'])
def handle_answer():
    # Extract the current list of responses from the session
    current_responses = session.get("responses", [])

    # Get the user's submitted answer
    answer = request.form['answer']

    # Append the new answer to the list of responses
    current_responses.append(answer)

    # Save the updated responses list back into the session
    session["responses"] = current_responses

    # Redirect to the next question or the thank you page
    if len(current_responses) < len(satisfaction_survey.questions):
        return redirect(f'/questions/{len(current_responses)}')
    else:
        return redirect('/thankyou')

@app.route('/thankyou')
def thank_you():
    """Show completion page after survey is finished."""
    return render_template('thankyou.html')


