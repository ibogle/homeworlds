# homeworlds
Efficient representation of the tabletop game homeworlds, intended for eventual AI consumption

Uses a bitwise representation packed into two 64-bit integers, with 9 bitmasks to determine appropriate context:
  - Board state is represented by 72 bits, 36 for the bank, 36 for the playable area.
  - The player mask determines the owner of ships and homeworlds
  - The star mask determines which pieces in play are stars; These are the first piece, followed by the ships at the star
  - The size masks (1,2,3) determine which pieces are which size
  - The color masks (red,green,blue,yellow) determine which pieces are which color

TODO, and miscellaneous thoughts:

  - If there are masks for each extant star, it will be easy to form conditionals to test whether actions are possible.
     The upper-bound for the possible number of stars is 2 + (36-4)/2 = 18, meaning I'd need 18 additional masks for this, potentially.
     2x the number of masks I currently have. Rough!

  - The movement rules aren't exactly straightforward to implement from what I have here. I suppose `star_mask & size_mask` can tell
     _if_ there are valid move actions that can take place, but not where they are, precisely. I need to turn a one-hot binary uint64 into the indicies that are nonzero, sounds annoying to me.

  - Movement means that if a ship at a new star moves to an old one, I need to scooch all newer stars over one to accommodate the new ship. Even worse for multi-yellow sacrifices, but maybe I can process those in serial instead of parallel.

  - Might make sense to keep a count of stars, and star-specific stuff to make it easy to execute the scooch

  - To propose a move is not to make the move, so could it make sense to develop a string-based method for describing moves, and letting the board execute them in the easiest way? For this to work, I'd need to name the stars (at least number them), so that they can be referred to.

  - Sounds like I just need to name the stars from left-to-right, without unique names (the numbers will be context sensitive based on how many stars exist right now.

AI notes:

  - enumerating all possible moves is probably not tractable. Enumerating all moves of a certain type may be barely tractable. For instance, all ship actions: 
    - check if any captures are possible (more prohibitive), see if red exists at a star where a capture is possible. - probably none, maybe on the order of 10 max
    - check if yellow exists at a star (more prohibitive), enumerate valid stars to travel to, all ships at that star can travel to those stars. - probably a ton (10-50?)
    - check if green exists at a star (more prohibitive), enumerate ships at that star, and the ships they can grow from the bank. (on the order of \#ships)
    - check if blue exists at a star (more prohibitive), enumerate ships at that star, and ships from the bank that they can transform into. (on the order of \#ships)
  
  - enumerating all possible sacrifice actions is the same as enumerating ship actions of a certain type, without the more prohibitive restrictions, except in the case of red.
    This means that each sacrifice action can be done by some number of sequential moves, checking a less restrictive version of the move each time. I.E.:

``` 
    action_type, num_actions = sacrifice((ship_type, ship_size))
    for(i in range(0,num_actions)):
      moves = enumerate_moves(action_type, board_state, ship_action=False)
      best_move = cool_ai_thing(moves)
      board = board.execute(best_move)
```
