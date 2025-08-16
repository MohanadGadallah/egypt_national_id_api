# egypt_national_id_api
Egyptian National ID Validator API  An API to verify and extract information from Egyptian national IDs


# to run seeds commands
```bash
cd national_id_api
```
Then
```bash

python app/database_seeds.py
```


# To Run Tests
```bash
cd national_id_api
```

```bash
 pytest --cov=app --cov-report=term --cov-report=html --cov-report=xml
```