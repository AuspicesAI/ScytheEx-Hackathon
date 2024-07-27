#ifndef ELASTICSEARCH_CLIENT_H
#define ELASTICSEARCH_CLIENT_H

#include <json-c/json.h>

void send_to_elasticsearch(json_object *log_entry);

#endif // ELASTICSEARCH_CLIENT_H
