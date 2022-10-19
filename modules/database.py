"""
DB 구조
main
    - room
    - count
    - time
"""

import sqlite3
import datetime

class Database():
    def __init__(self):
        self.db_path = "database.db"
    
    def set_count(self, room: int, count: int):
        time = datetime.datetime.now().timestamp()

        last_count = self.get_count(room)

        conn = sqlite3.connect(self.db_path, isolation_level=None)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS main (room integer, count integer, time int)")
        if last_count is None:
            # add count
            c.execute("INSERT INTO main (room, count, time) VALUES(?, ?, ?)", (room, count, time))
        else:
            # update count
            c.execute("UPDATE main SET count = ? AND time = ? WHERE room = ?", (count, time, room))
        conn.close()
    
    def get_count(self, room: int):
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM main WHERE room = ?", (room,))
        except sqlite3.OperationalError:
            conn.close()
            return None
        count = c.fetchone()
        conn.close()

        # 저장된 데이터 갱신 실패가 30분 이상 경과했을 경우 None 반환
        if count is not None:
            if int(count[2]) + 1800 < datetime.datetime.now().timestamp():
                return "timeout"
        return count