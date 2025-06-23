from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Author name is required')
        elif db.session.query(Author).filter_by(name=name).first():
            raise ValueError('Author name must be unique')
        return name
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number.isdigit():
            raise ValueError('Phone number is required')
        elif len(phone_number) != 10:
            raise ValueError('Phone number must be 10 digits')
        return phone_number
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("content")
    def validate_post(self, key, content):
        if not content or len(content) <250 :
            raise ValueError('Post is required')
        return content
    @validates("category")
    def validate_category(self, key, category):
        if not category or category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category is required')
        return category
    @validates("summary")
    def validate_summary(self, key, summary):
        if not summary or len(summary) > 250:
            raise ValueError('Summary is required')
        return summary
    @validates("title")
    def validate_title(self, key, title):
        if not title :
            raise ValueError('Title is required')
        clickbait=['Won\'t Believe', 'Secret', 'Top', 'Guess']
        if not any(substring in title for substring in clickbait):
            raise ValueError('Title must contain one of the following: "Won\'t Believe", "Secret", "Top", "Guess"')
        return title
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'