#include <map>
#include <iostream>
#include "ninja/memory.hxx"
#include "ninja/error.hxx"

using namespace ninja;
using namespace ninja::memory;
using namespace ninja::errors;


#ifdef NJ_LEAK_DETECTION
static std::map<void*, size_t> allocation_table{};

void* operator new(size_t size) {
    return memory::nj_malloc(size);
}

void operator delete(void* ptr) noexcept {
    return memory::nj_free(ptr);
}

void show_allocations() {
    std::cerr << "--- Allocation Report ---" << std::endl;
    for (auto& pair : allocation_table) {
        std::cerr << "address: " << std::hex << pair.first << ", size: " << pair.second << "\n";
    }
    std::cerr << std::flush;
}

void assert_no_leak() {
    if (allocation_table.size() == 0) return;

    std::cerr << "Not all memory was freed, displaying allocation report.\n";
    show_allocations();
    abort();
}
#endif


void* nj_malloc(size_t size) {
    void* ptr = malloc(size);

    if (ptr == nullptr) {
        throw new ninja::errors::memory_exception_t{nullptr, size};
    }

#   ifdef NJ_LEAK_DETECTION
    allocation_table[ptr] = size;
#   endif 

    return ptr;
}

void* nj_realloc(void* ptr, size_t size) {
    void* new_ptr = realloc(ptr, size);

    if (new_ptr == nullptr && size != 0) {
        throw ninja::errors::memory_exception_t{nullptr, size};
    }

#   ifdef NJ_LEAK_DETECTION 
    if (size == 0) {
        allocation_table.erase(ptr);
    } 
    else if (ptr == nullptr) {
        allocation_table[new_ptr] = size;
    } 
    else {
        allocation_table.erase(ptr);
        allocation_table[new_ptr] = size;
    }
#   endif

    return ptr;
}

void nj_free(void* ptr) {
#   ifdef NJ_LEAK_DETECTION
    allocation_table.erase(ptr);
#   endif

    free(ptr);
}