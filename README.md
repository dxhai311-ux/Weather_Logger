# Weather Logger

A simple ETL project that collects weather data from OpenWeather API and stores it in PostgreSQL.

## Features

- Fetch weather data from OpenWeather API
- Convert JSON response into Python data
- Store data in PostgreSQL using SQLAlchemy
- Secure API key management with `.env`
- Handle network/API connection errors

## Tech Stack

- Python
- Requests
- PostgreSQL
- SQLAlchemy
- python-dotenv

## Workflow

```text
OpenWeather API
      ↓
   JSON Data
      ↓
 Python Processing
      ↓
 PostgreSQL
```

## Run

```bash
python main.py
```

## Future Improvements

- Add timestamp (`created_at`)
- Support multiple cities
- Export data to CSV
- Schedule automatic data collection