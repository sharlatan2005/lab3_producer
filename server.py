import lections_pb2
import lections_pb2_grpc
import sqlite3
from typing import Iterator
from config import SQLITE_PATH, SQLITE_TABLE_NAME

class LectionsServicer(lections_pb2_grpc.LectionsServiceServicer):
    def GetLectionAttendance(self, request, context):
        conn = sqlite3.connect(SQLITE_PATH)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT * FROM {SQLITE_TABLE_NAME}")
        
        for row in cursor:
            yield lections_pb2.LectionAttendance(
                id=int(row[0]),
                student_id=int(row[1]),
                student_full_name=row[2],
                faculty_id=int(row[3]),
                faculty_name=row[4],
                group_id=int(row[5]),
                group_name=row[6],
                lection_id=int(row[7]),  # Преобразуем строку в int
                subject_id=int(row[8]),
                subject_name=row[9],
                teacher_id=int(row[10]),
                teacher_full_name=row[11],
                start_timestamp=row[12],
                end_timestamp=row[13]
            )
        
        conn.close()
        
        conn.close()