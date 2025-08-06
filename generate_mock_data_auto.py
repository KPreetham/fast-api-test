#!/usr/bin/env python3
"""
Automated script to generate comprehensive mock data for the FastAPI demo application
Generates 100+ users with 20-50 posts each without user interaction
"""

import random
from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy.orm import Session

from auth import get_password_hash
from database import SessionLocal, engine
from models import Base, Post, User

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize Faker for generating realistic data
fake = Faker()

# Categories for posts to make them more realistic
POST_CATEGORIES = [
    "Technology", "Programming", "Web Development", "Data Science",
    "Machine Learning", "DevOps", "Cybersecurity", "Mobile Development",
    "Database Design", "API Development", "Frontend", "Backend",
    "Cloud Computing", "Docker", "Kubernetes", "Microservices",
    "Testing", "CI/CD", "Agile", "Project Management"
]

# Post titles templates
POST_TITLES = [
    "Getting Started with {topic}",
    "Best Practices for {topic}",
    "Advanced {topic} Techniques",
    "Common Mistakes in {topic}",
    "How to Optimize {topic}",
    "Understanding {topic} Fundamentals",
    "Tips and Tricks for {topic}",
    "Troubleshooting {topic} Issues",
    "Modern Approaches to {topic}",
    "Deep Dive into {topic}",
    "Building Scalable {topic} Solutions",
    "Security Considerations in {topic}",
    "Performance Optimization in {topic}",
    "Integration Patterns for {topic}",
    "Testing Strategies for {topic}",
    "Deployment Best Practices for {topic}",
    "Monitoring and Logging in {topic}",
    "Architecture Patterns for {topic}",
    "Code Quality in {topic}",
    "Team Collaboration in {topic} Projects"
]

# Post content templates
POST_CONTENT_TEMPLATES = [
    """
# {title}

## Introduction
{intro}

## Key Points
{key_points}

## Conclusion
{conclusion}

---
*Posted on {date}*
""",
    """
## {title}

{intro}

### Main Content
{main_content}

### Summary
{summary}

---
*Published: {date}*
""",
    """
# {title}

{intro}

## Detailed Analysis
{analysis}

## Recommendations
{recommendations}

---
*Created: {date}*
"""
]


def generate_user_data():
    """Generate realistic user data"""
    return {
        "name": fake.name(),
        "email": fake.unique.email(),
        "password": "password123"  # All users get the same password for testing
    }


def generate_post_content(title, category):
    """Generate realistic post content"""
    template = random.choice(POST_CONTENT_TEMPLATES)

    intro = fake.paragraph(nb_sentences=3)
    key_points = "\n".join([f"- {fake.sentence()}" for _ in range(random.randint(3, 6))])
    main_content = fake.text(max_nb_chars=500)
    analysis = fake.text(max_nb_chars=400)
    recommendations = "\n".join([f"- {fake.sentence()}" for _ in range(random.randint(2, 4))])
    summary = fake.paragraph(nb_sentences=2)
    conclusion = fake.paragraph(nb_sentences=2)

    content = template.format(
        title=title,
        intro=intro,
        key_points=key_points,
        main_content=main_content,
        analysis=analysis,
        recommendations=recommendations,
        summary=summary,
        conclusion=conclusion,
        date=fake.date_between(start_date='-1y', end_date='today').strftime('%B %d, %Y')
    )

    return content


def generate_post_title(category):
    """Generate a realistic post title"""
    template = random.choice(POST_TITLES)
    return template.format(topic=category)


def generate_mock_data_auto(num_users=100, min_posts_per_user=20, max_posts_per_user=50, clear_existing=True):
    """Generate comprehensive mock data automatically"""
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            if clear_existing:
                print(f"🗑️  Clearing existing {existing_users} users...")
                db.query(Post).delete()
                db.query(User).delete()
                db.commit()
                print("✅ Cleared existing data.")
            else:
                print(f"⚠️  Database already has {existing_users} users. Skipping generation.")
                return

        print(f"🚀 Generating {num_users} users with {min_posts_per_user}-{max_posts_per_user} posts each...")

        # Generate users
        users = []
        for i in range(num_users):
            user_data = generate_user_data()
            hashed_password = get_password_hash(user_data["password"])

            user = User(
                name=user_data["name"],
                email=user_data["email"],
                password=hashed_password
            )
            users.append(user)
            db.add(user)

            if (i + 1) % 20 == 0:
                print(f"   Created {i + 1} users...")

        db.commit()
        print(f"✅ Created {len(users)} users successfully!")

        # Generate posts for each user
        total_posts = 0
        for i, user in enumerate(users):
            num_posts = random.randint(min_posts_per_user, max_posts_per_user)

            for j in range(num_posts):
                category = random.choice(POST_CATEGORIES)
                title = generate_post_title(category)
                content = generate_post_content(title, category)

                # Generate realistic creation date (within last year)
                created_at = fake.date_time_between(
                    start_date='-1y',
                    end_date='now'
                )

                post = Post(
                    user_id=user.id,
                    title=title,
                    content=content,
                    created_at=created_at,
                    updated_at=created_at
                )
                db.add(post)
                total_posts += 1

            if (i + 1) % 20 == 0:
                print(f"   Generated posts for {i + 1} users...")

        db.commit()

        print(f"🎉 Mock data generation completed!")
        print(f"   📊 Total users: {len(users)}")
        print(f"   📝 Total posts: {total_posts}")
        print(f"   📈 Average posts per user: {total_posts / len(users):.1f}")

        # Show some sample data
        print(f"\n📋 Sample Users:")
        for i, user in enumerate(users[:3]):
            user_posts = db.query(Post).filter(Post.user_id == user.id).count()
            print(f"   {i+1}. {user.name} ({user.email}) - {user_posts} posts")

        print(f"\n📋 Sample Posts:")
        sample_posts = db.query(Post).limit(3).all()
        for i, post in enumerate(sample_posts):
            user = db.query(User).filter(User.id == post.user_id).first()
            print(f"   {i+1}. '{post.title}' by {user.name}")

        print(f"\n🔐 Test Credentials:")
        print(f"   Email: {users[0].email}")
        print(f"   Password: password123")

        return {
            "users_created": len(users),
            "posts_created": total_posts,
            "sample_user_email": users[0].email
        }

    except Exception as e:
        print(f"❌ Error generating mock data: {e}")
        db.rollback()
        return None
    finally:
        db.close()


def main():
    """Main function to run the automated mock data generation"""
    print("🎭 Automated Mock Data Generator for FastAPI Demo")
    print("=" * 55)

    # Default configuration
    num_users = 100
    min_posts = 20
    max_posts = 50
    clear_existing = True

    print(f"📋 Configuration:")
    print(f"   Users: {num_users}")
    print(f"   Posts per user: {min_posts}-{max_posts}")
    print(f"   Estimated total posts: {num_users * (min_posts + max_posts) // 2}")
    print(f"   Clear existing data: {clear_existing}")

    result = generate_mock_data_auto(num_users, min_posts, max_posts, clear_existing)

    if result:
        print(f"\n✅ Successfully generated mock data!")
        print(f"   Ready to test your API endpoints!")
    else:
        print(f"\n❌ Failed to generate mock data.")


if __name__ == "__main__":
    main()
