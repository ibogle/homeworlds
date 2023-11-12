# homeworlds
Efficient representation of the tabletop game homeworlds, intended for eventual AI consumption

Uses a bitwise representation packed into one 64-bit integer:
  - bank_mask determines if the piece is currently in the bank
  - size_mask[0-2] determines which size a piece is, and never changes
  - color_mask[0-3] determines which color a piece is, and never changes
  - star_mask determines which pieces are stars
  - player_mask[0-1] determines which pieces belong to which players
    - stars in general belong to neither player, homeworlds are the exception
  - at_star_mask[0-17] holds information about which pieces are currently at which star
    - ids here are translated to the star's piece by using the star_position array
    - the star is included in this mask, allowing easy checking of whether a player's ship has access to a power at a given star
 

TODO, and miscellaneous thoughts:

  - Finish implementing moves. Need higher level function for general actions, that executes ship and sacrifice actions.
    - Ship actions are essentially a special case of sacrifice action. No precondition for losing a ship, and only a single action of any type.

  - Checking if a ship of a certain color is present at a star is a generalizable check, should do that to avoid code duplication
    - return true if a ship owned by player or the star is a certain color, false otherwise
  

AI notes:

  - enumerating all possible moves is probably not tractable. Enumerating all moves of a certain type may be barely tractable. For instance, all ship actions: 
    - check if any captures are possible (more prohibitive), see if red exists at a star where a capture is possible. - probably none, maybe on the order of 10 max
    - check if yellow exists at a star (more prohibitive), enumerate valid stars to travel to, all ships at that star can travel to those stars. - probably a ton (10-50?)
    - check if green exists at a star (more prohibitive), enumerate ships at that star, and the ships they can grow from the bank. (on the order of \#ships)
    - check if blue exists at a star (more prohibitive), enumerate ships at that star, and ships from the bank that they can transform into. (on the order of \#ships)
    
  - napkin math memory usage for avg-case ship action enumeration: 10 + 50 + 18 + 18 = 96. size of board representation = 2\*64\*36 = 4.5 KB per board. Memory footprint for ship enumeration: 96 * 4.5 KB = 432 KB. The board state (or some representation of the move taken) needs to be preserved for each turn, so 4.5 KB * \# turns, which means I can store about 14M turns in RAM alone, assuming I add the convenience star masks to the board representation.
  - Action enumeration is embarassingly parallel if it is parallelized at the ship level. Each action is taken independently, so I can ignore the other actions that are being tried concurrently. For move actions, copy the set of stars from one ship and apply them to the other ships for valid stars to travel to.

  - enumerating all possible sacrifice actions is the same as enumerating ship actions of a certain type, without the more prohibitive restrictions, except in the case of red.
    This means that each sacrifice action can be done by some number of sequential moves, checking a less restrictive version of the move each time. I.E.:

``` 
    action_type, num_actions = sacrifice((ship_type, ship_size))
    for(i in range(0,num_actions)):
      moves = enumerate_moves(action_type, board_state, ship_action=False)
      best_move = cool_ai_thing(moves)
      board = board.execute(best_move)
```

  - Because of the amount of possible moves being very large, deep Q learning probably won't work end-to-end. It _could_ work for selecting whether the move should be sacrifice/ship action, and then which type of action should be taken. Then, we can enumerate all possible moves of that type, and use a deep neural net to do board state evaluation based on it playing itself. Changing the weights frequently will probably make learning unstable, so play old vs. changing or something to keep stability, then add the changed weights to the old weights scaled by how many times they won, and the learning rate.
