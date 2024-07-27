#include "alerts.h"
#include <stdio.h>
#include <sqlite3.h>

int generate_alert(Database *database, int event_id, const char *alert_type, const char *alert_message)
{
    const char *sql = "INSERT INTO alerts (event_id, alert_type, alert_message) VALUES (?, ?, ?);";
    sqlite3_stmt *stmt;

    if (sqlite3_prepare_v2(database->db, sql, -1, &stmt, NULL) != SQLITE_OK)
    {
        fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(database->db));
        return 1;
    }

    sqlite3_bind_int(stmt, 1, event_id);
    sqlite3_bind_text(stmt, 2, alert_type, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 3, alert_message, -1, SQLITE_STATIC);

    int rc = sqlite3_step(stmt);
    if (rc != SQLITE_DONE)
    {
        fprintf(stderr, "Failed to execute statement: %s\n", sqlite3_errmsg(database->db));
        sqlite3_finalize(stmt);
        return 1;
    }

    sqlite3_finalize(stmt);
    return 0;
}