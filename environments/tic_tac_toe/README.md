# Tic-Tac-Toe

## action_space (Discrete):
Each turn the player can put his mark in one of the 9 possible boxes (if it is empty).

```python
Discrete(n = 9) #{0 - 8}
```

### Example:
```python
Discrete(n = 9, seed = 23).sample() 
#8
```
In this case the player would place its mark in the 9th (last) box in the field

## observation_space (MultiDiscrete)
Each box in a tic-tac-toe grid can have 3 states:
- Empty (0)
- Occupied by the player (1)
- Occupied by the opponent (2)

```python
MultiDiscrete(np.array([[3,3,3],[3,3,3],[3,3,3]]))
```

### Example:
```python
MultiDiscrete(np.array([[3,3,3],[3,3,3],[3,3,3]]), seed = 23).sample() 
#array([[1, 0, 0],
#       [0, 0, 2],
#       [1, 1, 2]])
```

If the player using `X` is at turn that would means the board state would look like this:
```python
|X| | |
 - - - 
| | |O|
 - - - 
|X|X|O|
 - - - 
```