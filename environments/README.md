# Environments
The games are all made into a gymnasion environment.

Each game should have the follwing fuctions or attributes

## Mandatory Functions:
- `step(action) -> observation, reward, terminated, truncated, info`: Update the game with the action of the player

## Mandatory Attributes:
- `action_space`: A gym space object that describes the possible options
- `observation_space`: A gyme space object that describes the possible observations (i.e. gamestate)
- `_possible_actions`: For each state these are the actions that are allowed at this point