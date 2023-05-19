#include "ninja/list.h"
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#define FIELD(list, node, name) *((void **)((char *)node + list->name##_field_offset))

void nj_list_push(nj_list_t* list, void *node) {
    // Append/Push a node to the list

    if (NJ_IS_EMPTY_LIST(list)) {
        // list is empty
        // set start and end to the current node

        list->start_ptr = node;
        list->end_ptr = node;

        // set node links to null
        FIELD(list, node, next) = NULL;
        FIELD(list, node, last) = NULL;


        // done
        list->length++;
        return;
    }

    void* last_node = list->end_ptr;

    // set next field of last node to the pushed node
    FIELD(list, last_node, next) = node;
    FIELD(list, node, next) = NULL;

    /* set the last field of the pushed
         node to the now second last node */
    FIELD(list, node, last) = last_node;


    // set the end ptr to the pushed node
    // and increment the length
    list->end_ptr = node;
    list->length++;
}

void* nj_list_pop(nj_list_t* list) {
    // pop a node from the end

    assert(!NJ_IS_EMPTY_LIST(list));

    void *node = list->end_ptr;
    void *new_ending_node = FIELD(list, node, last);

    list->end_ptr = new_ending_node;
    list->length--;

    if (list->length == 0) {
        list->end_ptr = NULL;
        list->start_ptr = NULL;
    }

    // unlink old last and new last 
    if (new_ending_node != NULL) {
        FIELD(list, new_ending_node, next) = NULL;
    }
    
    // set old lasts fields to NULL
    FIELD(list, node, next) = NULL;
    FIELD(list, node, last) = NULL;
    return node;
}

void* nj_list_unlink(nj_list_t* list, void *node) {
    // unlink a node from the tree at any position
    assert(list != NULL);
    assert(node != NULL);

    // if the list is empty, fail
    assert(NJ_IS_EMPTY_LIST(list));

    // unlink the node
    if (list->end_ptr == list->start_ptr) {
        // only node in the list
        assert(list->start_ptr == node);

        list->start_ptr = NULL;
        list->end_ptr = NULL;
    }

    else if (FIELD(list, node, next) == NULL) {
        // node is at the end and other nodes exist
        assert(FIELD(list, node, last) != NULL);

        // unlink the last and current node
        void* last_node = FIELD(list, node, last);
        FIELD(list, last_node, next) = NULL; 

        list->end_ptr = last_node;  // set the end
    }

    else if (FIELD(list, node, last) == NULL) {
        // node is at the start and other nodes exist
        assert(FIELD(list, node, next) != NULL);

        // unlink the next and current node
        void* next_node = FIELD(list, node, next);
        FIELD(list, next_node, last) = NULL;   

        list->start_ptr = next_node; // set the start
    }

    else {
        // node is somewhere in between
        assert(FIELD(list, node, last) != NULL);
        assert(FIELD(list, node, next) != NULL);

        // link last with the next node
        FIELD(list, FIELD(list, node, last), next) = FIELD(list, node, next);
        
        // link next with the last node
        FIELD(list, FIELD(list, node, next), last) = FIELD(list, node, last);
    }

    // simply free the node
    return node;
}

void nj_list_link(nj_list_t* list, void* node, size_t index) {
    assert(list != NULL);
    assert(node != NULL);

    if (NJ_IS_EMPTY_LIST(list)) {
        assert(index == 0);

        // just assign as the root node
        list->start_ptr = node;
        list->end_ptr = node;
        FIELD(list, node, next) = NULL;
        FIELD(list, node, last) = NULL;
        list->length++;
        goto end;
    }

    // find the node at index
    void* top = list->start_ptr;
    for (size_t i = 0; i < index; i++) {
        printf("%lx", top);
        top = FIELD(list, top, next);
        assert(top != NULL);
    } // TODO check direction

    void* last_node = FIELD(list, top, last);
    if (last_node != NULL) {
        FIELD(list, last_node, next) = node;
    }

    FIELD(list, top, last) = node;

    if (list->start_ptr == top) {
        list->start_ptr = node;
    }

    // dont check for the end
    // we insert before the node at given index
    end:
    list->length++;
}