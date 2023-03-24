import mysql.connector

db = mysql.connector.connect(
  user='root',
  password='root',
  host='localhost',
  database='rognellabot',
  raise_on_warnings=True,
)
cur = db.cursor()
"""
cur = DB.cursor()
cur.execute("SELECT * FROM badword")
for i in cur:
  print(i)
cur.close()
"""


class db_CON_BadWord:
  def INSERT(user_id: int, first_name: str, last_name: str, stat: int):
    cur.execute("INSERT INTO badword(user_id, first_name, last_name, stat) VALUES (%s, %s, %s, %s)",
                (user_id, first_name, last_name, stat))
    db.commit()


  def UPDATE(stat: int, user_id):
    cur.execute("UPDATE BadWord SET stat = %s WHERE user_id = %s", (user_id, stat))
    db.commit()


class db_CON_WORD:
  def INSERT(word_text: str):
    cur.execute("INSERT INTO words(word_text) VALUES (%s)", (word_text,))
    db.commit()



