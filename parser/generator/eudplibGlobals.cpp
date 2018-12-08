#include <unordered_set>
#include "eudplibGlobals.h"
#include <iostream>

std::unordered_set<std::string> builtinConstSet = {
        "onPluginStart", "beforeTriggerExec", "afterTriggerExec",
        "f_dwread", "SetTo", "EUDArray", "EUDByteReader", "f_dwread_epd"
};

bool isBuiltinConst(std::string& name) {
    if(name == "True" || name == "true") {
        name = "True";
        return true;
    }

    else if(name == "False" || name == "false") {
        name = "False";
        return true;
    }
    else if (name == "None") return true;

    else {
        return builtinConstSet.find(name) != builtinConstSet.end();
    }
}
