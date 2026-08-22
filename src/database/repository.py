import os, sqlite3
from pathlib import Path
import pandas as pd
DB_PATH=os.getenv('CANIND_DB_PATH','data/canind.sqlite3')
def get_connection():
 Path(DB_PATH).parent.mkdir(parents=True,exist_ok=True); c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; return c
def init_db():
 c=get_connection(); c.executescript('''
 CREATE TABLE IF NOT EXISTS observations (id INTEGER PRIMARY KEY AUTOINCREMENT, indicator_id TEXT NOT NULL, reference_period TEXT NOT NULL, release_date TEXT, value REAL NOT NULL, unit TEXT, source TEXT, vintage_id TEXT, data_status TEXT DEFAULT 'LIVE', source_url TEXT, retrieved_at TEXT DEFAULT CURRENT_TIMESTAMP, UNIQUE(indicator_id,reference_period,vintage_id));
 CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY AUTOINCREMENT, calculated_at TEXT DEFAULT CURRENT_TIMESTAMP,recession_risk REAL,transition_score REAL,momentum_score REAL,breadth_score REAL);
 ''')
 for col,typ in [('data_status','TEXT'),('source_url','TEXT')]:
  try:c.execute(f'ALTER TABLE observations ADD COLUMN {col} {typ}')
  except sqlite3.OperationalError:pass
 c.commit();c.close()
def upsert_observations(rows):
 if not rows:return
 for r in rows:r.setdefault('data_status','LIVE');r.setdefault('source_url','')
 c=get_connection();c.executemany('''INSERT OR REPLACE INTO observations(indicator_id,reference_period,release_date,value,unit,source,vintage_id,data_status,source_url) VALUES (:indicator_id,:reference_period,:release_date,:value,:unit,:source,:vintage_id,:data_status,:source_url)''',rows);c.commit();c.close()
def read_observations():
 c=get_connection();df=pd.read_sql_query('SELECT * FROM observations ORDER BY reference_period,indicator_id',c);c.close();return df
def save_scores(scores):
 c=get_connection();c.execute('INSERT INTO scores(recession_risk,transition_score,momentum_score,breadth_score) VALUES(?,?,?,?)',(scores.get('recession_risk'),scores.get('transition_score'),scores.get('momentum_score'),scores.get('breadth_score')));c.commit();c.close()
def read_scores(limit=100):
 c=get_connection();df=pd.read_sql_query('SELECT * FROM scores ORDER BY calculated_at DESC LIMIT ?',c,params=(limit,));c.close();return df
