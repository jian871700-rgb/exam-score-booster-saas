"""
中高考卷面提分 SaaS - 数据库持久化模块 (database.py)
负责：学员档案与诊断报告的自动落盘、检索、删除与统计
"""

import sqlite3
import os
from datetime import datetime

# 数据库文件路径（会自动在项目根目录生成 student_records.db）
DB_PATH = os.path.join(os.path.dirname(__file__), "student_records.db")

def get_db_connection():
    """建立数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 允许以字典方式访问字段（如 row['student_name']）
    return conn

def init_db():
    """初始化数据库表结构"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 创建学员诊断档案表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT NOT NULL,
        grade TEXT NOT NULL,
        subject TEXT NOT NULL,
        score_gap TEXT,
        issue_desc TEXT,
        report_content TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

def save_report(student_name: str, grade: str, subject: str, score_gap: str, issue_desc: str, report_content: str):
    """保存一份新的学员诊断报告"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
    INSERT INTO student_reports (student_name, grade, subject, score_gap, issue_desc, report_content, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (student_name, grade, subject, score_gap, issue_desc, report_content, now_str))
    
    conn.commit()
    report_id = cursor.lastrowid
    conn.close()
    return report_id

def get_all_reports(search_query: str = None):
    """获取所有学员报告（支持按姓名或科目搜索）"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if search_query:
        cursor.execute("""
        SELECT * FROM student_reports 
        WHERE student_name LIKE ? OR subject LIKE ? OR grade LIKE ?
        ORDER BY id DESC
        """, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
    else:
        cursor.execute("SELECT * FROM student_reports ORDER BY id DESC")
        
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_report(report_id: int):
    """按 ID 删除某条学员记录"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student_reports WHERE id = ?", (report_id,))
    conn.commit()
    conn.close()

# 如果直接运行此脚本，测试初始化与写入
if __name__ == "__main__":
    init_db()
    print("✅ 数据库初始化成功！已建立 student_reports 表。")
git add .
git commit -m "Add database.py and upgrade to v5.0 Pro"
git push
