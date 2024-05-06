include(FetchContent)

################################################################################
# NetCDF library
if (MUSICA_BUILD_FORTRAN_INTERFACE)
  find_package(PkgConfig REQUIRED)
  pkg_check_modules(netcdff IMPORTED_TARGET REQUIRED netcdf-fortran)
endif()

################################################################################
# google test
if(MUSICA_ENABLE_TESTS)
  FetchContent_Declare(googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG be03d00f5f0cc3a997d1a368bee8a1fe93651f48
  )

  set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
  set(BUILD_GMOCK OFF CACHE BOOL "" FORCE)

  FetchContent_MakeAvailable(googletest)
endif()

################################################################################
# OpenMP
if(MUSICA_ENABLE_OPENMP)
  find_package(OpenMP REQUIRED)
endif()

################################################################################
# MICM

if (MUSICA_ENABLE_MICM)
  FetchContent_Declare(micm
      GIT_REPOSITORY https://github.com/NCAR/micm.git
      GIT_TAG 2a5cd4e11a6973974f3c584dfa9841d70e0a42d5
  )
  FetchContent_MakeAvailable(micm)
endif()

################################################################################
# TUV-x

if (MUSICA_ENABLE_TUVX)
  set(ENABLE_TESTS OFF CACHE BOOL "" FORCE)
  FetchContent_Declare(tuvx
    GIT_REPOSITORY https://github.com/NCAR/tuv-x.git
    GIT_TAG set_defaults_path
  )
  FetchContent_MakeAvailable(tuvx)
endif()

################################################################################
# pybind11
if(MUSICA_ENABLE_PYTHON_LIBRARY)
  set(PYBIND11_NEWPYTHON ON)

  FetchContent_Declare(pybind11
      GIT_REPOSITORY https://github.com/pybind/pybind11
      GIT_TAG        v2.12.0
  )

  FetchContent_GetProperties(pybind11)
  if(NOT pybind11_POPULATED)
      FetchContent_Populate(pybind11)
      add_subdirectory(${pybind11_SOURCE_DIR} ${pybind11_BINARY_DIR})
  endif()
endif()