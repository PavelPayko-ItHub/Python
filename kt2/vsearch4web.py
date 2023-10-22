from flask import Flask
from flask import render_template
from flask import request
from flask import escape
from vsearch import search4letters

app = Flask(__name__)
def log_request(req: 'flask_request', res: str)->None:
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase, letters))
    with open('vsearch.log', 'a') as log:
        print(phrase,letters, results, req.remote_addr,req.user_agent,file=log, sep='|')
@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results,)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')

@app.route('/viewlog')
def view_the_log() -> 'html':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Phrase', 'Letters','Results','Remote_addr', 'User_agent', )
    return render_template('viewlog.html', the_title='View Log', the_row_titles=titles,the_data=contents,)

if __name__ == '__main__':
    app.run(debug=True)