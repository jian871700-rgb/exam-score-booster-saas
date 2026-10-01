import sqlite3
from datetime import datetime

DB_NAME = "student_records.db"

def init_db():
    """初始化数据库表结构"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            grade TEXT NOT NULL,
            subject TEXT NOT NULL,
            score_gap TEXT,
            issue_desc TEXT,
            report_content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_report(student_name, grade, subject, score_gap, issue_desc, report_content):
    """保存生成的诊断报告"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO student_reports (student_name, grade, subject, score_gap, issue_desc, report_content, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        student_name, 
        grade, 
        subject, 
        score_gap, 
        issue_desc, 
        report_content, 
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

def get_all_reports(keyword=""):
    """获取所有诊断报告，支持按姓名模糊搜索"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if keyword.strip():
        cursor.execute("""
            SELECT id, student_name, grade, subject, score_gap, issue_desc, report_content, created_at
            FROM student_reports
            WHERE student_name LIKE ?
            ORDER BY id DESC
        """, (f"%{keyword.strip()}%",))
    else:
        cursor.execute("""
            SELECT id, student_name, grade, subject, score_gap, issue_desc, report_content, created_at
            FROM student_reports
            ORDER BY id DESC
        """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_report(report_id):
    """删除指定报告"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student_reports WHERE id = ?", (report_id,))
    conn.commit()
    conn.close()
