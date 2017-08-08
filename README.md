# Tab Keeper

Keeping track for money among friends. Demo for week2 Practical Programming.

## Run in Development Mode
You need to have a postgres running in background with database name tabkeeper with access from user `postgres` with blank`''` password. This should be the default already.

### Requirement
```
pip install psycopg2 flask
```
### Create and DB
#### create
create the databse
```
python create_tables.py
```
#### seed
populate the database with some data
```
python seed.py
```

### Run the App
```
python app.py
```
Access it at localhost:5000

## Production Mode

It relies on having a file called `secret` the project directory to store the password. The file is gitignored so you need to create one. Then you can do the usual `docker-compose up`.
