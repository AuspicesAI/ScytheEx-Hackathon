#include "events.h"
#include <stdio.h>
#include <sqlite3.h>

int store_event(Database *database, int agent_id, const char *event_type, const char *event_data)
{
    const char *sql = "INSERT INTO events (agent_id, event_type, event_data) VALUES (?, ?, ?);";
    sqlite3_stmt *stmt;

    if (sqlite3_prepare_v2(database->db, sql, -1, &stmt, NULL) != SQLITE_OK)
    {
        fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(database->db));
        return 1;
    }

    sqlite3_bind_int(stmt, 1, agent_id);
    sqlite3_bind_text(stmt, 2, event_type, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 3, event_data, -1, SQLITE_STATIC);

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