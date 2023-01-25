Api for books and comments managment. Developed with Python, FastApi, Pytest, SQLALchemy, Docker

## To run the unit tests
```
pytest
```

## To run the api
```
docker build . -t books-manager
docker run --name books-manager-container -p 8000:8000/tcp books-manager
```

## clean:
```
docker stop books-manager-container
docker rm books-manager-container
```

## OpenApi doc
```
127.0.0.1:8000
```
