"""Bank market capitalization ETL."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
import re
import sqlite3

from bs4 import BeautifulSoup
import pandas as pd
import requests


SOURCE_URL = (
    "https://web.archive.org/web/20230908091635/"
    "https://en.wikipedia.org/wiki/List_of_largest_banks"
)
RATES_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv"
)
TABLE_NAME = "Largest_banks"
LOG_PATH = Path("code_log.txt")


def log_progress(message: str) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    with LOG_PATH.open("a", encoding="utf-8") as log:
        log.write(f"{timestamp} : {message}\n")


def _read_text(source: str) -> str:
    local_file = Path(source)
    if local_file.is_file():
        return local_file.read_text(encoding="utf-8")
    response = requests.get(source, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    return response.text


def extract(url: str = SOURCE_URL, table_attribs: tuple[str, str] = ("Name", "MC_USD_Billion")) -> pd.DataFrame:
    soup = BeautifulSoup(_read_text(url), "html.parser")
    heading = soup.find(id="By_market_capitalization")
    if heading is None:
        heading = soup.find(string=re.compile(r"By market capitalization", re.I))
    if heading is None:
        raise ValueError("Could not locate the 'By market capitalization' section")

    table = heading.find_next("table", class_=lambda c: c and "wikitable" in c)
    if table is None:
        raise ValueError("Could not locate the market capitalization table")

    rows: list[tuple[str, float]] = []
    for tr in table.find_all("tr"):
        cells = tr.find_all(["th", "td"], recursive=False)
        if len(cells) < 3:
            continue
        rank = cells[0].get_text(" ", strip=True)
        if not re.match(r"^\d+\b", rank):
            continue
        name = re.sub(r"\s*\[\d+\]", "", cells[1].get_text(" ", strip=True)).strip()
        amount = cells[2].get_text(" ", strip=True)
        amount = re.sub(r"\[[^]]*\]", "", amount).replace(",", "")
        match = re.search(r"\d+(?:\.\d+)?", amount)
        if name and match:
            rows.append((name, float(match.group())))
        if len(rows) == 10:
            break

    if len(rows) != 10:
        raise ValueError(f"Expected 10 valid bank rows, found {len(rows)}")
    return pd.DataFrame(rows, columns=list(table_attribs))


def transform(df: pd.DataFrame, csv_path: str = RATES_URL) -> pd.DataFrame:
    rates = pd.read_csv(StringIO(_read_text(csv_path)))
    rates.columns = rates.columns.str.strip()
    if not {"Currency", "Rate"}.issubset(rates.columns):
        raise ValueError("Exchange rate CSV must contain Currency and Rate columns")
    lookup = dict(zip(rates["Currency"].astype(str).str.strip(), pd.to_numeric(rates["Rate"])))
    result = df.copy()
    result["MC_USD_Billion"] = pd.to_numeric(result["MC_USD_Billion"])
    for currency in ("GBP", "EUR", "INR"):
        if currency not in lookup or pd.isna(lookup[currency]):
            raise ValueError(f"Missing or invalid {currency} exchange rate")
        result[f"MC_{currency}_Billion"] = (result["MC_USD_Billion"] * lookup[currency]).round(2)
    return result


def load_to_csv(df: pd.DataFrame, output_path: str = "Largest_banks_data.csv") -> None:
    df.to_csv(output_path, index=False)


def load_to_db(df: pd.DataFrame, sql_connection: sqlite3.Connection, table_name: str = TABLE_NAME) -> None:
    df.to_sql(table_name, sql_connection, if_exists="replace", index=False)


def run_query(query_statement: str, sql_connection: sqlite3.Connection) -> pd.DataFrame:
    result = pd.read_sql_query(query_statement, sql_connection)
    print(result.to_string(index=False))
    log_progress(f"Query executed: {query_statement}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", default=SOURCE_URL, help="Archived Wikipedia URL or local HTML file")
    parser.add_argument("--rates", default=RATES_URL, help="Course CSV URL or local exchange_rate.csv")
    parser.add_argument("--csv", default="Largest_banks_data.csv", help="Output CSV path")
    parser.add_argument("--db", default="Banks.db", help="Output SQLite database path")
    args = parser.parse_args()

    log_progress("Preliminaries complete. Initiating ETL process")
    banks = extract(args.html)
    log_progress("Data extraction complete. Initiating Transformation process")
    print("Extracted data:")
    print(banks.to_string(index=False))

    banks = transform(banks, args.rates)
    log_progress("Data transformation complete. Initiating Loading process")
    load_to_csv(banks, args.csv)
    log_progress("Data saved to CSV file")

    with sqlite3.connect(args.db) as connection:
        load_to_db(banks, connection, TABLE_NAME)
        log_progress("Data loaded to Database as a table. Running the query")
        run_query(f"SELECT * FROM {TABLE_NAME}", connection)
        run_query(f"SELECT AVG(MC_GBP_Billion) AS avg_gbp_billion FROM {TABLE_NAME}", connection)
        run_query(f"SELECT Name FROM {TABLE_NAME} LIMIT 5", connection)
    log_progress("Process complete")


if __name__ == "__main__":
    main()
