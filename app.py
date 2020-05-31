from flask import Flask, render_template, request
from main import create_abstract

# Create the application.
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/abstract',methods=['GET', 'POST'])
def abstract():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the user has entered
        try:
            keyword = request.form['keyword']
            method = request.form['subject']
            title, body = create_abstract(keyword,method)
            results = {'title':title, 'body':body, 'keywords':'keywords: ' + keyword}
        except IndexError:
            error_msg = "Unable to get keyword(s). Please make sure it's about physics/math/computer science/chemistry and try again."
            if error_msg not in errors:
                errors.append(error_msg)
    return render_template('abstract.html',errors=errors, results=results)

if __name__ == '__main__':
    app.debug=True
    app.run()
