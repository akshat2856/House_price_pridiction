"""
Delete a user from database
Usage: python delete_user.py email@example.com
"""

import sys
from app import app, db
from database import User

def delete_user(email):
    """Delete a user by email"""
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        
        if user:
            user_name = user.full_name
            confirm = input(f"⚠️  Are you sure you want to delete '{user_name}' ({email})? (yes/no): ")
            
            if confirm.lower() == 'yes':
                db.session.delete(user)
                db.session.commit()
                print(f"\n✅ User '{user_name}' deleted successfully!\n")
            else:
                print("\n❌ Deletion cancelled.\n")
        else:
            print(f"\n❌ No user found with email: {email}\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("\n❌ Usage: python delete_user.py <email>")
        print("Example: python delete_user.py demo@delhihouse.com\n")
    else:
        delete_user(sys.argv[1])
