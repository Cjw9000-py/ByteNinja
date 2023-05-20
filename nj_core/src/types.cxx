#include "ninja/memory.hxx"
#include "ninja/types.hxx"


using namespace ninja::types;
using namespace ninja::memory;


code_object_t::code_object_t(const char* bytecode) : data(bytecode) {}


///////////////// Data Types

bool data_type_t::is_primitive() const noexcept {
    return false;
}

bool primitive_type_t::is_primitive() const noexcept {
    return true;
}
