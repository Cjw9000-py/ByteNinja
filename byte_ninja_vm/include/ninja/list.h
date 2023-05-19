#pragma once

#include <stdlib.h>
#include <stddef.h>
#include <inttypes.h>

#include "ninja/config.h"

/*
 This linked list implementation provides:

 - bidirectional linked list

 Notes: 
    freeing is user handled
    searching is user handled
*/

typedef struct {
    void* start_ptr;  // pointer to the start of the list
    void* end_ptr;  // pointer to the end of the list
    size_t length;  // length of the list
    size_t next_field_offset;  // the offset where the next node pointer is stored (in each node)
    size_t last_field_offset;  // the offset where the next last pointer is stored (in each node)
} nj_list_t;

#define NJ_IS_EMPTY_LIST(list) (list->start_ptr == NULL && list->end_ptr == NULL)

#define nj_list_init(list, node_type)                                       \
                (list)->length    = 0;                                      \
                (list)->start_ptr = NULL;                                   \
                (list)->end_ptr   = NULL;                                   \
                (list)->next_field_offset = offsetof(node_type, next_ptr);  \
                (list)->last_field_offset = offsetof(node_type, last_ptr) // no semicolon 


/////////////// Bidirectional linked list

NJ_EXPORT void  nj_list_push(nj_list_t* list, void* node);
NJ_EXPORT void* nj_list_pop(nj_list_t* list);
NJ_EXPORT void* nj_list_unlink(nj_list_t* list, void* node);
NJ_EXPORT void  nj_list_link(nj_list_t* list, void* node, size_t index);






