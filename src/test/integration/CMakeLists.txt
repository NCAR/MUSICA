include(test_util)

if (MUSICA_ENABLE_TUVX AND MUSICA_ENABLE_MICM)
  create_standard_test_cxx(NAME photolysis_mapping_cxx SOURCES test_photolysis_mapping.cpp)
endif()