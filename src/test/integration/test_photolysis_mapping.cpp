#include <musica/micm.hpp>
#include <musica/tuvx/tuvx.hpp>
#include <musica/util.hpp>

#include <micm/util/error.hpp>

#include <gtest/gtest.h>

#include <iostream>

using namespace musica;

TEST(MusicaAPI, PhotolysisMapping)
{
  Error error;
  MICM* micm = CreateMicm("configs/chapman", MICMSolver::RosenbrockStandardOrder, 1, &error);
  ASSERT_TRUE(IsSuccess(error));
  TUVX* tuvx = CreateTuvx("examples/ts1_tsmlt.yml", &error);
  ASSERT_TRUE(IsSuccess(error));

  // size_t n_micm_rxns;
  // Mapping* micm_rxns = GetUserDefinedReactionRatesOrdering(micm, &n_micm_rxns, &error);
  // double custom_rate_constants = new double[n_micm_rxns];

  // size_t n_tuvx_rxns;
  // Mapping* tuvx_rxns = GetPhotolysisReactionLabels(tuvx, &n_tuvx_rxns, &error);
  // double tuvx_photo_rates = new double[n_tuvx_rxns];

  // IndexMapping* tuvx_to_micm = CreateIndexMap(map_config_path, tuvx_rxns, n_tuvx_rxns, micm_rxns, n_micm_rxns);

  // TuvxCalculate(tuvx, tuvx_photo_rates);
  // ApplyIndexMap(tuvx_to_micm, tuvx_photo_rates, custom_rate_constants);
  // MicmSolve(micm, ..., custom_rate_constants, ...);
}