

#define true 1
#define false 0



typedef byte_t byteorder_t;


typedef bool_t array_type_t;


typedef byte_t primitive_type_t;
enum primitive_type_e {
    primitive_int_e = 0,
    primitive_float_e = 1,
    primitive_bool_e = 2,
};


/////////// TYPES
typedef struct {
    
} complex_info_t;

typedef struct {
    byteorder_t order;
    uint8_t byte_count;
    bool_t is_signed;
} int_info_t;

typedef struct {
    uint8_t byte_count;
} float_info_t;

typedef struct {
    // empty
} bool_info_t;

typedef struct {

} static_array_info_t;

typedef union {
    complex_info_t as_complex;
    int_info_t as_int;
    float_info_t as_float;
    bool_info_t as_bool;
} type_info_t;

typedef struct {
    bool_t is_primitive;
    bool_t is_array;
    union {
        name_t as_name;

    } type;
    type_info_t info;
} data_type_t;




/////////// INSTANCES

typedef struct {
    data_type_t type;
    union {

    } data;
} instance_t;

typedef struct int_data_t {

};


