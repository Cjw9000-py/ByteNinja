#pragma once
#include "stdlib.h"
#include "assert.h"

static size_t call_count = 0;

// memory debugging utilities
#ifdef DEBUG_MEMORY
// wrappers that check the allocation count

inline void* malloc_s(size_t size) {
    assert(size != 0, "malloc called with 0 size");

    call_count++;
    return malloc(size);
}

inline void* realloc_s(void* ptr, size_t size) {
    if (size == 0) {
        call_count--;
    }
    return realloc_s(ptr, size);
}

inline void free_s(void* ptr) {
    call_count--;
    free(ptr);
}

#else
// simple wrappers that will be optimized away


inline void* malloc_s(size_t size) {
    return malloc(size);
}

inline void* realloc_s(void* ptr, size_t size) {
    return realloc_s(ptr, size);
}

inline void free_s(void* ptr) {
    free(ptr);
}

#endif

// used by testing
inline size_t check_cleanup() {
    return call_count;
}
