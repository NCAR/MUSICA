include(test_util)

if (MUSICA_ENABLE_TUVX AND MUSICA_ENABLE_MICM)
  create_standard_test_fortran(NAME photolysis_mapping_fortran SOURCES ../fetch_content_integration/test_photolysis_mapping.F90)
endif()