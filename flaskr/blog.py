from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.src.run_search_by_keyword import run_sbk

bp = Blueprint('blog', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        error = None

        if not keyword:
            error = 'keyword is required'

        if error is not None:
            flash(error)
        else:
            # Google検索
            rs = run_sbk(keyword, g.user['id'])

            db = get_db()
            db.executemany(
                'INSERT INTO company (author_id, cnt, keyword, rank, title, url) VALUES (?,?,?,?,?,?)',
                rs
            )
            db.commit()
            return redirect(url_for('blog.index'))

    db = get_db()
    company_list = db.execute(
        'SELECT created, keyword, rank, title, url'
        ' FROM company'
        ' ORDER BY id'
    )
    
    return render_template('blog/index.html', posts=company_list)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if not title:
            error = 'Title is required'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?,?,?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    
    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if not title:
            error = 'Title is required'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/<int:id>/detail',methods=('GET', 'POST'))
@login_required
def detail(id):
    post = get_post(id,False)
    
    # コメントの読み込み
    db = get_db()
    comments = db.execute(
        'SELECT c.id, post_id, comment, created, author_id, u.username'
        ' FROM comment c JOIN user u ON c.author_id = u.id'
        ' WHERE c.post_id = ?'
        ' ORDER BY created DESC',
        (id,)
    ).fetchall()
    
    # コメント投稿
    if request.method == 'POST':
        comment = request.form['comment']
        error = None
        
        if not comment:
            error = 'Comment is required'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO comment (comment, post_id, author_id)'
                ' VALUES (?,?,?)',
                (comment, id, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.detail', id=id))

    return render_template('blog/detail.html', post=post, comments=comments)


