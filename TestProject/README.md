# TestProject


## Running with docker

```
git clone <github_project_path>

cd TestProject

docker-compose run web python3.10 manage.py migrate #migrate django db inside container

docker-compose up

```

### Run the tests
```
$ python manage.py test
```

### Import the CSV Data to django models
```
$ python3.10 utilities/lo
ad_csv_into_db.py -file_path test_app/data_source/Project_raw_table.csv -model project

$ python3.10 utilities/load_csv_into_db.py -file_path test_app/data_source/WTG_raw_table.csv -model wtg
```

### Developed and Tested using below tools, technologies, frameworks or modules:
```
    OS: macOS Monterey 12.0.1
    IDE: PyCharm 2021.2.1 (Community Edition)
    Python: 3.10
    django: 4.1.7
    DB: Sqlite3
    djangorestframework: 3.14.0
    drf-api-logger: 1.1.2
    pands: 1.5.3
```


### Run DB Migrations

```
$ python3.10 manage.py makemigrations

$ python3.10 manage.py migrate
```

### If you want to run all files manually
```
pre-commit run --all-files
```