from datetime import datetime

from flask import jsonify, request

from app.models.petplanner import db, Article
from app.models.role import Role


def create_article(current_user):
    user_role = Role(current_user.role)

    if user_role != Role.CENTER:
        return jsonify({"message": "You are not authorized to perform this action"}), 403

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    try:
        new_article = Article(
            author_id=current_user.id,
            title=title,
            content=content
        )
        db.session.add(new_article)
        db.session.commit()
        return jsonify({"message": "Article created successfully ", "data": new_article.to_json()})

    except Exception as e:
        return jsonify({"message": str(e)}), 400

def get_all_articles():
    try:
        articles = db.session.query(Article).all()
        return jsonify({"message": "List of all articles", "data": [article.to_json() for article in articles]}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

def get_my_articles(current_user):
    try:
        articles = db.session.query(Article).filter_by(author_id=current_user.id).all()
        return jsonify({"message": "List of my articles", "data": [article.to_json() for article in articles]}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

def get_article(article_id):
    try:
        article = Article.query.get(article_id)
        if not article:
            return jsonify({"message": "Article not found"}), 404

        return jsonify({"message": "Article found successfully", "data": article.to_json()})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

def update_article(current_user, article_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    try:
        article = Article.query.filter_by(author_id=current_user.id,id=article_id).first()
        if not article:
            return jsonify({"message": "Article not found"}), 404
        article.title = title
        article.content = content
        article.updated_at = datetime.now()
        db.session.commit()
        return jsonify({"message": "Article updated successfully", "data": article.to_json()})

    except Exception as e:
        return jsonify({"message": str(e)}), 400

def delete_article(current_user, article_id):
    user_role = Role(current_user.role)
    if user_role != Role.CENTER:
        return jsonify({"message": "You are not authorized to perform this action"}), 403

    try:
        article = Article.query.filter_by(author_id=current_user.id,id=article_id).first()

        if not article:
            return jsonify({"message": "Article not found"}), 404

        db.session.delete(article)
        db.session.commit()
        return jsonify({"message": "Article deleted successfully"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400