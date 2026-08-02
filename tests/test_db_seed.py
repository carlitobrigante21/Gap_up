import sqlite3
import unittest

import db


class DatabaseSeedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.build_database(force=True)

    def test_tiered_roles_and_skill_mappings_exist(self):
        conn = db.get_connection()
        try:
            cur = conn.cursor()

            cur.execute("SELECT name FROM roles WHERE name = ?", ("Network Engineer",))
            self.assertIsNone(cur.fetchone())

            levels = {
                "Junior": "Network Engineer - Junior",
                "Middle": "Network Engineer - Middle",
                "Senior": "Network Engineer - Senior",
            }

            counts = {}
            for level, role_name in levels.items():
                cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM role_skills rs
                    JOIN roles r ON r.id = rs.role_id
                    WHERE r.name = ?
                    """,
                    (role_name,),
                )
                counts[level] = cur.fetchone()[0]

            self.assertGreater(counts["Junior"], 0)
            self.assertGreater(counts["Middle"], 0)
            self.assertGreater(counts["Senior"], 0)
            self.assertLess(counts["Junior"], counts["Middle"])
            self.assertLess(counts["Middle"], counts["Senior"])
        finally:
            conn.close()

    def test_rebuild_preserves_existing_roles(self):
        conn = sqlite3.connect(db.DB_PATH)
        try:
            conn.execute("INSERT OR IGNORE INTO roles (name) VALUES (?)", ("Preserved Custom Role",))
            conn.commit()
        finally:
            conn.close()

        db.build_database(force=False)

        conn = db.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT name FROM roles WHERE name = ?", ("Preserved Custom Role",))
            self.assertIsNotNone(cur.fetchone())
            cur.execute("SELECT name FROM roles WHERE name = ?", ("Frontend Developer",))
            self.assertIsNone(cur.fetchone())
            cur.execute("SELECT name FROM roles WHERE name = ?", ("Frontend Developer - Senior",))
            self.assertIsNotNone(cur.fetchone())
        finally:
            conn.close()


if __name__ == "__main__":
    unittest.main()
