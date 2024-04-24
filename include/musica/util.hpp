/// Copyright (C) 2023-2024 National Center for Atmospheric Research
/// SPDX-License-Identifier: Apache-2.0
#pragma once

#include <cstddef>

#ifdef __cplusplus
#include <system_error>

#define MUSICA_ERROR_CATEGORY "MUSICA Error"
#define MUSICA_ERROR_CODE_SPECIES_NOT_FOUND 1

extern "C"
{
#endif

/// @brief A struct to describe failure conditions
struct Error
{
  int code_;
  const char* category_;
  const char* message_;
};

/// @brief A struct to represent a string
struct String
{
  char* value_;
  size_t size_;
};

/// @brief A struct to represent a mapping between a string and an index
struct Mapping
{
    char name[256];
    size_t index;
    size_t string_length;
};

/// @brief Casts a char* to a String
/// @param value The char* to cast
/// @return The casted String
String ToString(char* value);

/// @brief Deletes a String
/// @param str The String to delete
void DeleteString(String str);

#ifdef __cplusplus
}

/// @brief Creates an Error indicating no error
/// @return The Error
Error NoError();

/// @brief Creates an Error from syd::system_error
/// @param e The std::system_error to convert
/// @return The Error
Error ToError(const std::system_error& e);

/// @brief Overloads the equality operator for Error types
/// @param lhs The left-hand side Error
/// @param rhs The right-hand side Error
/// @return True if the Errors are equal, false otherwise
bool operator==(const Error& lhs, const Error& rhs);

/// @brief Overloads the inequality operator for Error types
/// @param lhs The left-hand side Error
/// @param rhs The right-hand side Error
/// @return True if the Errors are not equal, false otherwise
bool operator!=(const Error& lhs, const Error& rhs);
#endif