CC = gcc
CFLAGS = -Wall -Iinclude
LDFLAGS = -lpfring -ljson-c -lcurl -lpcap

SRC = src/capture/packet_capture.c src/utils/logger.c src/main.c
OBJ = $(SRC:.c=.o)
EXEC = scytheex-agent

all: $(EXEC)

$(EXEC): $(OBJ)
	$(CC) $(OBJ) -o $(EXEC) $(LDFLAGS)

src/%.o: src/%.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(EXEC)

.PHONY: clean
