CC = gcc
CFLAGS = -Wall -Wextra -pthread
TARGET = scytheex-server
SRCS = main.c server/server.c analysisd/analysisd.c config/config.c config/ini.c logging/logging.c db/db.c db/setup_db.c db/events.c db/alerts.c

all: $(TARGET)

$(TARGET): $(SRCS)
    $(CC) $(CFLAGS) -o $(TARGET) $(SRCS)

clean:
    rm -f $(TARGET)