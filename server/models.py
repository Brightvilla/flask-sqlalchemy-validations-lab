from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

CLICKBAIT_PHRASES = ("Won't Believe", "Secret", "Top", "Guess")
VALID_CATEGORIES = ("Fiction", "Non-Fiction")
PHONE_NUMBER_LENGTH = 10
MIN_CONTENT_LENGTH = 250
MAX_SUMMARY_LENGTH = 250


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name.")

        existing = db.session.query(Author).filter(
            Author.name == name, Author.id != self.id
        ).first()
        if existing:
            raise ValueError("Author name must be unique.")

        return name

    @validates("phone_number")
    def validate_phone_number(self, key, phone):
        if phone and (len(phone) != PHONE_NUMBER_LENGTH or not phone.isdigit()):
            raise ValueError(f"Phone number must be exactly {PHONE_NUMBER_LENGTH} digits.")
        return phone

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name!r})"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("title")
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post must have a title.")

        if not any(phrase in title for phrase in CLICKBAIT_PHRASES):
            raise ValueError("Title must contain a clickbait phrase.")

        return title

    @validates("content")
    def validate_content(self, key, content):
        if content and len(content) < MIN_CONTENT_LENGTH:
            raise ValueError(f"Post content must be at least {MIN_CONTENT_LENGTH} characters.")
        return content

    @validates("summary")
    def validate_summary(self, key, summary):
        if summary and len(summary) > MAX_SUMMARY_LENGTH:
            raise ValueError(f"Post summary must be at most {MAX_SUMMARY_LENGTH} characters.")
        return summary

    @validates("category")
    def validate_category(self, key, category):
        if category not in VALID_CATEGORIES:
            raise ValueError(f"Post category must be one of {VALID_CATEGORIES}.")
        return category

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title!r})"