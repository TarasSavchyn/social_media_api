# Requirements:
# User Registration and Authentication:
Users should be able to register with their email and password to create an account.
Users should be able to login with their credentials and receive a token for authentication.
Users should be able to logout and invalidate their token.
# User Profile:
Users should be able to create and update their profile, including profile picture, bio, and other details.
Users should be able to retrieve their own profile and view profiles of other users.
Users should be able to search for users by username or other criteria.
# Follow/Unfollow:
Users should be able to follow and unfollow other users.
Users should be able to view the list of users they are following and the list of users following them.
# Post Creation and Retrieval:
Users should be able to create new posts with text content and optional media attachments (e.g., images). (Adding images is optional task)
Users should be able to retrieve their own posts and posts of users they are following.
Users should be able to retrieve posts by hashtags or other criteria.
# Likes and Comments (Optional):
Users should be able to like and unlike posts. Users should be able to view the list of posts they have liked. Users should be able to add comments to posts and view comments on posts.

# Schedule Post creation using Celery (Optional):
Add possibility to schedule Post creation (you can select the time to create the Post before creating of it).
# API Permissions:
Only authenticated users should be able to perform actions such as creating posts, liking posts, and following/unfollowing users.
Users should only be able to update and delete their own posts and comments.
Users should only be able to update and delete their own profile.
# API Documentation:
The API should be well-documented with clear instructions on how to use each endpoint.
The documentation should include sample API requests and responses for different endpoints.
# Technical Requirements:
Use Django and Django REST framework to build the API.
Use token-based authentication for user authentication.
Use appropriate serializers for data validation and representation.
Use appropriate views and viewsets for handling CRUD operations on models.
Use appropriate URL routing for different API endpoints.
Use appropriate permissions and authentication classes to implement API permissions.
Follow best practices for RESTful API design and documentation.
Note: You are not required to implement a frontend interface for this task. Focus on building a 
well-structured and well-documented RESTful API using Django and Django REST framework. 
This task will test the junior DRF developer's skills in building RESTful APIs, 
handling authentication and permissions, working with models, serializers, views, 
and viewsets, and following best practices for API design and documentation.

## Using
Clone the repository from GitHub:
```sh
$ git clone https://github.com/TarasSavchyn/theatre_API.git
```
Once you've cloned the repository, navigate into the repository.

Create a virtual environment and activate it using the following commands:
```sh
$ python3 -m venv venv
$ source venv/bin/activate
```

Create file ".env" with the following content:
```python
POSTGRES_ENGINE=POSTGRES_ENGINE
POSTGRES_NAME=POSTGRES_NAME
POSTGRES_USER=POSTGRES_USER
POSTGRES_PASSWORD=POSTGRES_PASSWORD
POSTGRES_HOST=POSTGRES_HOST
POSTGRES_PORT=POSTGRES_PORT
SECRET_KEY=SECRET_KEY
```

Once you've activated your virtual environment install your python packages by running:
```sh
$ pip install -r requirements.txt
```
Now let's migrate our django project:
```sh
$ python3 manage.py migrate
```
If there are no hitches here you should now be able to open your server by running:
```sh
$ python3 manage.py runserver
```
Go to the web browser and enter http://127.0.0.1:8000/api/social/


## Docker
Create file ".env" with the following content:
```python
POSTGRES_ENGINE=POSTGRES_ENGINE
POSTGRES_NAME=POSTGRES_NAME
POSTGRES_USER=POSTGRES_USER
POSTGRES_PASSWORD=POSTGRES_PASSWORD
POSTGRES_HOST=POSTGRES_HOST
POSTGRES_PORT=POSTGRES_PORT
SECRET_KEY=SECRET_KEY

CELERY_BROKER_URL=CELERY_BROKER_URL
CELERY_RESULT_BACKEND=CELERY_RESULT_BACKEND
```
After that create the file "docker-compose.yml"
```python
version: '3'
services:
  # PostgreSQL
  postgres:
    image: postgres:latest
    env_file:
      - .env
    ports:
      - "5432:5432"
    networks:
      - mynetwork
  # Redis
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    networks:
      - mynetwork
  # Django
  web:
    image: savik1992/social_media:latest
    command: python manage.py runserver 0.0.0.0:8000
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    networks:
      - mynetwork
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
networks:
  mynetwork:
    driver: bridge
```
Then open your terminal and navigate to the directory you wish to store the project and run the following commands:
```sh
$ docker push savik1992/social_media
$ docker-compose up
```
Welcome, the application is ready to use at url http://127.0.0.1:8000/admin/social/

