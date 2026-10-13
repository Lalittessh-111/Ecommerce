"""Promote an existing user to admin (run by the site owner on the server).

Usage:  python scripts/make_admin.py someone@example.com
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import connect_db  # noqa: E402


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python scripts/make_admin.py <email>")
    email = sys.argv[1].strip().lower()
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            changed = cursor.execute(
                "UPDATE user_details SET role = 'admin' WHERE email_id = %s", (email,)
            )
        conn.commit()
    finally:
        conn.close()
    print(f"{email} is now an admin." if changed else f"No user found with email {email}.")


if __name__ == "__main__":
    main()
