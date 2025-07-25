# Product Inventory System with Stock Management
A full-stack inventory management system for an online store built with Django (DRF) and React.js.
It allows admins to manage products, their variants/sub-variants, and track stock movements such as purchases and sales.

## Features
 Backend (Django REST Framework)

## Product Management

Create a product with multiple variants and sub-variants (e.g., Size, Color)

List all products with variant details

## Stock Management

- Add stock (purchase) to a specific product variant

- Remove stock (sale) from a specific product variant

- View current stock levels of each variant

- Stock Transactions Report

- View stock in/out history with filters by date range

- Each transaction includes: Variant, Quantity, Type (IN/OUT), Date, User

- Validation & Error Handling

- Robust validation of inputs

- Clean API responses and HTTP status codes

- Handles edge cases like insufficient stock or invalid variant combinations

- RESTful & Secure

- APIs follow REST principles

- Token-based authentication (if implemented)

- Admin-level actions protected via permissions

## Frontend (React.js)

- Create Product Form

- Add new product with variants and sub-variant options dynamically

- JSON-based structure for frontend → backend sync

# Product List

- Displays product name, variants, stock availability

# Stock Actions

- Add or remove stock for a specific variant

- Displays updated quantity after transaction

# Stock Report

- View list of transactions (IN/OUT)

- Filter transactions by date range

- Display product name, variant, quantity, type, date

## UI/UX Features

- Form validations with inline error messages

- Alerts for API errors and confirmations
 
- Simple, clean interface with responsive layout

## Tech Stack
- Layer	Technology
- Backend	Django, Django REST Framework
- Frontend	React.js, Axios
- Database	SQLite (dev)
- Auth 	JWT Token Auth
- Styling	Tailwind CSS 


# Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/abhinandbhaskar/product-inventory-backend.git
cd product-inventory-backend


2. **Create & Activate Virtual Environment:**
python -m venv venv
venv\Scripts\activate    # For Windows
# source venv/bin/activate    # For macOS/Linux


3. **Install Dependencies:**
pip install -r requirements.txt


4.**Apply Migrations:**
python manage.py makemigrations
python manage.py migrate


5. **Create Admin User:**
python manage.py createsuperuser

Username (Required)
Email (Required)
Password (Required)

**After Superuser Login — Creating New Admin Users:**
Login to the Django Admin Panel using the superuser credentials.

Go to Users → Add User.

While adding a new user, make sure to:

Provide Username (Required)

Password-based authentication: enabled

Set Password (Required)

Click Save.

Go to Users → Add User profiles

click -> Add user profile

then select a created username from select box

Check Is Admin (If applicable in your model)

Click Save.


6.**Run the Development Server:**
python manage.py runserver

7.**also at the same time run react server**

npm run dev



7.**Access the App in Browser:**

http://localhost:5173/



## References

- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Documentation](https://reactjs.org/)
- [Django Model Relationships](https://docs.djangoproject.com/en/5.2/topics/db/models/)
- [Axios HTTP Client](https://axios-http.com/)
- [ChatGPT by OpenAI](https://chat.openai.com/) – Used as a coding assistant
