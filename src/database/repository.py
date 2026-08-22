import os
import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = os.getenv("CANIND_DB_PATH", "data/canind.sqlite3")

def get_connection():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = get_connection()
    con.executescript("""
    CREATE TABLE IF NOT EXISTS observations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        indicator_id TEXT NOT NULL,
        reference_period TEXT NOT NULL,
        release_date TEXT,
        value REAL NOT NULL,
        unit TEXT,
        source TEXT,
        vintage_id TEXT,
        retrieved_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(indicator_id, reference_period, vintage_id)
    );
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        calculated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        recession_risk REAL,
        transition_score REAL,
        momentum_score REAL,
        breadth_score REAL
    );
    """)
    con.commit()
    con.close()

def upsert_observations(rows):
    if not rows:
        return
    con = get_connection()
    con.executemany("""
      INSERT OR REPLACE INTO observations
      (indicator_id, reference_period, release_date, value, unit, source, vintage_id)
      VALUES (:indicator_id, :reference_period, :release_date, :value, :unit, :source, :vintage_id)
    """, rows)
    con.commit()
    con.close()

def read_observations():
    con = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM observations ORDER BY reference_period, indicator_id", con
    )
    con.close()
    return df

def save_scores(scores):
    con = get_connection()
    con.execute("""
      INSERT INTO scores (recession_risk, transition_score, momentum_score, breadth_score)
      VALUES (?, ?, ?, ?)
    """, (
        scores.get("recession_risk"),
        scores.get("transition_score"),
        scores.get("momentum_score"),
        scores.get("breadth_score"),
    ))
    con.commit()
    con.close()

def read_scores(limit=100):
    con = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM scores ORDER BY calculated_at DESC LIMIT ?", con, params=(limit,)
    )
    con.close()
    return df
