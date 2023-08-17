# battleshipTerminalGame

Each player has their own 10x10 grid they place their ships on. On their turn, they can fire a torpedo at a square on the enemy's grid. Player 'first' gets the first turn to fire a torpedo, after which players alternate firing torpedos. A ship is sunk when all of its squares have been hit. When a player sinks their opponent's final ship, they win.

Examples of the placeShip method:  
`place_ship('first', 4, 'G9', 'C')`

```
  1 2 3 4 5 6 7 8 9 10
A
B
C
D
E
F
G                 x
H                 x
I                 x
J                 x
```

`place_ship('second', 3, 'E3', 'R')`

```
  1 2 3 4 5 6 7 8 9 10
A
B
C
D
E     x x x
F
G                 
H                 
I                 
J                
```

As a simple example, your class could be used as follows:
```
game = ShipGame()
game.place_ship('first', 5, 'B2', 'C')
game.place_ship('first', 2, 'I8', 'R')
game.place_ship('second', 3, 'H2, 'C')
game.place_ship('second', 2, 'A1', 'C')
game.place_ship('first', 8, 'H2', 'R')
game.fire_torpedo('first', 'H3')
game.fire_torpedo('second', 'A1')
print(game.get_current_state())
```

Your file must be named **ShipGame.py**
