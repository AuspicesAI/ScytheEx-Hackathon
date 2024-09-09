#ifndef RULES_LOADER_H
#define RULES_LOADER_H

// Define the structure for a Rule
typedef struct
{
    int id;                // Rule ID
    int level;             // Rule severity level
    char match[256];       // Pattern to match in logs
    char description[512]; // Description of the rule
    char mitre_id[100];    // MITRE ATT&CK ID
    char group[256];       // Compliance group
} Rule;

// Define the structure for each rule node (linked list)
typedef struct RuleNode
{
    Rule *rule;
    struct RuleNode *next;
} RuleNode;

extern RuleNode *rule_list_head; // Linked list head containing loaded rules
extern int rule_count;

// Function declarations
void replace_variables(char *pattern, const char *var_name, const char *var_value);
int load_rules_from_directory(const char *directory);

// Functions to manage the linked list of rules
void print_loaded_rules(); // For debugging
void free_rules();         // To free all dynamically allocated rules

#endif // RULES_LOADER_H