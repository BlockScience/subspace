## Simulation Complexity

- Controllable Parameter Combinations: 23,328
- Environmental Parameter Combinations: 9
- Sweep Combinations: 209,952
- MC Runs: 3
- Total Trajectories: 629,856
- Timesteps: 1,096
- Total State Measurements: 690,322,176

## Performance Measurements
- Execution Time on a Mac M1, 4 Jobs: 274,000 measurements on 250 trajectories in 232 seconds
  - 1,181 M/s
  - 295 M/(J*s)
  - Under the current numbers, the full simulation would take 162 hours to execute.
  - If executed with 100 Jobs, it would take 6.5 hours to execute.
 


| Machine | -d (Days) | -s (Monte Carlo) | -sw (Sweep Samples) | N_jobs (number of processes) | N_t (total timesteps) | N_sweeps (sweeps per process) | N_mc | N_trajectories | N_measurements | Duration(s) | M/s      | M/(J\*S) | Dataset Compressed | Dataset in Memory |
| ------- | --------- | ---------------- | ------------------- | ---------------------------- | --------------------- | ----------------------------- | ---- | -------------- | -------------- | ----------- | -------- | -------- | ------------------ | ----------------- |
| Danilo  | 3*365     | 3                | 83                  | 4                            | 1096                  | 10                            | 3    | 250            | 274,000        | 232         | 1,181    | 295      | x                  | x                 |
| YGG     | 3*365     | 3                | 230                 | 23                           | 1096                  | 5                             | 3    | 690            | 756,240        | 126         | 6,001.88 | 260.95   | 137MB              | 0.69GB            |
| YGG     | 3*365     | 3                | 2300                | 23                           | 1096                  | 5                             | 3    | 6900           | 7,562,400      | 1,261.71    | 5,993.78 | 260.60   | 1.4GB              | 6.9GB             |
|         |           |                  |                     |                              |                       |                               |      |                |                |             |          |          |                    |                   |

What can be achieved in 4 hours of compute?
- YGG is getting 6K measurements / second with 23 jobs.
- How many samples can we sweep in 4 hours?
- X * 1096 * 3 / 6000 = 4\*60\*60
- X = 4\*60\*60 * 6000 / (1096 * 3) = 26277 sweep samples.
- Running now with `RETURN_SIM_DF: bool = False` to eliminate memory constraint in combining the parts.
- Calculating trajectory_tensor batch-wise 


