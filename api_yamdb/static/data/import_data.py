import pandas as pd
import sqlite3
import datetime

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
df = pd.read_csv('users.csv')

df['password'] = ""
df['is_superuser'] = 0
df['first_name'] = ""
df['last_name'] = ""
df['is_staff'] = 0
df['is_active'] = 0
df['date_joined'] = datetime.date.today()
df['bio'] = ""
df['confirmation_code'] = '000000'

df.to_sql('users_user', conn, if_exists='append', index=False)
