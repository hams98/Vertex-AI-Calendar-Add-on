import requests
from flask import Flask, request, redirect, jsonify, session

app = Flask(__name__)
app.secret_key = '12345'

# Replace these with your actual client ID and client secret
CLIENT_ID = 'sRrui5W2OsMy7Gq0h4'
CLIENT_SECRET = '(HOk3OYv*L&%gxwn10T4vkK665Epg&(('
REDIRECT_URI = 'http://localhost:5000/callback'  # This should match the redirect URI registered with TickTick

# TickTick endpoints
AUTHORIZE_URL = 'https://ticktick.com/oauth/authorize'
TOKEN_URL = 'https://ticktick.com/oauth/token'
TASKS_URL = 'https://api.ticktick.com/api/v2/task'

@app.route('/')
def home():
    # Redirect the user to the TickTick authorization URL
    authorize_url = f"{AUTHORIZE_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
    return redirect(authorize_url)

@app.route('/callback')
def callback():
    # Extract the authorization code from the callback URL
    code = request.args.get('code')

    # Exchange the authorization code for an access token
    token_response = requests.post(TOKEN_URL, data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
        'code': code
    })

    if token_response.status_code == 200:
        # Parse the access token from the response
        token_data = token_response.json()
        session['access_token'] = token_data.get('access_token')
        return redirect('/create_task')
    else:
        return jsonify({'error': 'Failed to obtain access token'}), token_response.status_code
    
@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        # Get task details from the form
        title = request.form.get('title')
        content = request.form.get('content')
        due_date = request.form.get('due_date')
        
        # Get the access token from session
        access_token = session.get('access_token')

        if not access_token:
            return jsonify({'error': 'Access token missing'}), 401

        # Create the task data payload
        task_data = {
            'title': title,
            'content': content,
            'dueDate': due_date
        }

        # Set up headers with the access token
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Send POST request to create task
        response = requests.post(TASKS_URL, json=task_data, headers=headers)

        if response.status_code == 200 or response.status_code == 201:
            return jsonify({'message': 'Task created successfully', 'task': response.json()})
        else:
            return jsonify({'error': 'Failed to create task'}), response.status_code
    return '''
    <form method="post">
        Title: <input type="text" name="title"><br>
        Content: <input type="text" name="content"><br>
        Due Date: <input type="text" name="due_date"><br>
        <input type="submit" value="Create Task">
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=True)

