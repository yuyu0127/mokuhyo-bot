import os

import psycopg2
from psycopg2.extras import DictCursor

# __import__('dotenv').load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']


def get_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')


def register_goal(created_at, user_id, content):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO goal (created_at, user_id, content, completed) VALUES (%s, %s, %s, False)', (created_at, user_id, content))
        conn.commit()


def set_completed(user_id, flag):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'UPDATE goal SET completed = %s WHERE user_id = %s AND id = (SELECT max(id) FROM goal)', (flag, user_id))
        conn.commit()


def fetch_goal(user_id):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                'SELECT * FROM goal WHERE user_id = %s AND id = (SELECT max(id) FROM goal)', (user_id, ))
            goal = cur.fetchone()
            return dict(goal)


def fetch_goals():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('''
                SELECT *
                FROM goal AS m
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM goal AS s
                    WHERE m.user_id = s.user_id
                    AND m.id < s.id
                );
            ''')
            goals = []
            for row in cur:
                goals.append(dict(row))
            return goals
