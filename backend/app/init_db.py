# Database initialization script
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models.database_models import Base, User, Template, Tag, MetadataField
from .auth import get_password_hash
from . import schemas

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
                "content_template": """
# {course_title}

## Course Overview
{course_overview}

## Learning Outcomes
{learning_outcomes}

## Course Structure
{course_structure}

## Assessment Methods
{assessment_methods}

## Resources
{resources}
""",
                "created_by": admin.id
            },
            {
                "name": "Competency Unit Template",
                "description": "Template for individual competency units",
                "template_type": "unit",
                "content_template": """
# Competency Unit: {unit_code} - {unit_title}

## Unit Overview
{unit_overview}

## Elements and Performance Criteria
{elements_criteria}

## Required Skills and Knowledge
{skills_knowledge}

## Assessment Requirements
{assessment_requirements}
""",
                "created_by": admin.id
            },
            {
                "name": "Lesson Plan Template",
                "description": "Standard lesson plan structure",
                "template_type": "lesson",
                "content_template": """
# Lesson Plan: {lesson_title}

## Lesson Objectives
{lesson_objectives}

## Duration
{lesson_duration}

## Resources Required
{resources_required}

## Lesson Structure
### Introduction ({intro_duration})
{introduction_content}

### Main Activity ({main_duration})
{main_activity_content}

### Conclusion ({conclusion_duration})
{conclusion_content}

## Assessment
{assessment_method}
""",
                "created_by": admin.id
            },
            {
                "name": "Assessment Template",
                "description": "Template for creating assessments",
                "template_type": "assessment",
                "content_template": """
# Assessment: {assessment_title}

## Assessment Type
{assessment_type}

## Learning Outcomes Assessed
{learning_outcomes}

## Instructions
{instructions}

## Marking Criteria
{marking_criteria}

## Resources Allowed
{resources_allowed}

## Time Allocation
{time_allocation}
""",
                "created_by": admin.id
            }
        ]
        
        for template_data in templates:
            template = Template(**template_data)
            db.add(template)
        
        db.commit()
        print("✅ Default templates created successfully")
        
    finally:
        db.close()

def create_default_tags():
    """Create default tags for categorization."""
    db = SessionLocal()
    try:
        # Check if tags already exist
        if db.query(Tag).count() > 0:
            print("ℹ️  Tags already exist")
            return
        
        # Default tags
        tags = [
            {"name": "TVET", "color": "#3B82F6", "description": "Technical and Vocational Education and Training"},
            {"name": "NOSS", "color": "#10B981", "description": "National Occupational Skills Standard"},
            {"name": "Competency", "color": "#8B5CF6", "description": "Competency-based content"},
            {"name": "Assessment", "color": "#F59E0B", "description": "Assessment related content"},
            {"name": "Theory", "color": "#EF4444", "description": "Theoretical content"},
            {"name": "Practical", "color": "#06B6D4", "description": "Practical/hands-on content"},
            {"name": "Safety", "color": "#DC2626", "description": "Safety and compliance related"},
            {"name": "Industry", "color": "#059669", "description": "Industry-specific content"}
        ]
        
        for tag_data in tags:
            tag = Tag(**tag_data)
            db.add(tag)
        
        db.commit()
        print("✅ Default tags created successfully")
        
    finally:
        db.close()

def create_default_metadata_fields():
    """Create default metadata fields."""
    db = SessionLocal()
    try:
        # Check if metadata fields already exist
        if db.query(MetadataField).count() > 0:
            print("ℹ️  Metadata fields already exist")
            return
        
        # Default metadata fields
        fields = [
            {
                "name": "industry_sector",
                "display_name": "Industry Sector",
                "field_type": "select",
                "is_required": True,
                "options": ["Manufacturing", "Construction", "ICT", "Healthcare", "Tourism", "Agriculture"]
            },
            {
                "name": "qualification_level",
                "display_name": "Qualification Level",
                "field_type": "select",
                "is_required": True,
                "options": ["Certificate I", "Certificate II", "Certificate III", "Certificate IV", "Diploma", "Advanced Diploma"]
            },
            {
                "name": "delivery_mode",
                "display_name": "Delivery Mode",
                "field_type": "multiselect",
                "is_required": False,
                "options": ["Face-to-face", "Online", "Blended", "Workplace-based"]
            },
            {
                "name": "target_audience",
                "display_name": "Target Audience",
                "field_type": "text",
                "is_required": False
            },
            {
                "name": "duration_hours",
                "display_name": "Duration (Hours)",
                "field_type": "number",
                "is_required": False
            },
            {
                "name": "prerequisites",
                "display_name": "Prerequisites",
                "field_type": "text",
                "is_required": False
            },
            {
                "name": "is_core_unit",
                "display_name": "Core Unit",
                "field_type": "boolean",
                "is_required": False,
                "default_value": "false"
            }
        ]
        
        for field_data in fields:
            field = MetadataField(**field_data)
            db.add(field)
        
        db.commit()
        print("✅ Default metadata fields created successfully")
        
    finally:
        db.close()

def initialize_database():
    """Initialize the database with default data."""
    print("🚀 Initializing NOSS database...")
    
    try:
        create_tables()
        create_default_admin()
        create_default_templates()
        create_default_tags()
        create_default_metadata_fields()
        
        print("\n✅ Database initialization completed successfully!")
        print("\n📋 Default Login Credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n⚠️  Please change the default admin password after first login!")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        raise

if __name__ == "__main__":
    initialize_database()
