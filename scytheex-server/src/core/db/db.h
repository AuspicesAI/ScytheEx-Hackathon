#ifndef DB_H
#define DB_H

#include <sqlite3.h> // sudo apt install libsqlite3-dev

typedef struct
{
    sqlite3 *db;
} Database;

int open_database(const char *filename, Database *database);
void close_database(Database *database);
void setup_database(Database *database);

#endif // DB_H