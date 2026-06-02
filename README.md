# FastAPI Customer Management System

## Overview

A Customer Management REST API built with FastAPI, SQLAlchemy, and MySQL.

The project provides CRUD operations for:

* Customers
* Addresses
* Orders

It also includes:

* Customer Search
* Customer Restore
* Soft Delete Functionality
* Order Management
* Address Management

---

## Features

### Customer Management

* Add Customer
* View Customers
* Update Customer
* Search Customer
* Soft Delete Customer
* Restore Customer

### Address Management

* Add Address
* View Address
* Update Address
* Delete Address

### Order Management

* Add Order
* View Order
* Update Order
* Delete Order

---

## Technologies Used

* Python
* FastAPI
* SQLAlchemy
* MySQL
* Pydantic
* Uvicorn

---

## Project Structure

```text
project/
│
├── main.py
├── model.py
├── database.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/customer-management-api.git
cd customer-management-api
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

to access Swagger UI.

---

## API Endpoints

### Customer

* POST `/ADD-CUSTOMER`
* GET `/SHOW-CUSTOMERS`
* PUT `/UPDATE-CUSTOMER/{customer_id}`
* DELETE `/SOFT.delete-customer/{id}`
* PUT `/RESTORE-CUSTOMER/{id}`

### Address

* GET `/ADDRESS`
* PUT `/update-address/{customer_id}`
* DELETE `/DElETE-ADDRESS/{id}`

### Orders

* POST `/ADD-ORDER/{customers_id}`
* GET `/SHOW-ORDER/{Customer_id}`
* PUT `/update-order/{order_id}`
* DELETE `/DELETE-ORDER/{id}`

### Search

* GET `/SEARCH-CUSTOMER-BY(Name-Email-ID)`

---

## Author

Ritesh Saini
