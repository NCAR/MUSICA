! Copyright (C) 2023-2024 National Center for Atmospheric Research
! SPDX-License-Identifier: Apache-2.0
!
program photolysis_mapping
  use iso_c_binding
  use musica_tuvx, only: tuvx_t, grid_map_t, grid_t, profile_map_t, profile_t
  use musica_util, only: assert, error_t

  implicit none

#define ASSERT( expr ) call assert( expr, __FILE__, __LINE__ )
#define ASSERT_EQ( a, b ) call assert( a == b, __FILE__, __LINE__ )

  ! Call the solve test subroutine
  call test_photolysis_mapping()

contains

  subroutine test_photolysis_mapping()

    type(tuvx_t),        pointer :: tuvx
    type(error_t)                :: error
    type(grid_map_t),    pointer :: grids
    character(len=256)           :: config_path
    type(grid_t),        pointer :: grid
    type(profile_map_t), pointer :: profiles
    type(profile_t),     pointer :: profile, profile_copy


    config_path = "examples/ts1_tsmlt.json"

    tuvx => tuvx_t( config_path, error )
    ASSERT( error%is_success() )


    deallocate( tuvx )

  end subroutine test_photolysis_mapping

end program photolysis_mapping
