#include <stdio.h>
#include <stdlib.h>
#include "db.h"

void setup_database(Database *database)
{
    const char *sql = "CREATE TABLE IF NOT EXISTS agents ("
                      "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                      "name TEXT NOT NULL, "
                      "ip_address TEXT NOT NULL, "
                      "last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                      "status TEXT DEFAULT 'active');"
                      "CREATE TABLE IF NOT EXISTS events ("
                      "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                      "agent_id INTEGER REFERENCES agents(id) ON DELETE CASCADE, "
                      "event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                      "event_type TEXT, "
                      "event_data TEXT);"
                      "CREATE TABLE IF NOT EXISTS alerts ("
                      "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                      "event_id INTEGER REFERENCES events(id) ON DELETE CASCADE, "
                      "alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                      "alert_type TEXT, "
                      "alert_message TEXT, "
                      "resolved BOOLEAN DEFAULT FALSE);"
                      "CREATE TABLE IF NOT EXISTS configurations ("
                      "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                      "key TEXT UNIQUE NOT NULL, "
                      "value TEXT NOT NULL);";

    char *err_msg = 0;
    int rc = sqlite3_exec(database->db, sql, 0, 0, &err_msg);
    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Failed to execute SQL: %s\n", err_msg);
        sqlite3_free(err_msg);
    }
}