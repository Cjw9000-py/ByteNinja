#include <assert.h>
#include <stdlib.h>
#include "ninja/list.h"


struct test_node_s {
    long value;
    struct test_node_s* last_ptr;
    struct test_node_s* next_ptr;
};

typedef struct test_node_s test_node_t;


#define PUSH_COUNT 1000
#define LINK_COUNT 1000
#define UNLINK_DIVISOR 2

void traverse(nj_list_t* list) {
    size_t counter = 0;
    for (
        test_node_t* node = list->start_ptr;
        node != NULL;
        node = node->next_ptr
    ) {
        assert(node->value == counter);
        counter++;
    }
}

void test_pushing(nj_list_t* list) {

    for (size_t i = 0; i < PUSH_COUNT; i++) {
        test_node_t* node = malloc(sizeof(test_node_t));
        node->value = i;

        nj_list_push(list, node);
    }

    traverse(list);
    assert(list->length == PUSH_COUNT);

    for (size_t i = 0; i < PUSH_COUNT; i++) {
        test_node_t* node = nj_list_pop(list);
        assert(node != NULL);
        free(node);
    }

    assert(list->length == 0);
    assert(list->start_ptr == NULL);
    assert(list->end_ptr == NULL);
}


void test_linking(nj_list_t* list) {
    for (size_t i = 0; i < LINK_COUNT / 2; i++) {
        test_node_t* node = malloc(sizeof(test_node_t));
        node->value = i;

        nj_list_link(list, node, 0);
    }

    for (size_t i = 0; i < LINK_COUNT / 2; i++) {
        test_node_t* node = malloc(sizeof(test_node_t));
        node->value = i;

        nj_list_link(list, node, list->length);
    }

    // values should be
    // 10, ..., 0, 0, ..., 10

    // traverse backwards
    int encountered_zero = 0;
    int counter = -(LINK_COUNT / 2);
    test_node_t* last = NULL;
    test_node_t* current = list->end_ptr;
    for (;;) {
        if (last == NULL) break;
        
        last = current;
        if (current != NULL) {
            current = current->last_ptr;
        }

        void* res = nj_list_unlink(list, last);
        assert(res == last);
            
        // account for the two zeros in the middle of the list
        if (counter == 0 && !encountered_zero) {
            encountered_zero = 1;
        } else {
            counter++;
        }
    }

    assert(counter == LINK_COUNT);
    assert(list->length == 0);

    // now test unlinking nodes not at the end or start
}


int main() {
    nj_list_t* list = malloc(sizeof(nj_list_t));
    nj_list_init(list, test_node_t);

    test_pushing(list);
    test_linking(list);

    free(list);
}

