#include <cassert>
#include <stdexcept>
#include "ninja/database.hxx"
#include "ninja/error.hxx"

using namespace ninja::database;
using namespace ninja::errors;


void database_t::register_type(const std::string& name, const database_entry_t* value) {
    if (value == nullptr) {
        throw std::runtime_error("value cannot be null");
    }

    
    if (data.find(name) != data.end()) {
        throw key_error_t("name does already exist", name);
    }

    data[std::string(name)] = value;
}

const database_entry_t* database_t::unregister_type(const std::string& name) {
    if (data.find(name) == data.end()) {
        throw key_error_t("name does not exist", name);
    }

    const database_entry_t* ptr = data.at(name);
    data.erase(name);
    return ptr;
}

const database_entry_t* database_t::query(const std::string& name) const noexcept {
    if (data.find(name) == data.end()) {
        return nullptr;
    }

    return data.at(name);
}

