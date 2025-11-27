"""
Simple script to view all users in the database
Run: python view_database.py
"""

from app import app, db
from database import User
from datetime import datetime

def view_all_users():
    """Display all users in the database"""
    with app.app_context():
        users = User.query.all()
        
        if not users:
            print("❌ No users found in database!")
            return
        
        print("\n" + "="*80)
        print(f"📊 USERS DATABASE - Total Users: {len(users)}")
        print("="*80)
        
        for idx, user in enumerate(users, 1):
            print(f"\n👤 User #{idx}")
            print(f"   ID:           {user.id}")
            print(f"   Full Name:    {user.full_name}")
            print(f"   Email:        {user.email}")
            print(f"   Role:         {user.role.upper()}")
            print(f"   Created:      {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Password:     {user.password_hash[:30]}... (hashed)")
        
        print("\n" + "="*80)
        print(f"\n✅ Total: {len(users)} user(s) in database")
        print("="*80 + "\n")

if __name__ == '__main__':
    view_all_users()
