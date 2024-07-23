#include "elasticsearch_client.h"
#include <curl/curl.h>

void send_to_elasticsearch(json_object *log_entry)
{
    CURL *curl;
    CURLcode res;

    curl = curl_easy_init();
    if (curl)
    {
        curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:9200/scytheex/logs");
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_object_to_json_string(log_entry));

        res = curl_easy_perform(curl);
        if (res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));

        curl_easy_cleanup(curl);
    }
}
