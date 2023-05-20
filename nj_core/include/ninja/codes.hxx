

namespace ninja::codes {
    enum byteorder_e {
        order_le = 0,
        order_be = 1,
    };

    enum class primitive_e {
        not_primitive   = 0b000,
        int_type        = 0b001,
        float_type      = 0b010,
        bool_type       = 0b011,
        // array_type      = 0b100,
        // custom_array    = custom_type   | array_type,
        // int_array       = int_type      | array_type,
        // float_array     = float_type    | array_type,
        // bool_array      = bool_type     | array_type,
    };

    enum opcode_e {
        op_get,
        op_set,

        op_dynamic,
        op_static,
        op_apop,
        op_apush,
        op_aget,
        op_aset,
        op_freeze,
        op_loose,
        op_push,
        op_pop,
        op_look,
        op_put,
        op_math,

        op_seek,
        op_tell,
        op_read,
        op_rseq,
        op_write,
        op_wseq,

        op_jump,
        op_test,
        op_ret,
    };

    // constexpr inline uint8_t bit_length(uint64_t value) {
    //     uint8_t counter = 0;
    //     while (value != 0) {
    //         value >>= 1;
    //         counter++;
    //     }
    //     return counter;
    // }

    // inline bool is_array_type(data_type_e type) {
    //     const uint8_t bit_index = bit_length(array_type);
    //     // array = 0b100
        
    //     return type & array_type >> (bit_index - 1);
    // }
}