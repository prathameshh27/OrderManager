# Order Manager API

The Order Management Application is a web service designed to facilitate the creation and management of purchase orders. It provides a RESTful interface for handling order-related operations, such as create, update, list, describe, and delete.

## Table of Contents

1. [Order Manager API](#order-manager-api)
   - [Getting Started](#getting-started)
     - [Prerequisites](#prerequisites)
   - [Installation (Docker)](#installation-docker)
   - [Installation (Local test server)](#installation-local-test-server)
   - [Authentication](#authentication)
     - [Get Bearer Token](#get-bearer-token)
     - [Refresh Access Token](#refresh-access-token)
   - [Purchase Orders](#purchase-orders)
     - [List all Purchase Orders](#list-all-purchase-orders)
     - [Create Order](#create-order)
     - [Get Purchase Order](#get-purchase-order)
     - [Update Order](#update-order)


## Getting Started

These instructions will help you understand the available API endpoints and how to use them.

### Prerequisites

- Python 3.10
- Django 5.0
- Django REST framework 3.14
- Postman (for testing the APIs)

## Installation (Docker)
This approach will help you to install the application on docker with postgres or sqlite database.  
Make sure you have docker installed on your system.  
If not, skip to [Installation (Local test server)](#installation-local-test-server) - postgres not supported
1. #### Clone this repository to your local machine

   ```shell
   git clone https://github.com/prathameshh27/OrderManager.git
   ```

2. #### configure the .env file (root dir).

```shell
cd OrderManager
```

Setup the superuser creds:

```shell
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin@123
ADMIN_EMAIL=admin@host.com
```

Setup the Database: choose between 'postgres' or 'sqlite'
```shell
DB_TYPE = postgres
```

3. #### Build and run the container
```shell
docker-compose up --build
```

The application will be accessible at http://127.0.0.1:8080/.

## Installation (Local test server)

1. #### Clone this repository to your local machine

   ```shell
   git clone https://github.com/prathameshh27/OrderManager.git
   ```


2. #### Create and Activate the virtual environment to isolate dependencies:

    ```shell
   cd OrderManager
   ```

   ```shell
   virtualenv env

   source env/bin/activate   # On macOS/Linux
   env\Scripts\activate      # On Windows
   ```

3. #### Install the required Python packages:

Navigate to the project folder and install the dependencies using pip:

```shell
pip install -r requirements.txt     # skip
```

4. #### configure the .env file (root dir).
Setup the superuser creds:

```shell
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin@123
ADMIN_EMAIL=admin@host.com
```

Setup the Database:  
***Note:*** postgres will only work in docker.
```shell
DB_TYPE = sqlite
```


5. #### Run the Django application:

Start the Django development server:

```shell
python manage.py migrate
python manage.py runserver 0.0.0.0:8080
```
The application will be accessible at http://127.0.0.1:8080/.


## API Specifications
The API specifications for the application are available at the below endpoints:  
```
/api/schema/swagger/
/api/schema/redoc/ 
```

## Authentication
This section describes the available API endpoints for Authentication, their purposes, and the expected input and output data for each operation.

### Get Bearer Token

Allows the user to retrieve a bearer token for accessing the API endpoints. Accepts username and password.

- **URL:** `/api/auth/token/`
- **Method:** `POST`
- **Security:**
  - None



#### Request Body

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

#### Response

```json
{
  "access_token": {
    "token": "your_access_token",
    "valid_upto": "token_validity_date"
  },
  "refresh_token": {
    "token": "your_refresh_token",
    "valid_upto": "refresh_token_validity_date"
  }
}
```

### Refresh Access Token

Allows the user to refresh the short persistent access token for accessing the API endpoints. Accepts a Refresh token previously obtained from the Auth token API endpoint.

- **URL:** `/api/auth/token/refresh/`
- **Method:** `POST`
- **Security:**
  - None


#### Request Body

```json
{
  "refresh_token": "your_refresh_token"
}
```

#### Response

```json
{
  "access_token": {
    "token": "your_new_access_token",
    "valid_upto": "new_token_validity_date"
  }
}
```

## Purchase Orders
This section describes the available API endpoints for the operations on Purchase Order, their purposes, and the expected input and output data for each operation.     


### List all Purchase Orders

Allows the user to retrieve all existing purchase orders along with the line items. The orders are sorted by the PO number in descending order. The user can also use the query parameters to filter the list.

- **URL:** `/api/v1/purchase/order/`
- **Method:** `GET`
- **Security:**
  - JWT Auth
- **Query Parameters:**
  - `item_name`: filter by item name
  - `supplier_name`: filter by supplier name


#### Header
```
Authorization: Bearer access_token
```


#### Response

```json
[
  {
    "id": "purchase_order_id",
    "supplier": {
      "id": "supplier_id",
      "name": "supplier_name",
      "email": "supplier_email"
    },
    "order_number": 123,
    "order_time": "order_timestamp",
    "total_amount": "total_order_amount",
    "total_quantity": 10,
    "total_tax": "total_order_tax",
    "line_items": [
      {
        "id": "line_item_id",
        "item_name": "item_name",
        "quantity": 5,
        "price_without_tax": "item_price",
        "tax_name": "tax_name",
        "tax_amount": "item_tax",
        "line_total": "item_line_total"
      }
    ]
  }
]
```

### Create Order

Allows the user to create a new purchase order. Accepts multiple line items and a non-existing Supplier.

- **URL:** `/api/v1/purchase/order/`
- **Method:** `POST`
- **Security:**
  - JWT Auth

#### Header

```
Authorization: Bearer access_token
```

#### Request Body

```json
{
  "supplier": {
    "name": "supplier_name",
    "email": "supplier_email"
  },
  "line_items": [
    {
      "item_name": "item_name",
      "quantity": 5,
      "price_without_tax": "item_price",
      "tax_name": "tax_name",
      "tax_amount": "item_tax"
    }
  ]
}
```

#### Response

```json
{
  "id": "purchase_order_id",
  "supplier": {
    "id": "supplier_id",
    "name": "supplier_name",
    "email": "supplier_email"
  },
  "order_number": 123,
  "order_time": "order_timestamp",
  "total_amount": "total_order_amount",
  "total_quantity": 10,
  "total_tax": "total_order_tax",
  "line_items": [
    {
      "id": "line_item_id",
      "item_name": "item_name",
      "quantity": 5,
      "price_without_tax": "item_price",
      "tax_name": "tax_name",
      "tax_amount": "item_tax",
      "line_total": "item_line_total"
    }
  ]
}
```

### Get Purchase Order

Allows the user to retrieve an existing purchase order with a purchase order ID.

- **URL:** `/api/v1/purchase/order/{id}/`
- **Method:** `GET`
- **Security:**
  - JWT Auth
- **Path Parameter:**
  - `id`: purchase order ID

#### Header

```
Authorization: Bearer access_token
```

#### Response

```json
{
  "id": "purchase_order_id",
  "supplier": {
    "id": "supplier_id",
    "name": "supplier_name",
    "email": "supplier_email"
  },
  "order_number": 123,
  "order_time": "order_timestamp",
  "total_amount": "total_order_amount",
  "total_quantity": 10,
  "total_tax": "total_order_tax",
  "line_items": [
    {
      "id": "line_item_id",
      "item_name": "item_name",
      "quantity": 5,
      "price_without_tax": "item_price",
      "tax_name": "tax_name",
      "tax_amount": "item_tax",
      "line_total": "item_line_total"
    }
  ]
}
```

### Update Order

Allows the user to update an existing purchase order. Accepts multiple line items and a non-existing Supplier.

- **URL:** `/api/v1/purchase/order/{id}/`
- **Method:** `PUT`
- **Security:**
  - JWT Auth
- **Path Parameter:**
  - `id`: purchase order ID

#### Header

```
Authorization: Bearer access_token
```

#### Request Body

```json
{
  "supplier": {
    "name": "new_supplier_name",
    "email": "new_supplier_email"
  },
  "line_items": [
    {
      "id": "line_item_id",
      "item_name": "new_item_name",
      "quantity": 3,
      "price_without_tax": "new_item_price",
      "tax_name": "new_tax_name",
      "tax_amount": "new_item_tax"
    }
  ]
}
```

#### Response

```json
{
  "id": "purchase_order_id",
  "supplier": {
    "id": "supplier_id",
    "name": "new_supplier_name",
    "email": "new_supplier_email"
  },
  "order_number": 123,
  "order_time": "order_timestamp",
  "total_amount": "new_total_order_amount",
  "total_quantity": 8,
  "total_tax": "new_total_order_tax",
  "line_items": [
    {
      "id": "line_item_id",
      "item_name": "new_item_name",
      "quantity": 3,
      "price_without_tax": "new_item_price",
      "tax_name": "new_tax_name",
      "tax_amount": "new_item_tax",
      "line_total": "new_item_line_total"
    }
  ]
}
```


### Delete Purchase Order

Allows the user to delete an existing purchase order with a purchase order ID.

- **URL:** `/api/v1/purchase/order/{id}/`
- **Method:** `DELETE`
- **Security:**
  - JWT Auth
- **Path Parameter:**
  - `id`: purchase order ID

#### Header

```
Authorization: Bearer access_token
```

#### Response

```json
{
  "message": "Purchase order deleted"
}
```


## Testing
Prerequisites: [Installation (Local test server)](#installation-local-test-server)    

Open the root dir in the terminal and run the below command:
```shell
python manage.py test
```

