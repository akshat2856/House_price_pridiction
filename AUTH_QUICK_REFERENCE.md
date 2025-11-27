# 🔐 Authentication Quick Reference

## Current Demo Accounts

| Role | Email | Password | Purpose |
|------|-------|----------|---------|
| 🛒 Buyer | demo@delhihouse.com | demo123 | Browse and predict prices |
| 🏪 Seller | seller@delhihouse.com | seller123 | List properties (future feature) |

## How Authentication Works

### 1️⃣ Sign Up (Create New Account)
- **URL**: http://localhost:5000/signup
- **Requirements**:
  - Unique email (not already registered)
  - Password minimum 6 characters
  - Choose role: Buyer or Seller
- **After signup**: Automatically redirects to sign-in page

### 2️⃣ Sign In (Login)
- **URL**: http://localhost:5000/signin
- **What happens**:
  - System finds your account by email
  - Verifies password (hashed, secure)
  - Logs you in with your chosen role
- **After signin**: 
  - Navbar shows: "YourName (buyer)" or "YourName (seller)"
  - Full access to all features

### 3️⃣ User Roles Explained

**Current Implementation**:
- Both buyers and sellers have same access to all features
- Role is displayed in navbar for identification
- Future: Role-based features (buyers save favorites, sellers list properties)

**How to check your role**:
- Look at navbar after signing in
- You'll see: `Full Name (role)`
- Example: "John Doe (buyer)" or "Jane Smith (seller)"

## 🔄 Common Scenarios

### Scenario 1: "I want to create a seller account"
```
1. Go to /signup
2. Enter NEW email (not demo@delhihouse.com)
3. Choose password
4. Select "Seller" role
5. Sign up → Sign in with those credentials
```

### Scenario 2: "Email already exists error"
```
❌ Email already registered. Please sign in.

This means:
- Someone (you or demo) already used this email
- You cannot create duplicate accounts
- Solution: Use different email OR sign in with existing account
```

### Scenario 3: "I want to test as both buyer and seller"
```
Option A: Use demo accounts
- Buyer: demo@delhihouse.com / demo123
- Seller: seller@delhihouse.com / seller123

Option B: Create two accounts
- Account 1: yourname+buyer@gmail.com (role: buyer)
- Account 2: yourname+seller@gmail.com (role: seller)
```

### Scenario 4: "How do I know which role I'm signed in as?"
```
✅ After signing in, check navbar top-right:
- Shows: "Full Name (role)"
- Example: "Demo Buyer (buyer)"
```

## 🐛 Troubleshooting

### Issue: "I tried to sign up with demo@delhihouse.com but can't sign in"
**Reason**: That email already exists in database with password "demo123"  
**Solution**: Either:
- Sign in with demo123 password
- OR use a different email for signup

### Issue: "I don't see my role after signing in"
**Check**: Look at navbar (top right corner)  
**Format**: `👤 Full Name (role) 🚪`  
**Example**: `👤 John Doe (buyer) 🚪`

### Issue: "Can I change my role after signup?"
**Currently**: No automatic way  
**Workaround**: Create a new account with different email and desired role

## 📝 Account Rules

1. **One email = One account**
   - Cannot create duplicate emails
   - Each email can only register once

2. **Role is permanent** (for now)
   - Set during signup
   - Cannot be changed later
   - Must create new account to switch roles

3. **Password requirements**
   - Minimum 6 characters
   - Hashed in database (secure)
   - Cannot be viewed by anyone

4. **Role selection**
   - Choose during signup only
   - Displayed in navbar after signin
   - Both roles have same features (for now)

## 🎯 Testing Authentication

### Test 1: Sign in as Buyer
```
1. Go to http://localhost:5000/signin
2. Email: demo@delhihouse.com
3. Password: demo123
4. Sign in
5. Check navbar → Should show "Demo Buyer (buyer)"
```

### Test 2: Sign in as Seller
```
1. Go to http://localhost:5000/signin
2. Email: seller@delhihouse.com
3. Password: seller123
4. Sign in
5. Check navbar → Should show "Demo Seller (seller)"
```

### Test 3: Create New Buyer Account
```
1. Go to http://localhost:5000/signup
2. Full Name: Test Buyer
3. Email: testbuyer@example.com
4. Password: test123
5. Confirm Password: test123
6. Role: Buyer
7. Sign Up
8. Sign in with testbuyer@example.com / test123
9. Navbar shows: "Test Buyer (buyer)"
```

### Test 4: Create New Seller Account
```
1. Go to http://localhost:5000/signup
2. Full Name: Test Seller
3. Email: testseller@example.com
4. Password: test456
5. Confirm Password: test456
6. Role: Seller
7. Sign Up
8. Sign in with testseller@example.com / test456
9. Navbar shows: "Test Seller (seller)"
```

## 🎨 Visual Guide

### Sign-In Page Shows:
```
┌─────────────────────────────────────┐
│ 📧 Demo Accounts:                   │
│ 🛒 Buyer: demo@delhihouse.com       │
│ 🏪 Seller: seller@delhihouse.com    │
└─────────────────────────────────────┘

Email: [________________]
Password: [________________]
☑ Remember me

[Sign In Button]
```

### After Signing In (Navbar):
```
┌──────────────────────────────────────────┐
│ 🏠 Delhi House Finder                    │
│                                          │
│ 👤 Full Name (role) 🚪                  │
│                    ↑    ↑                │
│                    │    └─ Logout        │
│                    └────── Your Role     │
└──────────────────────────────────────────┘
```

## 💡 Pro Tips

1. **Use demo accounts for quick testing**
   - No need to create accounts
   - Ready to use immediately

2. **Create unique emails for testing**
   - Gmail trick: yourname+test@gmail.com
   - Each +suffix counts as different email

3. **Remember me checkbox**
   - Keeps you logged in
   - No need to sign in every time

4. **Check role in navbar**
   - Always visible after signin
   - Shows full name + role

---

**Last Updated**: November 27, 2025  
**Status**: ✅ Working Perfectly
