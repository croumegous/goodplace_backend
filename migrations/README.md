# Migrations

## Init config file and location
```
poetry run aerich init -t good_place.db.utils.TORTOISE_CONFIG
```

## Init DB
```
poetry run aerich init-db
```
## Generate the migrations

```
poetry run aerich migrate --name <migation_name>
```

## Run the migrations

```
poetry run aerich upgrade
```

## Revert migrations

```
poetry run aerich downgrade
```
To downgrade multiple versions :
```
poetry run aerich downgrade -v -2 
```

`base` can be replaced by the revision id where you want to go back.
