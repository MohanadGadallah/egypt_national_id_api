
# Egyptian National ID Validator & Extractor API

This project is a backend API built with **FastAPI** to validate Egyptian national IDs and extract associated data. It supports API key authentication, rate limiting based on client IP, and tracks API usage .

##  Features

* Validate and parse Egyptian national ID numbers.
* Extract birth year, gender, governorate, and more.
* API key-based authentication for access control.
* **Rate limiting based on client IP address** to prevent abuse.
* API usage tracking per API key  .
* Dockerized with PostgreSQL and PgAdmin.
* Unit tests with coverage reports.
* **CI workflow to run tests and show quick summary** (no acceptance criteria yet). check it [https://github.com/MohanadGadallah/egypt_national_id_api/actions/runs/17016013427/attempts/1#summary-48238467678](https://github.com/MohanadGadallah/egypt_national_id_api/actions/runs/17016013427/attempts/1#summary-48238467678)

---

##  Running the Project with Docker

1. Clone the repo:

   ```bash
   git clone https://github.com/MohanadGadallah/egypt_national_id_api.git
   cd egypt_national_id_api
   cd national_id_api
   ```

2. Start the services:

   ```bash
   docker compose up
   ```

3. Access docs:

   * Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
   * Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## API key is already seeded in the database.

Include header:

```
x-api-key: test
```

---

## Design Trade-offs and Considerations

* **Row-level locks** are used to protect API usage tracking under concurrent requests. This prevents race conditions with minimal complexity especially important when a company shares the same API key across multiple IPs.
* **Rate limiting is enforced per IP address** to prevent abuse, regardless of API key rotation.
* I considered separating **authentication and usage tracking** into distinct components for better modularity and scalability, but for simplicity, both are currently handled within the same logic.
* **Async usage tracking via a background task queue** (e.g. queue,background task(FastAPI)) was considered to improve performance under high load, but was not implemented to keep the system simple for this task.
* **No national ID data is stored** in the database  privacy is preserved by design.
* Two isolated environments (dev and prod) are set up using **Poetry** as the package manager.(See(click on it)):[`pyproject.toml`](national_id_api/pyproject.toml) 
* In the event of a database outage, it's preferable to **serve the request and potentially lose some usage data** rather than reject the request prioritizing availability and customer experience.


---

## Example Requests

### Invalid ID example

```bash
curl -X POST http://localhost:8000/validate-id \
  -H "accept: application/json" \
  -H "x-api-key: test" \
  -H "Content-Type: application/json" \
  -d '{"national_id": 10000000000000}'
```

Response 

```json
{
  "data": {
    "id_number": "10000000000000",
    "is_valid": false,
    "invalid_id_reason": " invalid century part. and Year of birth is in the future. and invalid month. and invalid day for the month. and invalid governorate ID. ",
    "year_of_birth": 3000,
    "month_of_birth": 0,
    "month_of_birth_name": null,
    "day_of_birth": 0,
    "gender": "Female",
    "governorate_id": 0,
    "governorate_name": null,
    "century": 1
  },
  "message": "Invalid ID .Thanks for using TRU National ID Service",
  "code": "INVALID_ID"
}
```

### Valid ID example

```bash
curl -X POST http://localhost:8000/validate-id \
  -H "accept: application/json" \
  -H "x-api-key: test" \
  -H "Content-Type: application/json" \
  -d '{"national_id": 29905228800910}'
```

Response 

```json
{
  "data": {
    "id_number": "29905228800910",
    "is_valid": true,
    "invalid_id_reason": "",
    "year_of_birth": 1999,
    "month_of_birth": 5,
    "month_of_birth_name": "May",
    "day_of_birth": 22,
    "gender": "Male",
    "governorate_id": 88,
    "governorate_name": "Outside the republic",
    "century": 2
  },
  "message": " Valid ID .thanks for using  National ID Service",
  "code": "VALID_ID"
}
```

---

##  Database Design (Bonus)

The project tracks API usage per API key in a dedicated table with the following columns:

* **id**: A UUID primary key.
* **company_name**: Name of the company owning the API key.
* **api_key**: The unique API key string.
* **usage_count**: Number of API calls made with this key.
* **last_request_at**: Timestamp of the last API call.



---

##  Local Development Setup

* Requires Python 3.13+, Poetry.
* Install dependencies with `poetry install`.
* Run PostgreSQL via Docker separately.
* Adjust `.env` for local DB connection.
* Run tests with `poetry run pytest`.


---
##  Summary

* Chose FastAPI over Django for async support because I’m more familiar with it, it’s lightweight, and I don’t use LLM in task assessments.
* Used **SQLAlchemy + Alembic** for ORM and migrations.
* Applied **Pydantic** models for data validation.
* Implemented **row-level locking** in DB for safe usage count updates.
* Tests use real DB connections for accuracy.
* Rate limiting is based on client IP, not API key.
* Added a **CI workflow that runs tests and provides a quick summary** — it currently does not enforce acceptance criteria but helps ensure tests pass on commits.

---

##  Environment Variables

`.env`

```env
DATABASE_URL=postgresql+asyncpg://postgres:test@postgres:5432/APIUSAGE
TEST_DATABASE_URL=postgresql+asyncpg://postgres:test@postgres:5432/APIUSAGE
```

`database.env`

```env
POSTGRES_DB=APIUSAGE
POSTGRES_USER=postgres
POSTGRES_PASSWORD=test

PGADMIN_DEFAULT_EMAIL=admin@gmail.net
PGADMIN_DEFAULT_PASSWORD=12345678
```

---

##  Test Coverage Reports

* The HTML coverage report is generated under `tests/reports/html`.
* Note: The `.gitignore` currently excludes the HTML coverage folder, but i will add it.

