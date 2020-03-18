# CUSTOMER SERVICE APPLICATION
This app provides backend with UI to add customer service functionality to an existing platform.

The backend is built by Python with Django, leverages the Django Rest Framework for API work and authentication. Frontend uses jQuery. sqlite3 is used during development while Postgre is the choice for production since it is well supported by Docker/Heroku.

## Running
This app is already deployed to Heroku. You can try it at [https://supportticketmanager.herokuapp.com/](https://supportticketmanager.herokuapp.com/).

Or you can also do it with Docker with the following command:
```sh
docker-compose up --build -d
```

## Features
**Involved parties:**
This app is designed for two types of portal users:
- Customer user: They can self-regiser/sign up for an account via our page.
- Customer service user: Admin can create this kind of account via designed API. UI for this function is out of scope.

**Objects and Permisions**
This app leverages three objects: Ticket & Post and User. There is a many-to-one relationship between post to ticket.
* User (Customer User) can read, create and reply to any ticket. They can delete their own post, as long as it is not the first post - initial query - of the ticket.
* Customer service can read, reply to any ticket, delete their own posts and can't create any ticket.

**Backend APIs**
Notes:
* Server validates credentials information first, then request body before processes the request.
* Basic UI is supported by Django Rest Framework. We can just login and send api requests

Heroku prefix: https://supportticketmanager.herokuapp.com

* Sign up:
    * Endpoint: api/signup/
    * Method: post
    * Header:
        * Content-Type: application/json
    * Request body example:
        {
            "username": "Lyly",
            "first_name": "",
            "last_name": "",
            "email": "lyly@yopmail.com",
            "is_customer_service": "False",
            "password": "12345aaa"
        }
    * Response example:
        {
            "username": "Lyly",
            "first_name": "",
            "last_name": "",
            "email": "lyly@yopmail.com",
            "is_customer_service": False,
            "password": "pbkdf2_sha256$180000$iisBCiQVYz5c$QvItd6mAmTKohCgiUvPT1Z0iu0EdhHjGY7JSay5bq9Y="
        }
    * Note: admin can use this api to create customer service user, passing "True" to "is_customer_service".
* Authentication:
    * Endpoint: api/token/
    * Method: post
    * Header:
        * Content-Type: application/json
    * Request body example:
        {
            "username": "DavidClaw",
            "password": "12345aaa"
        }
    * Response example:
        {
            "token": "9ea93042ba8997529b1433804c3ae0ec0fc8ed5e"
        }
* Create ticket:
    * Endpoint: api/newticket/
    * Method: post
    * Header:
        * Content-Type: application/json
        * Authorization: Token <token>
    * Request body example:
        {
            "subject": "DavidClaw ticket",
            "message": "message content"
        }
    * Response example:
        {
            "id": 38,
            "subject": "DavidClaw ticket"
        }
* Get ticket details:
    * Endpoint: api/tickets/<ticket_id>/posts/
    * Method: get
    * Header:
        * Authorization: Token <token>
    * Response example:
        {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [
                {
                    "id": 91,
                    "username": "Lyly",
                    "message": "message content",
                    "created_at": "2020-03-18T17:17:09.168833+07:00"
                }
            ]
        }
    * Pagination is applied.
* Reply to a ticktet:
    * Endpoint: api/tickets/<ticket_id>/reply/
    * Method: post
    * Header:
        * Content-Type: application/json
        * Authorization: Token <token>
    * Request body example:
        {
            "message": "message content"
        }
    * Response example:
        {
            "id": 83,
            "status": "Success"
        }
* Delete a post:
    * Endpoint: api/posts/<post_id>/
    * Method: delete
    * Header:
        * Content-Type: application/json
        * Authorization: Token <token>

**Frontend**
Support the following basic functions:
* Signup / Login
* Navigation
* Pagination
* Create tickets
* Reply a ticket

**Unit Testing**
All functions are covered by unit tests.

