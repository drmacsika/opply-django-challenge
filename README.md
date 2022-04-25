# My solution to Opply Technical Challenge.

Table of Contents:
- [Tools](#tools)
- [Installation and Usage](#installation-and-usage)
- [Authentication and Authorization](#authentication-and-authorization)
- [Steps on How to Authenticate](#steps-on-how-to-authenticate)
- [Guide on Endpoint Usage](#guide-on-endpoint-usage)
- [API Documentation](#api-documentation)
- [Pagination](#pagination)
- [Admin](#admin)
- [Project Limitations](#project-limitations)
- [Deployment Guide](#deploying-to-heroku)

## Tools

- Django
- DRF
- JWT Token Authentication
- Django Debug Toolkit
- API Documentation with Swagger UI and Redoc
- Model model for generating tests fixtures and data.

## Installation and Usage

Use the package manager [pip](https://pip.pypa.io/en/stable/) for installation.

- Clone this repo
- Set up and activate a Python virtual environment with ```python3 -m venv venv```
- Navigate to the **src** directory where manage.py is located.
- Create a **.env** file in the **src** folder, add a secret key parameter e.g: SECRET_KEY=very_secure_randomly_generated_key
- Run ```pip install requirements.txt```, you can also use the requirements files in the requirements folder within the core directory.
- Run ```python manage.py makemigrations```
- Run ```python manage.py migrate```
- Create a superuser: run ```python manage.py createsuperuser```
- Run checks ```python manage.py check```
- Run the tests ```python manage.py test```
- Run the server ```python manage.py runserver```
- You can populate the products through the admin panel for testing.

## Authentication and Authorization

- The project utilizes JWT Authentication for its token authentication using the **djangorestframework-simplejwt** package.
- The JWT authentication provides two tokens
- An **access token**, which should have a shorter expiry time such as 5 minutes, but for testing this project, 1 day is set.
- A **refresh token**, which should have a longer expiry time, 15 days is set.

## Steps on How to Authenticate

- Create a new user using the endpoint **${HOST}/api/customers/new**. If you already have a registered user, you can skip this step.
- Make a post request to the login endpoint **${HOST}/api/customers/login** using a valid username and password, you will get a refresh and access token.
- Use the access token to send authorized request to endpoints requiring authentication by setting the authorization header either in clients such as Postman, Insomnia or using the Swagger UI and Redoc provided.
E.g Authorization: `Bearer <access_token>`


## Guide on Endpoint Usage
There are currently 9 active endpoints.
${HOST} is the address of the local host or the server where it is hosted. 

| Endpoints       | Authentication Required         | Method(s)  | Action | 
| ------------- |:-------------:| -----:| :-------------: |
| ${HOST}/api/customers/new | False | POST | Create a new user as a customer |
| ${HOST}/api/customers/login | False |   POST | Generate an access and refresh JWT token for authentication and authorization |
| ${HOST}/api/customers/refresh | True | POST | Generate a new access token using a refresh token. |
| ${HOST}/api/products/ | False | GET | List all available products in a paginated format.
| ${HOST}/api/products/{id}/ | False | GET | Get single product using the id.|
| ${HOST}/api/products/orders/ | True  | GET | Get a list of orders pertaining to a customer |
| ${HOST}/api/products/orders/ | True  | POST | Create an order for a product |
| ${HOST}/api/products/orders/{order_id}/ | True  | GET | Get a single order using the order_id |
| ${HOST}/api/customers/order-history/ | True | GET | Get the order history of an authenticated customer |

## API Documentation
This project has an API documentation with Swagger UI as well as Redoc.
- Access the swagger UI API Doc via **${HOST}/api/swagger/**
- Access the Redoc API Doc via **${HOST}/api/redoc/**


## Pagination
- There is pagination for all list endpoints with a minimum of 10 objects per page. The pagination utilizes a page format.

## Admin
- The admin can be accessed via: ${HOST}/admin. Ideally, you would want to populate just the Product and the Custom Users table. The data of every other table is self-generated when using the endpoints including the Order table. You can also create new users via the endpoint for new customers.

## Project Limitations
- This project does not go in-depth in User Registration processes since it's not the primary scope of the project. It provides a basic registration procedure with auto activation set for every registered user. Hence, there is no change password, reset password, email activation etc.

- There could be possibility of catching more advance edge cases and validations.

## Deploying to Heroku
Here's a short guide on deploying this project to Heroku
- Create a file named **Procfile**, in it, specify the type of server and the location of you wsgi file in your project using dot notation. E.g with gunicorn will be ```web: gunicorn core.wsgi```.

- Create a "runtime.txt" file, and in it, enter the version of python you want this project to run on. This project was built using Python 3.10.1. E.g of an entry will be ```python-3.10.1```.

- With an active Heroku account, create an app instance, you can deploy directly using Heroku cli or create a CI/CD pipeline with Heroku and Github, which will automatically deploy when you push to the Github repo.
