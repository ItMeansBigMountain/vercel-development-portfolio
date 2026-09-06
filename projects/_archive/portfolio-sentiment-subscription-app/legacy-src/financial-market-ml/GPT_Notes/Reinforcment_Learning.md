### Simple Notes Sheet: Reinforcement Learning

#### Key Vocabulary and Concepts

| Term                       | Quick Explanation                                                                                         |
|----------------------------|-----------------------------------------------------------------------------------------------------------|
| **Reinforcement Learning** | Training an algorithm to make decisions by rewarding good actions and penalizing bad ones.                |
| **Agent**                  | The learner or decision-maker (like a robot or a trading algorithm).                                       |
| **Environment**            | The world the agent interacts with (like a maze or the stock market).                                      |
| **State**                  | The current situation of the agent (e.g., agent's position in the maze).                                   |
| **Action**                 | Possible moves the agent can make (e.g., move up, down, left, right).                                      |
| **Reward**                 | Feedback given to the agent (positive for good actions, negative for bad).                                  |
| **Q-Learning**             | A method where the agent learns the best actions by keeping a table of rewards for each action in each state.|
| **Q-Table**                | A table storing the expected rewards for each action in each state.                                        |
| **Discounted Rewards**     | Future rewards are valued less than immediate rewards, using a factor called gamma (γ).                    |
| **Gamma (γ)**              | A factor that determines how much future rewards are discounted (values between 0 and 1).                  |
| **Policy**                 | The strategy used by the agent to decide actions based on the current state.                               |
| **Epsilon-Greedy Policy**  | A strategy where the agent mostly takes the best-known action but sometimes takes a random action to explore.|
| **Trajectory**             | The sequence of states and actions taken by the agent from start to finish.                                |
| **Episode**                | A complete sequence of actions from the start to the end of the task (like one run through the maze).      |
| **Proximal Policy Optimization (PPO)** | An advanced RL algorithm used to improve the agent's decision-making process.                          |
| **State-Action Pair**      | A combination of a state and an action, used to determine the best actions based on rewards.               |
| **Continuous State**       | A state with many possible values (like stock prices).                                                     |
| **Discrete State**         | A state with a limited set of values (like grid positions in a maze).                                      |
| **Continuous Action**      | Actions with a range of values (e.g., the amount to buy/sell).                                             |
| **Discrete Action**        | A limited set of actions (e.g., buy, sell, hold).                                                          |
| **Dynamic Programming**    | An approach for solving problems with a lot of overlapping subproblems, often used for discrete spaces.    |
| **Neural Networks**        | Algorithms modeled after the human brain, used for recognizing patterns and making decisions in RL.        |
| **Advantage Actor-Critic (A2C)** | A method in RL that uses two neural networks: one for deciding actions (actor) and one for evaluating them (critic).|

### Quick Reference Guide

1. **Reinforcement Learning Basics**
   - **Agent**: Learner (e.g., robot, trading bot).
   - **Environment**: World it interacts with (e.g., maze, stock market).
   - **State**: Current situation (e.g., position in the maze).
   - **Action**: Possible moves (e.g., up, down).
   - **Reward**: Feedback (e.g., +1 for reaching the exit).

2. **Learning Methods**
   - **Q-Learning**: Learning the best actions by storing rewards in a Q-Table.
   - **Discounted Rewards**: Future rewards are less valuable; calculated using gamma (γ).

3. **Policies and Strategies**
   - **Policy**: Strategy for deciding actions.
   - **Epsilon-Greedy**: Mostly best actions, sometimes random for exploration.

4. **Advanced Techniques**
   - **PPO Algorithm**: Improves decision-making by optimizing the policy.
   - **Neural Networks**: Used for pattern recognition in RL.

5. **Applications in Trading**
   - **Continuous States**: Stock prices, indicators.
   - **Discrete Actions**: Buy, sell, hold.

### Example: Applying RL to a Maze

- **Goal**: Get the agent from start to exit.
- **States**: Each position in the maze.
- **Actions**: Move up, down, left, right.
- **Rewards**: +1 for reaching the exit, -1 for hitting a wall.

By following these simple notes and using the vocabulary and concepts as a reference, you can better understand the reinforcement learning process and how to apply it to various problems, including financial trading.