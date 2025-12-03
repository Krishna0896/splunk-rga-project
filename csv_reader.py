# csv_reader.py
import pandas as pd




def read_csv_logs(path: str, message_column: str = "message", limit: int = 500):
df = pd.read_csv(path)
if message_column not in df.columns:
# fallback: join all columns
texts = df.astype(str).agg(' | '.join, axis=1).tolist()
else:
texts = df[message_column].astype(str).tolist()


return texts[:limit]




def read_excel_logs(path: str, sheet_name: str = 0, message_column: str = "message", limit: int = 500):
df = pd.read_excel(path, sheet_name=sheet_name)
if message_column not in df.columns:
texts = df.astype(str).agg(' | '.join, axis=1).tolist()
else:
texts = df[message_column].astype(str).tolist()


return texts[:limit]
