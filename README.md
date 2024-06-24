# Rest Tic-Tac-Toe

## Overview


## Variables
There is a couple different ways to pass variables into the code.
This can either be done via environment variables which is the
method used when running the containers in the prod.
The other way is using a .env file that can be created in
the root of the project directory.
###
| Variable | Description                                                |
|----------|------------------------------------------------------------|
|          |                                                            |
|          |                                                            |
|          |                                                            |
|          |                                                            |
|          |                                                            |

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
* Added APM
* Look into maybe adding synthetic monitoring
* Break out the UI into its own repo
* Look at django-environ for settings

## Contributing
Rawr!

## Authors
Me!
