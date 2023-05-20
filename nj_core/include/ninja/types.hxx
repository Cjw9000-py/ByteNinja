#pragma once

#include <map>
#include <vector>
#include <cinttypes>
#include "ninja/codes.hxx"


namespace ninja::types {
    using namespace ninja::codes;
   
    typedef uint8_t opcode_t;
    typedef uint64_t index_t;
    typedef uint64_t length_t;
 

    struct code_object_t {
        const char* data;
        const char** name_table;
        const char* code;

        code_object_t(const char* bytecode);
    };

       
    struct data_type_t {
        virtual bool is_primitive() const noexcept;
        virtual const code_object_t* get_read_code() const noexcept = 0;
        virtual const code_object_t* get_write_code() const noexcept = 0;
    };

    struct primitive_type_t : data_type_t {
        bool is_primitive() const noexcept override;
        const code_object_t* get_read_code() const noexcept override;
        const code_object_t* get_write_code() const noexcept override;
    };

    struct int_type_t : primitive_type_t {
        uint16_t byte_count;
        uint8_t order;
        bool sign;

        
    };

    struct float_type_t : primitive_type_t {
        uint8_t byte_count;
    };

    struct bool_type_t : primitive_type_t { };




    // : byte_count(count), order(order), sign(sign) {
    //         primitive = static_cast<uint8_t>(primitive_e::int_type);
    //     }


    // struct field_collection_t {
    //     bool is_data;
    //     union {
    //         std::map<name_t, field_collection_t> as_collection;
    //         data_type_t* as_data;
    //     } value;
    // };

    // struct stack_value_t {

    // };

    // struct stack_t {
    //     std::vector<stack_value_t*> values;
    //     std::vector<uint64_t> levels;

    //     stack_t();

    // };
}