#ifndef RULE_ENGINE_H
#define RULE_ENGINE_H

#include "decoders.h"
#include "rules-loader.h"

void apply_detection_rules(DecodedLog *decoded_log);

#endif // RULE_ENGINE_H