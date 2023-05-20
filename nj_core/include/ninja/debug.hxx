#include <stdio.h>
#include "ninja/config.hxx"

#define VERBOSE

#ifdef VERBOSE
#define INFO(msg) printf("%s", #msg);
#else
#define INFO(msg) 
#endif 