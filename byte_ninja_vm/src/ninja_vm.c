// #include "ninja_vm.h"

// nj_err_t nj_get_error(nj_vm* vm) {
//     nj_err_t err = vm->__error;
//     vm->__error = err_none_e;
//     return err;
// }

// void nj_set_error(nj_vm* vm, nj_err_t err) {
// #ifdef NJ_ASSERT_CATCH_ALL
//     // check if the last error was catched
//     assert(vm->__error == err_none_e);
// #endif 
//     vm->__error = err;
// }