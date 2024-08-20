import spacy
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

nlp = spacy.load("en_core_web_sm")

tasks = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def get_bot_response():
    user_input = request.json.get('message')
    context = session.get('context', {})

    response, new_context = process_input(user_input, context)
    session['context'] = new_context

    return {'response': response}

def process_input(user_input, context):
    doc = nlp(user_input.lower())
    
    if 'add' in [token.lemma_ for token in doc]:
        if 'adding_task' in context:
            task_name = user_input
            tasks.append(task_name)
            response = f"Task '{task_name}' has been added."
            context.pop('adding_task')
        else:
            response = "What task would you like to add?"
            context['adding_task'] = True
    elif 'change' in [token.lemma_ for token in doc] and 'name' in [token.lemma_ for token in doc]:
        response = "Which task would you like to rename, and what should the new name be?"
    elif 'view' in [token.lemma_ for token in doc] and 'task' in [token.lemma_ for token in doc]:
        if not tasks:
            response = "You have no tasks."
        else:
            response = "Your tasks are:\n" + '\n'.join(tasks)
    else:
        response = "I'm here to help with your productivity. What can I do for you?"

    return response, context

if __name__ == '__main__':
    app.run(debug=True)
