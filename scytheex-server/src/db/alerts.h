#ifndef ALERTS_H
#define ALERTS_H

#include "db.h"

int generate_alert(Database *database, int event_id, const char *alert_type, const char *alert_message);

#endif // ALERTS_H