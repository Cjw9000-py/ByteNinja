#include <assert.h>
#include <stdlib.h>
#include "ninja_error.h"


typedef struct {
    nj_err_t _error = err_none_e;
    void* _memory_info;    
} nj_vm;


nj_err_t nj_get_error(nj_vm* vm);
void nj_set_error(nj_vm* vm, nj_err_t err);