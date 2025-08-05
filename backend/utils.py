from db import connect_db

def is_admin(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM user_details WHERE userid = %s", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result and result['role'] == 'admin'
