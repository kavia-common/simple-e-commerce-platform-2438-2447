# simple-e-commerce-platform-2438-2447

## Django Backend Quickstart

1. **Install Python dependencies:**
    ```
    pip install -r backend_django/requirements.txt
    ```

2. **Make and Apply Migrations:**
    ```
    python backend_django/manage.py makemigrations api
    python backend_django/manage.py migrate
    ```

3. **Create a Superuser (for admin):**
    ```
    python backend_django/manage.py createsuperuser
    ```

4. **Run Development Server:**
    ```
    python backend_django/manage.py runserver 0.0.0.0:3001
    ```

5. **API Endpoints:**
    - All endpoints under `/api/`
        - `/api/products/`
        - `/api/register/` and `/api/profile/`
        - `/api/token/` and `/api/token/refresh/` (JWT Auth)
        - `/api/cart/`
        - `/api/orders/`
    - API Documentation (Swagger): http://localhost:3001/docs (via drf-yasg)

6. **Regenerate OpenAPI Spec:**
    ```
    python backend_django/manage.py generate_openapi
    ```
