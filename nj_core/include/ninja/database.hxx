#pragma once

#include <string>
#include <unordered_map>


namespace ninja::database {
    /*
        A database with all types (except the primitives)
    */


    struct database_entry_t {
    };

    struct database_t {
        void register_type(const std::string& name, const database_entry_t* value);
        const database_entry_t* unregister_type(const std::string& name);
        const database_entry_t* query(const std::string& name) const noexcept;

    private:
        std::unordered_map<std::string, const database_entry_t*> data;
    };
}