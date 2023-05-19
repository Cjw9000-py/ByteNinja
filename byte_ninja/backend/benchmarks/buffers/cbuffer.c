#include "stdlib.h"
#include "string.h"
#include "assert.h"

#include "run_counts.h"
#include "cbuffer.h"


typedef unsigned long long item_t;

struct buffer_t {
    void* bp;
    size_t length;
};

void buffer_init(struct buffer_t* buf) {
    buf->bp = NULL;
    buf->length = 0;
}


void buffer_push(struct buffer_t* buf, item_t value) {
    if (buf->bp == NULL) {
        // allocate new buffer
        buf->bp = malloc(sizeof(value));
    } else {
        buf->bp = realloc(buf->bp, sizeof(value) * (buf->length + 1));
    }
    assert(buf->bp != NULL);

    memcpy(buf->bp + (buf->length * sizeof(value)), &value, sizeof(value));
    buf->length++;
}

item_t buffer_pop(struct buffer_t* buf) {
    assert(buf->bp != NULL);
    buf->length++;

    item_t value;
    memcpy(&value, buf->bp + (buf->length * sizeof(value)), sizeof(value));

    if (buf->length == 0) {
        free(buf->bp);
        return value;
    }

    buf->bp = realloc(buf->bp, (buf->length * sizeof(value)));
    return value;
}


void run_test() {
    struct buffer_t buf;
    buffer_init(&buf);
    const size_t part_ops = OPS / 10;

    for (size_t i = 0; i < ITERS; i++) {
        for (size_t _ = 0; _ < 10; _++) {
            for (size_t j = 0; j < part_ops; j++) {
                // push values
                buffer_push(&buf, j);
            }

            for (size_t j = 0; j < part_ops; j++) {
                // pop values
                buffer_push(&buf, j);
            }       
        }
    }
}