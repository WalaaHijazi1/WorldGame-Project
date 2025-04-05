"""
This file’s sole purpose is to serve the user’s score currently in the scores.txt file over HTTP with
HTML. This will be done by using python’s flask library.

Methods
1. score_server - This function will serve the score. It will read the score from the scores file
and will return an HTML that will be as follows:

<html>
<head>
<title>Scores Game</title>
</head>
<body>
<h1>The score is <div id="score">{SCORE}</div></h1>
</body>
</html>

If the function will have a problem showing the result of reading the error it will return the
following:
<html>
<head>
<title>Scores Game</title>
</head>
<body>
<body>
<h1><div id="score" style="color:red">{ERROR}</div></h1>
</body>
</html>
"""

from flask import Flask, render_template
import os


app = Flask(__name__)


def read_score():

    try:

        script_path = os.path.dirname(os.path.abspath(__file__))
        working_file = os.path.join(script_path,'scores_file.txt')

        print(f"This is the file: {working_file}")
        print(f"File type is: {type(os.path.abspath(working_file))}")

        with open(working_file, 'r') as file:
            # Read the file content once and store it in a variable.
            # Use this variable for both validation and returning the score.
            
            content = file.read().strip()  # Read once and store
            curr_score = int(content)      # Validate it's an integer

            print(curr_score)
            print(f"type of curr score: {type(curr_score)}")

            return content                 # Return the original string

    except Exception as e:
        return f"Error: {e}"
        


@app.route('/')
def score_server():
    SCORE = read_score()

    if 'Error' in SCORE:
                html_content = f"""
        <html>
        <head>
            <title>Scores Game</title>
        </head>
        <body>
        <body>
            <h1><div id="score" style="color:red">{SCORE}</div></h1>
        </body>
        </html>
        """
    else:
         html_content = f"""
        <html>
        <head>
            <title>Scores Game</title>
        </head>
        <body>
            <h1>The score is <div id="score">{SCORE}</div></h1>
        </body>
        </html>
        """
    return html_content
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8777, debug=True)
