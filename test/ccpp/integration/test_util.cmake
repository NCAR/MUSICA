################################################################################
# build and add a standard test (one linked to the tuvx library)

function(create_standard_test)
  set(prefix TEST)
  set(singleValues NAME WORKING_DIRECTORY)
  set(multiValues SOURCES LIBRARIES)
  include(CMakeParseArguments)
  cmake_parse_arguments(${prefix} " " "${singleValues}" "${multiValues}" ${ARGN})

  add_executable(test_${TEST_NAME} ${TEST_SOURCES})

  # link additional libraries
  foreach(library ${TEST_LIBRARIES})
    target_link_libraries(test_${TEST_NAME} PUBLIC ${library})
  endforeach()

  target_link_libraries(test_${TEST_NAME} PUBLIC musica::musica)

  if(NOT DEFINED TEST_WORKING_DIRECTORY)
    set(TEST_WORKING_DIRECTORY "${CMAKE_BINARY_DIR}")
  endif()

  add_musica_test(${TEST_NAME} test_${TEST_NAME} "" ${TEST_WORKING_DIRECTORY})
endfunction(create_standard_test)

################################################################################
# Add a test

function(add_musica_test test_name test_binary test_args working_dir)
  add_test(NAME ${test_name}
            COMMAND ${test_binary} ${test_args}
            WORKING_DIRECTORY ${working_dir})
endfunction(add_musica_test)

################################################################################