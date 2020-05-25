from flask import Flask, render_template, request
from main import create_abstract

# Create the application.
app = Flask(__name__)

# Global variables




@app.route('/',methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the user has entered
        try:
            keyword = request.form['keyword']
            if request.form['action'] == 'Markov Chain':
                title, body = create_abstract(keyword)
                results = {'title':title, 'body':body, 'keywords':'keywords: ' + keyword}
            else: 
                error_msg = "Method not yet implemented."
                if error_msg not in errors:
                    errors.append(error_msg)
        except IndexError:
            error_msg = "Unable to get keyword(s). Please make sure it's about physics/math/computer science/chemistry and try again."
            if error_msg not in errors:
                errors.append(error_msg)
    return render_template('index.html',errors=errors, results=results)


if __name__ == '__main__':
    app.debug=True
    app.run()
