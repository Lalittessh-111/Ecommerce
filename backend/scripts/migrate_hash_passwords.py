"""One-time migration: replace plain-text passwords with bcrypt hashes.

Run once after deploying this version, before users log in:
    python scripts/migrate_hash_passwords.py

Safe to run more than once (rows that are already hashed are skipped).
Make sure the password column can hold 60+ characters first, e.g.:
    ALTER TABLE user_details MODIFY password VARCHAR(255) NOT NULL;
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import connect_db  # noqa: E402
from security import hash_password, is_bcrypt_hash  # noqa: E402


def main():
    conn = connect_db()
    updated = 0
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT userid, password FROM user_details")
            for row in cursor.fetchall():
                if row["password"] and not is_bcrypt_hash(row["password"]):
                    cursor.execute(
                        "UPDATE user_details SET password = %s WHERE userid = %s",
                        (hash_password(row["password"]), row["userid"]),
                    )
                    updated += 1
        conn.commit()
    finally:
        conn.close()
    print(f"Hashed {updated} plain-text password(s).")


if __name__ == "__main__":
    main()
