#!/usr/bin/env python3
"""Simple database initialization script"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'app'))

from database import SessionLocal, engine
from models.database_models import Base, User, Template, Tag, MetadataField
from auth import get_password_hash

def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

def create_default_admin():
    """Create default admin user."""
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print("ℹ️  Admin user already exists")
            return
        
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@noss.local",
            full_name="System Administrator",
            role="admin",
            hashed_password=get_password_hash("admin123"),
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        print("✅ Default admin user created (username: admin, password: admin123)")
        
    finally:
        db.close()

def create_default_templates():
    """Create default curriculum templates."""
    db = SessionLocal()
    try:
        # Check if templates already exist
        if db.query(Template).count() > 0:
            print("ℹ️  Templates already exist")
            return
        
        # Get admin user
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            print("❌ Admin user not found. Create admin user first.")
            return
        
        # Default templates
        templates = [
            {
                "name": "Course Outline Template",
                "description": "Standard template for creating course outlines",
                "template_type": "course",
                "content_template": "# {course_title}\\n\\n## Course Overview\\n{course_overview}",
                "created_by": admin.id
            },
            {
                "name": "Competency Unit Template", 
                "description": "Template for individual competency units",
                "template_type": "unit",
                "content_template": "# Competency Unit: {unit_code} - {unit_title}\\n\\n## Unit Overview\\n{unit_overview}",
                "created_by": admin.id
            }
        ]
        
        for template_data in templates:
            template = Template(**template_data)
            db.add(template)
        
        db.commit()
        print(f"✅ Created {len(templates)} default templates")
        
    finally:
        db.close()

def main():
    """Main initialization function."""
    print("🚀 Starting database initialization...")
    
    create_tables()
    create_default_admin()
    create_default_templates()
    
    print("✅ Database initialization completed!")

if __name__ == "__main__":
    main()
