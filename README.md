# Police Data Updater

This project fetches, processes, and stores **Stop and Search** data for the **Metropolitan Police Service** using the [UK Police Data API](https://data.police.uk/docs/method/stops-force/).  
It stores all historical stop and search records in CSV format and updates the file daily.

The project also includes a **daily update mechanism** to keep the dataset fresh, unit tests for key functions, and a **Dockerized deployment** for easy portability across environments.

---

## 📌 Features

- **Historical Data Fetching** – Download all available stop and search records for a specified police force.
- **Data Cleaning & Formatting** – Standardizes columns, removes duplicates, and ensures clean, ready-to-use datasets.
- **Daily Updates** – Appends new data to the existing dataset without overwriting historical records.
- **Dockerized** – Runs anywhere with Docker, using volume mapping to persist CSV files outside the container.
- **Unit Tests** – Includes test coverage for fetching, updating, and utility functions.
---

## 📂 Project Structure

```
stop_search_data/
│── config/                  # Configuration files
│   └── config.py
│
│── data/                    # CSV output folder (persisted outside container)
│   └── metropolitan_stops.csv
│
│── src/                     # Core application code
│   ├── __init__.py
│   ├── fetcher.py           # API calls to fetch stop & search data
│   ├── logger.py            # Logger utility
│   ├── main.py              # Entry point script
│   ├── updater.py           # Logic for updating the dataset
│   └── utils.py             # Helper functions
│
│── tests/                   # Unit tests
│   ├── __init__.py
│   ├── test_fetcher.py
│   ├── test_updater.py
│   └── test_utils.py
│
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # Compose configuration
├── Dockerfile          # Docker build file
│── data_storage_rdms.md     # Database schema documentation
│── data_update.log          # Log file
│── README.md                # Project documentation
```

---

## ⚙️ Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- [Docker Compose](https://docs.docker.com/compose/) installed.

---

## 📦 Setup & Run with Docker Compose

### 1️⃣ Build and start the service

```bash
docker-compose up --build -d
```

This will:
- Build the image from the `Dockerfile`.
- Mount the `./data` folder so CSV persists outside the container.
- Run the updater daily using a loop.

---

### 2️⃣ Check logs

```bash
docker-compose logs -f
```

---

### 3️⃣ Stop the service

```bash
docker-compose down
```

---

## 🗂 Data Persistence

The `data/` folder is mounted as a **Docker volume**.  
When the container stops, the CSV remains available on your local machine.

---

## 🔄 How It Updates Daily

The `docker-compose.yml` contains:

```yaml
command: sh -c "while true; do python src/main.py; sleep 86400; done"
restart: always
```

This ensures:
- The script runs once immediately on startup.
- Waits 24 hours.
- Runs again automatically.

---

## 🧪 Running Tests

From the host machine:

```bash
pytest tests
```

---

## 🛠 Tech Stack

- **Python 3.10**
- **Pandas** for data processing
- **Requests** for API calls
- **Docker Compose** for container orchestration

---

## 🗄 Database Schema (Optional)

If storing in a relational database, recommended schema:

- **stops_and_searches**
- **outcomes**
- **locations**
- **streets**

(More details provided [here]())

