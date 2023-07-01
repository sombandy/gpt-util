import hashlib
import sqlite3

CACHE_TABLE = "full_cache"

class SQLiteCache(object):
    def __init__(self, database_path=".llm.db"):
        self.database_path = database_path
        self.cache_table = "full_cache"
        self.conn = sqlite3.connect(self.database_path)
        self.cur = self.conn.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS {CACHE_TABLE} (
                key TEXT PRIMARY KEY, 
                response TEXT,
                created_at timestamp  NOT NULL  DEFAULT current_timestamp)
            """.format(CACHE_TABLE=CACHE_TABLE)
        )

    def _cache_key(self, messages):
        message_str = ""
        for message in messages:
            message_str += message["role"] + ": " + message["content"] + "\n"

        md5_key = hashlib.md5(message_str.encode("utf-8")).hexdigest()
        return md5_key

    def set(self, messages, response):
        key = self._cache_key(messages)
        insert_stmt = f"""
            INSERT INTO {CACHE_TABLE} (key, response)
            VALUES (?, ?)
        """

        try:
            self.cur.execute(insert_stmt,  (key, response))
            self.conn.commit()
            return True
        except sqlite3.OperationalError as e:
            print("Failed to insert into cache", str(e))
            print(insert_stmt)
            return False

    def get(self, messages):
        key = self._cache_key(messages)
        select_stmt = f"SELECT response FROM {CACHE_TABLE} WHERE key='{key}'"

        res  = self.cur.execute(select_stmt)
        row = res.fetchone()
        if not row:
            return None

        return row[0]