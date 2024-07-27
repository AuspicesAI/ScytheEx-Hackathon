#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>
#include "analysisd.h"
#include "config.h"
#include "logging.h"
#include "db.h"
#include "events.h"
#include "alerts.h"

#define BUFFER_SIZE 1024

void *handle_client(void *arg);
static Database db;
static FILE *log_file;

void start_server(const Config *config)
{
    int server_fd, new_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);

    // Initialize logging
    init_logging(config->logfile, LOG_INFO);
    log_message(LOG_INFO, "Server starting on port %d", config->port);

    // Initialize database
    if (open_database("scytheex.db", &db) != SQLITE_OK)
    {
        log_message(LOG_ERROR, "Failed to open database");
        exit(EXIT_FAILURE);
    }

    setup_database(&db);

    // Open log file for writing received data
    log_file = fopen("/var/log/scytheex/agent_data.log", "a");
    if (log_file == NULL)
    {
        log_message(LOG_ERROR, "Failed to open log file");
        close_database(&db);
        exit(EXIT_FAILURE);
    }

    // Create socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    {
        log_message(LOG_ERROR, "socket failed");
        fclose(log_file);
        close_database(&db);
        exit(EXIT_FAILURE);
    }

    // Bind socket to port
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(config->port);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
    {
        log_message(LOG_ERROR, "bind failed");
        close(server_fd);
        fclose(log_file);
        close_database(&db);
        exit(EXIT_FAILURE);
    }

    // Listen for connections
    if (listen(server_fd, 3) < 0)
    {
        log_message(LOG_ERROR, "listen failed");
        close(server_fd);
        fclose(log_file);
        close_database(&db);
        exit(EXIT_FAILURE);
    }

    log_message(LOG_INFO, "Server listening on port %d", config->port);

    while (1)
    {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0)
        {
            log_message(LOG_ERROR, "accept failed");
            close(server_fd);
            fclose(log_file);
            close_database(&db);
            exit(EXIT_FAILURE);
        }

        // Create a thread to handle the client
        pthread_t thread_id;
        int *client_sock = malloc(sizeof(int));
        *client_sock = new_socket;

        if (pthread_create(&thread_id, NULL, handle_client, (void *)client_sock) != 0)
        {
            log_message(LOG_ERROR, "pthread_create failed");
        }

        pthread_detach(thread_id); // Automatically reclaim resources when thread finishes
    }

    close_database(&db);
    close_logging();
    fclose(log_file);
}

void *handle_client(void *arg)
{
    int socket = *(int *)arg;
    char buffer[BUFFER_SIZE] = {0};
    int bytes_read;

    while ((bytes_read = read(socket, buffer, BUFFER_SIZE)) > 0)
    {
        log_message(LOG_INFO, "Received data: %s", buffer);

        // Analyze the received event
        analyze_event(&db, buffer);

        // Write the received data to the log file
        fprintf(log_file, "%s\n", buffer);
        fflush(log_file); // Ensure data is written to the file immediately

        // Send response to client
        send(socket, "Acknowledged", strlen("Acknowledged"), 0);
        memset(buffer, 0, BUFFER_SIZE);
    }

    if (bytes_read == 0)
    {
        log_message(LOG_INFO, "Client disconnected");
    }
    else
    {
        log_message(LOG_ERROR, "recv failed");
    }

    close(socket);
    free(arg);
    return NULL;
}