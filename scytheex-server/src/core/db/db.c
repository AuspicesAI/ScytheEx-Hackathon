#include "db.h"
#include <stdio.h>

int open_database(const char *filename, Database *database) {
    int rc = sqlite3_open(filename, &database->db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(database->db));
        return rc;
    }
    return SQLITE_OK;
}

void close_database(Database *database) {
    if (database->db) {
        sqlite3_close(database->db);
    }
}