#ifndef EVENTS_H
#define EVENTS_H

#include "db.h"

int store_event(Database *database, int agent_id, const char *event_type, const char *event_data);

#endif // EVENTS_H