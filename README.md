# Alembic

### Change Connection String
If there is a need to change the existing connection string go to `alembic.ini` and find `sqlalchemy.url`. 
There is no need for quotes
```javascript
sqlalchemy.url = your_connection_string
```

### Using Alembic
To update your tables to the latest version of the migration script use `poetry run alembic upgrade head`

If you have added any new tables under the model directory, go to `alembic/env.py` and import its `Base`
```python
from model.NEW_TABLE import Base
```

`from model.Base import Base as og_base` is a collection of all the metadata of all the tables above so that 
alembic will know what has changed

#### Autogeneration
After adding or removing tables/columns, run `poetry run alembic revision --autogenerate -m "NAME_OF_THE_CHANGE"`
