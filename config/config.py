from datetime import datetime

FORCE_ID = 'metropolitan'
CSV_FILE = '/app/data/metropolitan_stops.csv'
EARLIEST_DATA_DATE = datetime(2025, 1, 1)
API_URL_TEMPLATE = "https://data.police.uk/api/stops-force?force={force}&date={date}"