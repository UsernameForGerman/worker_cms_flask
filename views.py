import datetime as dt
import flask

import app
import db


@app.app.route('/ping')
def ping():
    return "pong"


@app.app.route('/')
def main():
    return flask.render_template('index.html')


@app.app.route('/authors', methods=['GET'])
def authors():
    authors = db.get_authors()
    return flask.render_template('authors.html', authors=authors)


@app.app.route('/authors/<int:id>', methods=['GET'])
def authors_id(id):
    author_info = db.get_author_by_id(id=id)
    return flask.render_template('author.html', **author_info)


@app.app.route('/authors/create', methods=['GET', 'POST'])
def authors_create():
    import models

    if flask.request.method == 'GET':
        countries = db.get_countries()
        works = db.get_works()
        return flask.render_template('authors_add.html', countries=countries, works=works)
    input = dict(**flask.request.form)
    if dt.datetime.fromisoformat(input['birth_date']) > dt.datetime.now():
        raise app.exceptions.BadRequest("Невалидная дата")
    death = input.pop('death', None)
    countries = flask.request.form.getlist('countries')
    works = flask.request.form.getlist('works')
    input.pop('countries', None)
    input.pop('works', None)

    author = models.Author(
        id=db.generate_new_id_for_model(models.Author),
        **input
    )
    if death:
        if dt.datetime.fromisoformat(input['birth_date']) >= dt.datetime.fromisoformat(death):
            raise app.exceptions.BadRequest("Невалидная дата")
        death = models.Death(
            id=author.id,
            death=death
        )
    db.insert_author(author, death, countries, works)
    return flask.redirect('/authors')


@app.app.route('/works', methods=['GET'])
def works():
    works = db.get_works()
    return flask.render_template('works.html', works=works)


@app.app.route('/works/<int:id>', methods=['GET'])
def works_id(id):
    work = db.get_work_by_id(id)
    return flask.render_template('work.html', **work)


@app.app.route('/works/create', methods=['GET', 'POST'])
def works_create():
    import models

    if flask.request.method == 'GET':
        countries = db.get_countries()
        authors = db.get_authors()
        types = db.get_types()
        return flask.render_template('works_add.html', countries=countries, authors=authors, types=types)

    input = dict(**flask.request.form)
    countries = flask.request.form.getlist('countries')
    authors = flask.request.form.getlist('authors')
    input.pop('countries', None)
    input.pop('authors', None)
    if dt.datetime.fromisoformat(input['release_date']) > dt.datetime.now():
        raise app.exceptions.BadRequest("Не валидная дата")
    work = models.Work(
        id=db.generate_new_id_for_model(models.Work),
        **input
    )
    db.insert_work(work, countries, authors)
    return flask.redirect('/works')
