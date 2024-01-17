#include <micm/micm.hpp>

#include <micm/configure/solver_config.hpp>

MICM::MICM(const std::string& config_path)
    : config_path_(config_path),
      solver_(nullptr)
    {}

MICM::~MICM()
{   
    delete solver_;
}

int MICM::create_solver()
{
    int faliure = 0;

    micm::SolverConfig solver_config;
    micm::ConfigParseStatus status = solver_config.ReadAndParse(config_path_);

    if (status == micm::ConfigParseStatus::Success)
    {
        micm::SolverParameters solver_params = solver_config.GetSolverParams();
        auto params = micm::RosenbrockSolverParameters::three_stage_rosenbrock_parameters(NUM_GRID_CELLS);
        params.reorder_state_ = false;
        solver_ = new VectorRosenbrockSolver{solver_params.system_,
                                            solver_params.processes_,
                                            params};
    }
    else 
    {
        faliure = 1; 
    }

    return faliure;
}

void MICM::solve(double temperature, double pressure, double time_step, int num_concentrations, double*& concentrations)
{
    micm::State state = solver_->GetState();

    for(size_t i{}; i < NUM_GRID_CELLS; ++i) {
        state.conditions_[i].temperature_ = temperature;
        state.conditions_[i].pressure_ = pressure;
    }

    v_concentrations_.assign(concentrations, concentrations + num_concentrations);
    state.variables_[0] = v_concentrations_;

    auto result = solver_->Solve(time_step, state);

    v_concentrations_ = result.result_.AsVector();
    for (int i=0; i<v_concentrations_.size(); i++)
    {
        concentrations[i] = v_concentrations_[i];
    }
}