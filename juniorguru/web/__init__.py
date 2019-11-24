import pickle
from pathlib import Path
from datetime import datetime

import arrow
from flask import Flask, render_template


app = Flask(__name__)
app.config['DATA_DIR'] = Path(app.root_path) / '..' / 'data'


@app.route('/')
def index():
    jobs_data_path = app.config['DATA_DIR'].joinpath('jobs.pickle')
    jobs = pickle.loads(jobs_data_path.read_bytes())

    companies_count = len(set([job['company_link'] for job in jobs]))
    since = (datetime.now() - datetime(2019, 10, 10))

    return render_template('index.html',
                           jobs_count=len(jobs),
                           companies_count=companies_count,
                           since=since)


@app.route('/learn/')
def learn():
    return render_template('learn.html', year=arrow.utcnow().year)


@app.route('/practice/')
def practice():
    return render_template('practice.html')


@app.route('/jobs/')
def jobs():
    jobs_data_path = app.config['DATA_DIR'].joinpath('jobs.pickle')
    jobs = pickle.loads(jobs_data_path.read_bytes())
    return render_template('jobs.html', jobs=jobs)


@app.route('/privacy/')
def privacy():
    return render_template('privacy.html')


@app.context_processor
def inject_updated_at():
    return dict(updated_at=arrow.utcnow())


from . import template_filters  # noqa