#include <stdio.h>
#include "ninja/config.h"

#define VERBOSE

#ifdef VERBOSE
#define INFO(msg) printf("%s", #msg);
#else
#define INFO(msg) 
#endif 