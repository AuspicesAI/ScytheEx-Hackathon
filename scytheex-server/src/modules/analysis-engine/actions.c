#include <stdio.h>
#include <stdlib.h>
#include "actions.h"

// Block IP using real firewall commands (for Linux, iptables)
void block_ip(const char *ip_address)
{
    char command[256];
    snprintf(command, sizeof(command), "sudo iptables -A INPUT -s %s -j DROP", ip_address);
    int result = system(command);
    if (result == 0)
    {
        printf("IP blocked successfully: %s\n", ip_address);
    }
    else
    {
        printf("Failed to block IP: %s\n", ip_address);
    }
}

// Trigger an alert (you can integrate with external alerting systems)
void trigger_alert(const char *alert_message)
{
    // Integrate with an enterprise alerting system like Slack, PagerDuty, etc.
    printf("ALERT: %s\n", alert_message);
}