from sqlalchemy import text
from core.database import Database

db = Database.get_session()

result = db.execute(text("SELECT * from pessoa"))
print(result.scalar())

db.close()
