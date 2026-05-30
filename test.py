from dotenv import load_dotenv
import os
load_dotenv()

db_path = os.environ['DB_FOLDER']
print(db_path)