# Rest Tic-Tac-Toe

## Overview
During one of my interviews rather than having a 1337 code challenge, I was asked to build a rest api to play Tic-Tac-Toe.
After the interview I looked around and saw this was a standard coding practice to learn a language. Granted I've been 
using python for a number of years, I thought it was still a lot of fun so wanted to finish where I left off and clean up
a bit. So this project was built without the help of AI such as Copilot. I also took it to the next step of building a 
frontend using Vue as that is the current frontend framework that I have been using. 

## Variables
There is a couple different ways to pass variables into the code.
This can either be done via environment variables which is the
method used when running the containers in the prod.
The other way is using a .env file that can be created in
the root of the project directory.
###
| Variable          | Description |
|-------------------|-------------|
| API_LOGGER_LEVEL  |             |
| DJANGO_DEBUG      |             |
| DJANGO_ORIGINS    |             |
| DJANGO_SECRET_KEY |             |


## Docker
* Docker installed wih Docker compose

### Development
Build the docker container for development environment:
```
docker compose -f docker-compose.dev.yaml build
```
Serve the app for development environment:
```
docker compose -f docker-compose.dev.yaml up
```
Because hot-reload can get itself stuck enter the container
and execute the process for npm and django:
```
docker exec -it tictotactotoe bash
npm run serve --prefix /home/mine/tictotactotoe-ui
gunicorn --chdir /home/mine/tictotactotoe --reload tictotactotoe.wsgi:application
```

Sometimes gunicorn does not handle hot reload well so can use this as well to serve the python.
```
python3 /home/mine/tictotactotoe/manage.py runserver
```

When all done and need to clean up
```
docker compose -f docker-compose.dev.yaml down
```
### Production
Build the docker container:
```
docker build -f Dockerfile -t tictotactotoe:latest .
```
Run the container assuming SSL loading is happened at a load balancer:
```
docker run --rm -p 80:80 tictotactotoe:latest
```

## Running Tests
Running test are done in the Djagno Framework and test the API.
One can run all the tests built by running these commands.
```
cd tictotactotoe
python3 manage.py test
```
One can also run a specific test within the test case by using the these commands.
```
cd tictotactotoe
python3 manage.py test tests.test_api.TicToTacToToeApiTestCase.test_true
```
Just change the "test_true" to the specific test name.

Running Tests is great but also need to be able to make sure we are getting good code coverage as the project grows.
Coverage is part of the requirements to get a good idea of everything tested.
```
cd tictotactotoe
coverage run manage.py test
coverage report
```

## Future ToDos
* Add helm chart for fun
* Move away from sqlite and move to postgres
* Setup more logging
* Add APM
* Look into maybe adding synthetic monitoring
* Break out the UI into its own repo

## Contributing
Rawr!

## Authors
Me!
