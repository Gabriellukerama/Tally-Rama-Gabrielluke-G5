# Tally

Tally is an offline-friendly sales register built with Django and PostgreSQL (Supabase). It helps cashiers, small-store owners and independent sellers manage products, record customer purchases, and calculate totals and change accurately.

## Core Feature (Project Development 2): Product and Category Management

The catalog is the foundation of the sales workflow, since a purchase can only be rung up from products that have prices, categories and stock.

- **Owner:** creates, views, edits and deletes categories and products (name, category, price, stock quantity).
- **Cashier:** views the product catalog and filters it by category; cannot add, edit or delete.
- **Validation:** required names, price of at least 0.01, non-negative stock, valid category, unique category names, and a category with products cannot be deleted. Clear success and error messages are shown.
- **Integration with accounts:** only logged-in users can access the catalog, each product records the user who created it (ForeignKey), and access follows the user's role.
- **Persistence:** all records are stored in PostgreSQL on Supabase.

## Standard Features (Project Development 1)

- Account registration with validation and hashed passwords
- Login and logout
- Role-based dashboards (Owner and Cashier)
- User profile with editable details and photo

## Tech Stack

Django (templates), PostgreSQL via Supabase, Python 3, python-dotenv, Pillow.

## Setup

1. Clone the repository and open the folder:
   ```bash
   git clone https://github.com/Gabriellukerama/Tally-Rama-Gabrielluke-G5.git
   cd Tally-Rama-Gabrielluke-G5
   ```
2. Create and activate a virtual environment, then install the packages:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root (this file is ignored by Git):
   ```
   SECRET_KEY=your-long-random-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_NAME=postgres
   DB_USER=postgres.your-project-ref
   DB_PASSWORD=your-database-password
   DB_HOST=your-supabase-pooler-host
   DB_PORT=5432
   DB_SSLMODE=require
   ```
   Use the **Session pooler** connection details from Supabase (Connect, then Direct). The direct host only works on networks with IPv6.
4. Apply migrations and create an admin account:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Start the server and open http://127.0.0.1:8000/:
   ```bash
   python manage.py runserver
   ```
6. New sign-ups are Cashiers. To make an Owner, log in to `/admin/`, open the user and set Role to Owner.

## Test Accounts

| Role | Username | Password |
|---|---|---|
| Owner | admin123 | admin123 |
| Cashier | lukerama123 | Cashier123! |

## Branching

`main` holds stable code, `develop` is the integration branch, and each feature is built on a `feature/<name>` branch and merged through a Pull Request.

## Roadmap

Sales register with automatic totals and change calculation, transaction history, sales summary, and offline operation.