from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)  # Handles "required" & "no duplicates"
    phone_number = db.Column(db.String, nullable=False)       # Added nullable=False for safety
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @db.validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Name cannot be blank")
    
        name = name.strip()
        
        # Check for an existing author with the same name
        # If updating an existing record, exclude the current author's own ID
        query = Author.query.filter(Author.name == name)
        if self.id is not None:  # When updating an existing record
            query = query.filter(Author.id != self.id)
        
        if query.first():
            raise ValueError("Name must be unique")
    
        return name

    @db.validates('phone_number')
    def validate_phone(self, key, phone):
        # Ensure phone is not None before calling .isdigit()
        if not phone or not phone.isdigit() or len(phone) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)   # Should be required for min-length check
    category = db.Column(db.String, nullable=False)  # Should be required
    summary = db.Column(db.String, nullable=False)   # FIXED: Added nullable=False
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @db.validates('title')
    def validate_title(self, key, title):
        keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in title for keyword in keywords):
            raise ValueError("Title must contain at least one of: Won't Believe, Secret, Top, or Guess.")
        return title

    @db.validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        return content

    @db.validates('category')
    def validate_category(self, key, category):
        # FIXED: Correct logic - check if category is exactly "Fiction" or "Non-Fiction"
        allowed_categories = ["Fiction", "Non-Fiction"]
        if category not in allowed_categories:
            raise ValueError(f"Category must be exactly one of: {', '.join(allowed_categories)}.")
        return category

    @db.validates('summary')
    def validate_summary(self, key, summary):
        # FIXED: Correct error message
        if len(summary) > 250:
            raise ValueError("Summary must be 250 characters or fewer (maximum length).")
        return summary

    def __repr__(self):
        # FIXED: Added commas between attributes for clarity
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'