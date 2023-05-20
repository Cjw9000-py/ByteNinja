#include <string>
#include <exception>

namespace ninja::errors {
    
    struct memory_exception_t : std::exception {
        void* address;
        size_t size;

        inline memory_exception_t(void* address, size_t size)
            : address(address), size(size) { }
    };

    struct io_exception_t : std::exception {

    };

    struct eof_exception_t : io_exception_t {

    };

    struct key_error_t : std::exception {
        std::string key;
        std::string msg;

        inline key_error_t(std::string msg, const std::string& key) : key(key) {
            this->msg = msg + ": " + key;
        }

        inline const char* what() const noexcept {
            return msg.c_str();
        }
    };
}


