#pragma once
#include <unistd.h>
#include <inttypes.h>

#include "ninja/config.h"
#include "ninja_vm.h"

/*
 Available compile time macros:
    NJ_LEAK_DETECTION -> checks for memory leaks
    NJ_DEBUG_MEMORY -> prints all ninja memory calls to stderr
    NJ_DISABLE_MEM_LIMIT -> disables memory limit checking
*/

#define NJ_NO_LIMIT 0 
#define NJ_DEFAULT_LIMIT NJ_NO_LIMIT

/*
 A node in the ninja allocation table.
 (Only used when NJ_LEAK_DETECTION is defined)
*/
typedef struct {
    void* alloc_ptr;  // pointer to the allocated memory
    size_t alloc_size;  // size of the allocated memory
    _nj_alloc_node_t* last_ptr; // pointer to the last node
    _nj_alloc_node_t* next_ptr; // pointer to the next node
} _nj_alloc_node_t;

typedef struct {
    _nj_alloc_node_t* start_ptr; // pointer to the start of the list
    _nj_alloc_node_t* end_ptr; // pointer to the end of the list
} _nj_alloc_list_t;

typedef struct {
    _nj_alloc_list_t allocations; // a list of all allocation the vm made
    size_t memory_limit; // the maximum amount of memory the vm can consume
} _nj_mem_info_t;


NJ_EXPORT void* nj_malloc(nj_vm* vm, size_t size);
NJ_EXPORT void* nj_calloc(nj_vm* vm, size_t size);
NJ_EXPORT void* nj_realloc(nj_vm* vm, void* ptr, size_t size);
NJ_EXPORT void nj_free(nj_vm* vm, void* ptr);

NJ_EXPORT size_t nj_get_mem_limit(nj_vm* vm);
NJ_EXPORT void nj_set_mem_limit(nj_vm* vm, size_t limit);


//////// ALLOCATION LIST HELPERS

NJ_EXPORT _nj_alloc_node_t* _nj_find_node(_nj_alloc_list_t* list, void* ptr);
NJ_EXPORT void _nj_remove_node(_nj_alloc_list_t* list, _nj_alloc_node_t* node);
NJ_EXPORT void _nj_append_node(_nj_alloc_list_t* list, _nj_alloc_node_t* node);
NJ_EXPORT void _nj_free_nodes(_nj_alloc_list_t* list);