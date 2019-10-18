# October Challenge
Just a simple POC with Python, Docker and MySQL

## How to run

Assuming you have docker installed and running:
```
cd word-ranking
docker-compose up
```

## Test Api

You can hit, for instance,
http://localhost:5000/api/topwords?url=https://en.wikipedia.org/wiki/Peace&limit=50
and it should return JSON data.
