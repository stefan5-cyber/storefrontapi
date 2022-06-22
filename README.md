# Initial web store

## Sample RESTful API using

- Python 3.8
- Django framework 4.0
  - djangorestframework
  - djangorestframework-simplejwt
  - drf-nested-routers
  - djoser
  - celery
- Postgres
- Authentication with JWT
- Redis
- Docker

## Requirements

Docker

## Commands

Docker compose up -d --build 

## Endpoints

#### Authentication:

- `/auth/users/`
- `/auth/users/me/`
- `/auth/users/confirm/`
- `/auth/users/resend_activation/`
- `/auth/users/set_password/`
- `/auth/users/reset_password_confirm/`
- `/auth/users/set_username/`
- `/auth/users/reset_username/`
- `/auth/users/reset_username_confirm/`
- `/auth/jwt/create/`
  - `POST` - Use this endpoint to obtain JSON Web Token
- `/auth/jwt/refresh/`
- `/auth/jwt/verify/`

#### Product:

- `/store/products/`
  - `GET` - Product List
  - `POST` - Create new Product (authenticated staff members JWT)

- `/store/products/:id`
  - `GET` - Product detail
  - `PUT` - Update Product (authenticated staff members JWT)
  - `DELETE` - Delete Product (authenticated staff members JWT)

- `/store/products/:id/reviews`
  - `GET` - Reviews list
  - `POST` - Add review for given Product

- `/store/products/:id/reviews/:reviewid`
  - `GET` - Review detail
  - `PUT`- Update Review
  - `DELETE` - Delete Review

#### Collection:

- `/store/collections/`
  - `GET` - Collection List
  - `POST`   - Create new Collection (authenticated staff members JWT)

- `/store/collections/:id`
  - `GET` - Collection detail
  - `PUT` - Update Collection (authenticated staff members JWT)
  - `DELETE` - Delete Collection (authenticated staff members JWT)

#### Customer:

- `/store/customers/`
  - `GET` - Customers List (authenticated staff members JWT)
  - `POST` - Create new Customer (authenticated staff members JWT)

- `/store/customers/me`
  - `GET` - Customer profile (authenticated JWT)
  - `PUT` - Update Customer profile (authenticated JWT)

- `/store/customers/:id`
  - `GET` - Customer detail
  - `PUT` - Update Customer (authenticated staff members JWT)
  - `DELETE` - Delete Customer (authenticated staff members JWT)

#### Cart:

- `/store/cart/`
  - `POST` - Create new Cart (get cart id)

- `/store/cart/:id/items`
  - `GET` - Items list for the given cart
  - `POST` - Add Item in the car

- `store/cart/:id/items/:itemid`
  - `GET` - Item detail
  - `PATCH` - Update Item quantity
  - `DELETE` - Remove Item from cart

#### Orders:

- `/store/orders/`
  - `POST` - Create new Order (authenticated JWT)

- `/store/orders/:id/`
  - `GET` - Order detail
  - `PUT` - Update Order payment status (authenticated staff members JWT)
  - `DELETE` - Delete Order (authenticated staff members JWT)

## Example

#### Open smtp4dev panel via the navigation menu

#### Default SuperUser:
username: `admin`  
password: `password`

#### Step 1:
Create JWT token for superuser
`POST` - `/auth/jwt/create/`

#### Step 2:
Create Cart (get ID)
`POST` - `/store/cart/`

#### Step 3:
Add Items to cart
`POST` - `/store/cart/:id/items`

#### Step 4:
Create Order with cart ID
`POST` - `/store/orders/` - required header (Authorization: JWT < access-token >)

*After creating the order, the background process (celery pkg) sends mail to customer with order details*

**NOTE:** When creating a user `/auth/users/`, the signal handler (post_save) creates a Customer for the given User with default parameters
