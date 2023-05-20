#pragma once

#include <cstdlib>
#include "ninja/config.hxx"


namespace ninja::memory {

    void* nj_malloc(size_t size);
    void* nj_realloc(void* ptr, size_t size);
    void nj_free(void* ptr);
}


#ifdef NJ_LEAK_DETECTION

void* operator new(size_t size);
void operator delete(void* ptr) noexcept;

void show_allocations();
void assert_no_leak();
#endif

