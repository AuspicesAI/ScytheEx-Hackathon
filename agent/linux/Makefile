# Compiler
CC = gcc
CFLAGS = -Wall -Iinclude

# Source files and object files
SRCS = src/main.c src/agent/agent.c src/logging/logger.c src/utils/config_manager.c
OBJS = $(SRCS:.c=.o)

# Target executable
TARGET = scytheex-agent

# Default rule
all: $(TARGET)

# Link the target executable
$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $(TARGET) -lpfring -ljson-c -lcurl -lpcap -lyaml

# Compile .c files to .o files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Clean up build artifacts
clean:
	rm -f $(OBJS) $(TARGET)
