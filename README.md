# Installation

> **docker-compose up -d**

## Testing

> **docker-compose -f docker-compose-tests.yml up**
>
> **Note**: Current implementation requires the database _to be empty_ for tests(pytest, postman) to work properly. Right now, it requires the celery container to stop, cache and database cleaned up.

# What is this

This is a backend **API** for a restaraunt. It allows you to create, read, update and delete menus, its submenus and the dishes of the submenus. The main feature of the project allows you to use excel file as an admin panel. If you change the excel file, the database will change accordingly.

# Stack

- FastAPI as the main framework.
- PostgreSQL as the database engine.
- SQLAlchemy as ORM and Alembic for migrations.
- Redis for caching
- Celery for background task that tracks changes in the Excel file. Celery app uses RabbitMQ as a broker
- Pytest for testing
- Docker

# Implementation

Whole app is written in async manner for better performance and uses the _service layer_ pattern for code reusability(**src/services**).

Caching is implemented with help of _aioredis_ library. Every **GET** route is saved to cache. Cache is invalidated correctly, when something got created, updated or deleted, leaving cache of unaffected entities untoched. Cache invalidation functions are sent to FastAPI _background tasks_, providing faster response time to user.

This project is covered with tests, both _postman_ and _pytest_ ones(**tests/**)

Celery is here to track Excel file in the **admin/** folder every 15 seconds. Every change in the file will be reflected in the database.

**Note:** The database uses UUID for ID fields, so ID columns should be populated with valid UUID4 values. The price for dishes must have 2 decimal places. Example of correct structure is in the Menu.xlsx file.

# Routes

The documentaion for each route can be accessed in the **localhost:8000/redoc** route. If you don't have the time to install this, here's a brief explanation:

> **/all/** **GET** route is going to get every menu with its children, leaving the count.
>
> **menus/** routes are CRUD, where its children are being counted in "_submenus_count_" and "_dishes_count_" fields(e.g no actual children being passed, only their count). **GET** routes are list of all menus or indivdual menu by id. If wrong ID provided, an 404 exception would be raised. With help of FastAPI dependecies, this ID validation is also present in **PATCH** and **DELETE** routes.
>
> **/menus/{id}/submenus/** routes are almost the same as the **menus/**, to work correctly they require the parent Menu id to be in the URL path, which is also always validated.
>
> **/menus/{id}/submenus/{id}/dishes/** is nothing new too, except for listing dishes submenu validation is optional, due to postman tests(this was a course project, postman tests provided by platform). Pass the ?filter_by_submenu=true in the query to get child dishes of individual submenu. If this query param is not passed, it supposed to return all dishes without validation of parents.
