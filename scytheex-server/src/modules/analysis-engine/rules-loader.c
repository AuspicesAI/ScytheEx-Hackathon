#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include "rules-loader.h"
#include <libxml/parser.h>

#define MAX_MATCH_LEN 256
#define MAX_DESC_LEN 512
#define MAX_MITRE_ID_LEN 100
#define MAX_GROUP_LEN 256

int rule_count = 0;

RuleNode *rule_list_head = NULL;

// Helper to replace variables in rule patterns (like $BAD_WORDS)
void replace_variables(char *pattern, const char *var_name, const char *var_value)
{
    char buffer[MAX_MATCH_LEN];
    char *pos = strstr(pattern, var_name);
    if (pos != NULL)
    {
        snprintf(buffer, sizeof(buffer), "%.*s%s%s", (int)(pos - pattern), pattern, var_value, pos + strlen(var_name));
        strncpy(pattern, buffer, MAX_MATCH_LEN - 1);
        pattern[MAX_MATCH_LEN - 1] = '\0'; // Ensure null-termination
    }
}

// Function to parse and load each rule from an XML node
static Rule *parse_rule_node(xmlNode *node)
{
    Rule *rule = malloc(sizeof(Rule));
    if (!rule)
    {
        printf("Memory allocation failed for rule.\n");
        return NULL;
    }

    xmlChar *id = xmlGetProp(node, (const xmlChar *)"id");
    rule->id = atoi((const char *)id);
    xmlFree(id);

    xmlChar *level = xmlGetProp(node, (const xmlChar *)"level");
    rule->level = atoi((const char *)level);
    xmlFree(level);

    // Loop through the children nodes to parse details (match, description, mitre, group)
    for (xmlNode *cur_node = node->children; cur_node; cur_node = cur_node->next)
    {
        if (cur_node->type == XML_ELEMENT_NODE)
        {
            if (strcmp((const char *)cur_node->name, "match") == 0)
            {
                xmlChar *match = xmlNodeGetContent(cur_node);
                strncpy(rule->match, (const char *)match, MAX_MATCH_LEN - 1);
                rule->match[MAX_MATCH_LEN - 1] = '\0';
                xmlFree(match);
            }
            else if (strcmp((const char *)cur_node->name, "description") == 0)
            {
                xmlChar *description = xmlNodeGetContent(cur_node);
                strncpy(rule->description, (const char *)description, MAX_DESC_LEN - 1);
                rule->description[MAX_DESC_LEN - 1] = '\0';
                xmlFree(description);
            }
            else if (strcmp((const char *)cur_node->name, "mitre") == 0)
            {
                xmlNode *mitre_id_node = cur_node->children;
                if (mitre_id_node && strcmp((const char *)mitre_id_node->name, "id") == 0)
                {
                    xmlChar *mitre_id = xmlNodeGetContent(mitre_id_node);
                    strncpy(rule->mitre_id, (const char *)mitre_id, MAX_MITRE_ID_LEN - 1);
                    rule->mitre_id[MAX_MITRE_ID_LEN - 1] = '\0';
                    xmlFree(mitre_id);
                }
            }
            else if (strcmp((const char *)cur_node->name, "group") == 0)
            {
                xmlChar *group = xmlNodeGetContent(cur_node);
                strncpy(rule->group, (const char *)group, MAX_GROUP_LEN - 1);
                rule->group[MAX_GROUP_LEN - 1] = '\0';
                xmlFree(group);
            }
        }
    }

    // printf("Parsed Rule ID: %d, Level: %d\n", rule->id, rule->level); // DEBUG - Print the parsed rule

    // Handle variable replacement like $BAD_WORDS
    replace_variables(rule->match, "$BAD_WORDS", "core_dumped|failure|error|attack| bad |illegal |denied|refused|unauthorized|fatal|failed|Segmentation Fault|Corrupted");

    return rule;
}

// Add a rule to the linked list
static void add_rule_to_list(Rule *rule)
{
    RuleNode *new_node = malloc(sizeof(RuleNode));
    if (!new_node)
    {
        printf("Memory allocation failed for RuleNode.\n");
        free(rule);
        return;
    }
    new_node->rule = rule;
    new_node->next = NULL;

    if (rule_list_head == NULL)
    {
        rule_list_head = new_node;
    }
    else
    {
        RuleNode *current = rule_list_head;
        while (current->next != NULL)
        {
            current = current->next;
        }
        current->next = new_node;
    }

    rule_count++; // Increment the rule count
}

// Function to parse and load each group of rules from an XML node
static void parse_group_node(xmlNode *group_node)
{
    for (xmlNode *cur_node = group_node->children; cur_node; cur_node = cur_node->next)
    {
        if (cur_node->type == XML_ELEMENT_NODE && strcmp((const char *)cur_node->name, "rule") == 0)
        {
            Rule *rule = parse_rule_node(cur_node);
            if (rule)
            {
                add_rule_to_list(rule);
            }
        }
    }
}

// Load a single XML rule file
static int load_xml_rule_file(const char *filename)
{
    xmlDoc *document = xmlReadFile(filename, NULL, 0);
    if (document == NULL)
    {
        printf("Failed to parse XML file: %s\n", filename);
        return EXIT_FAILURE;
    }

    xmlNode *root_element = xmlDocGetRootElement(document);
    if (root_element && strcmp((const char *)root_element->name, "ruleset") == 0)
    {
        // Handle multiple groups in a ruleset
        for (xmlNode *cur_node = root_element->children; cur_node; cur_node = cur_node->next)
        {
            if (cur_node->type == XML_ELEMENT_NODE && strcmp((const char *)cur_node->name, "group") == 0)
            {
                parse_group_node(cur_node);
            }
        }
    }
    else if (strcmp((const char *)root_element->name, "group") == 0)
    {
        // Handle a single group in the XML file
        parse_group_node(root_element);
    }
    else
    {
        printf("Unknown root element in file: %s\n", filename);
        xmlFreeDoc(document);
        return EXIT_FAILURE;
    }

    xmlFreeDoc(document);
    return EXIT_SUCCESS;
}

// Load all XML rule files from a directory
int load_rules_from_directory(const char *directory)
{
    DIR *dir = opendir(directory);
    if (!dir)
    {
        perror("Failed to open rules directory");
        return EXIT_FAILURE;
    }

    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL)
    {
        if (entry->d_name[0] == '.')
        {
            // Skip hidden files and parent directories (e.g., . and ..)
            continue;
        }

        char filepath[1024];
        snprintf(filepath, sizeof(filepath), "%s/%s", directory, entry->d_name);

        // Use stat to check if it is a regular file
        struct stat file_stat;
        if (stat(filepath, &file_stat) == 0 && S_ISREG(file_stat.st_mode))
        {
            printf("Loading rule file: %s\n", filepath);
            if (load_xml_rule_file(filepath) != EXIT_SUCCESS)
            {
                printf("Failed to load rules from file: %s\n", filepath);
            }
        }
    }

    closedir(dir);
    // printf("Loaded %d rules from directory\n", rule_count); // DEBUG

    return EXIT_SUCCESS;
}

// Free all allocated rules
void free_rules()
{
    RuleNode *current = rule_list_head;
    while (current)
    {
        RuleNode *temp = current;
        current = current->next;
        free(temp->rule); // Free the rule
        free(temp);       // Free the node
    }
    rule_list_head = NULL;
}