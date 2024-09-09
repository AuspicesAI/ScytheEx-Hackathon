#include <stdio.h>
#include <string.h>
#include "rule-engine.h"
#include "rules-loader.h"

// Externally declared linked list head from rules-loader.c
extern RuleNode *rule_list_head; // Linked list head containing the loaded rules

// Function to apply detection rules to a decoded log
void apply_detection_rules(DecodedLog *decoded_log)
{
    RuleNode *current = rule_list_head;
    while (current != NULL)
    {
        Rule *rule = current->rule;

        // Check if the decoded log data matches the rule's match pattern
        if (strstr(decoded_log->event_data, rule->match))
        {
            printf("Rule Matched: %s\n", rule->description);

            // Trigger an alert if the rule level is above a certain threshold (e.g., 8)
            if (rule->level >= 8)
            {
                trigger_alert(rule->description);
            }
        }

        current = current->next; // Move to the next rule in the list
    }
}