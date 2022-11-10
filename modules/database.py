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
        self.timeout_sec = 1800

    def set_count(self, room: int, count: int):
        time = datetime.datetime.now().timestamp()

        last_count = self.get_count(room)

        conn = sqlite3.connect(self.db_path, isolation_level=None)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS main (room integer, count integer, time integer)")
        if last_count is None:
            # add count
            c.execute("INSERT INTO main (room, count, time) VALUES(?, ?, ?)", (room, count, time))
        else:
            # update count
            print(count, time, room)
            c.execute("UPDATE main SET count = ? WHERE room = ?", (count, room))
            c.execute("UPDATE main SET time = ? WHERE room = ?", (time, room))
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

        # 저장된 데이터 갱신 실패가 30분 이상 경과했을 경우 timeout 반환
        if count is not None:
            if int(count[2]) + self.timeout_sec < datetime.datetime.now().timestamp():
                return "timeout"
        return count

    def get_all_rooms(self):
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM main")
        except sqlite3.OperationalError:
            conn.close()
            return None
        rooms = c.fetchall()
        conn.close()

        # timeout 판별을 위해 list로 변환
        result = []
        for i in rooms:
            result.append([i[0], i[1], i[2]])

        for room in enumerate(result):
            # 저장된 데이터 갱신 실패가 30분 이상 경과했을 경우 시간 timeout 처리
            if int(room[1][2]) + self.timeout_sec < datetime.datetime.now().timestamp():
                result[room[0]][1] = "timeout"
                result[room[0]][2] = "timeout"
        return result