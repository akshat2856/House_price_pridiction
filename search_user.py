"""
Search for a user by email
Usage: python search_user.py email@example.com
"""

import sys
from app import app, db
from database import User

def search_user(email):
    """Search for a user by email"""
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        
        if user:
            print("\n✅ User Found!")
            print("="*50)
            print(f"Full Name:    {user.full_name}")
            print(f"Email:        {user.email}")
            print(f"Role:         {user.role.upper()}")
            print(f"Created:      {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*50 + "\n")
        else:
            print(f"\n❌ No user found with email: {email}\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("\n❌ Usage: python search_user.py <email>")
        print("Example: python search_user.py demo@delhihouse.com\n")
    else:
        search_user(sys.argv[1])
