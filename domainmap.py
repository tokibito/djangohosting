import os
import sqlite3

def registered_domain(settings, domain):
    admin_db = os.path.join(os.path.abspath(settings.hosting.project_dir), '_admin/hosting/hosting.db')
    conn = sqlite3.connect(admin_db)
    try:
        try:
            rows = list(conn.execute('SELECT domain,project_name FROM domain_map WHERE domain="%s"' % domain))
            return rows[0][1]
        except:
            return
    finally:
        conn.close()
