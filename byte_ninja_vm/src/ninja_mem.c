// #include "ninja_mem.h"



// void* nj_malloc(nj_vm* vm, size_t size) {

// }

// NJ_EXPORT void* nj_calloc(nj_vm* vm, size_t size);
// NJ_EXPORT void* nj_realloc(nj_vm* vm, void* ptr, size_t size);
// NJ_EXPORT void nj_free(nj_vm* vm, void* ptr);

// NJ_EXPORT size_t nj_get_mem_limit();
// NJ_EXPORT void nj_set_mem_limit(size_t limit);


// //////// ALLOCATION LIST HELPERS

// _nj_alloc_node_t* _nj_find_node(_nj_alloc_list_t* list, void* ptr) {
//     assert(list != NULL);
//     assert(ptr != NULL);

//     // if the list is empty, fail
//     if (list->start_ptr == NULL) return NULL;

//     _nj_alloc_node_t* top = list->start_ptr;
//     // traverse the list
//     while (1) {
//         if (top->alloc_ptr == ptr) {
//             // found the node
//             return top;
//         }

//         if (top->next_ptr == NULL) {
//             // end of the list
//             break;
//         }

//         top = top->next_ptr;
//     }

//     // not found
//     return NULL;
// }


// void _nj_remove_node(_nj_alloc_list_t* list, _nj_alloc_node_t* node) {
//     assert(list != NULL);
//     assert(node != NULL);

//     // if the list is empty, fail
//     assert(list->start_ptr != NULL && list->end_ptr != NULL);

//     // unlink the node

//     if (list->end_ptr == list->start_ptr) {
//         // only node in the list
//         assert(list->start_ptr == node);

//         list->start_ptr = NULL;
//         list->end_ptr = NULL;
//     } 

//     else if (node->next_ptr == NULL) {
//         // node is at the end and other nodes exist
//         assert(node->last_ptr != NULL);

//         node->last_ptr->next_ptr = NULL; // unlink the last and current node
//         list->end_ptr = node->last_ptr; // set the end 
//     }

//     else if (node->last_ptr == NULL) {
//         // node is at the start and other nodes exist
//         assert(node->next_ptr != NULL);

//         node->next_ptr->last_ptr = NULL; // unlink the next and current node
//         list->start_ptr = node->next_ptr; // set the start
//     }

//     else {
//         // node is somewhere in between
//         assert(node->last_ptr != NULL);
//         assert(node->next_ptr != NULL);

//         // link last with the next node 
//         node->last_ptr->next_ptr = node->next_ptr; 
        
//         // link next with the last node 
//         node->next_ptr->last_ptr = node->last_ptr; 
//     }

//     // simply free the node
//     free(node);
// }

// void _nj_append_node(_nj_alloc_list_t* list, _nj_alloc_node_t* node) {
//     assert(list != NULL);
//     assert(node != NULL);

//     if (list->end_ptr == NULL) {
//         assert(list->start_ptr == NULL);
//         // list is empty

//         list->start_ptr = node;
//         list->end_ptr = node;
//         node->last_ptr = NULL;
//         node->next_ptr = NULL;
//         return;
//     }

//     // append to the end
//     assert(list->end_ptr->next_ptr == NULL);

//     // the current and end node
//     list->end_ptr->next_ptr = node;
//     node->last_ptr = list->end_ptr->next_ptr;

//     // set the end
//     list->end_ptr = node;
// }

// void _nj_free_nodes(_nj_alloc_list_t* list) {
//     assert(list != NULL);

//     // free all nodes
//     if (list->end_ptr == NULL) {
//         assert(list->start_ptr == NULL);
//         return; // nothing to free
//     }
    
//     void* last = NULL;
//     for (
//         _nj_alloc_node_t* node = list->start_ptr;
//         node != NULL;
//         node = node->next_ptr
//     ) {
//         if (last != NULL) {
//             free(last);
//         }

//         last = node;
//     }
// }

