database design : https://drawsql.app/teams/mahmuuudtolba/diagrams/rag

setting up database server :

```python
    docker run -d -p  5432:5432  \
        -e POSTGRES_USER=root \
        -e POSTGRES_PASSWORD=password \
        -e POSTGRES_DB=rag \
        -e PGDATA=/var/lib/postgresql/data \
    -v "$(pwd)"/dbstorage:/var/lib/postgresql/data \
    postgres:latest

```

```python
        db_document = result.scalar_one_or_none() # to be debug later line 40 at document_repositroy.py
```
