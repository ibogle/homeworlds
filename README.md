# homeworlds
Efficient representation of the tabletop game homeworlds, intended for eventual AI consumption

Uses a bitwise representation packed into two 64-bit integers, with 9 bitmasks to determine appropriate context

Board state is represented by 72 bits, 36 for the bank, 36 for the playable area.
The player mask determines the owner of ships and homeworlds
The star mask determines which pieces in play are stars; These are the first piece, followed by the ships at the star
The size masks (1,2,3) determine which pieces are which size
The color masks (red,green,blue,yellow) determine which pieces are which color

TODO, and miscellaneous thoughts:

  1. If there are masks for each extant star, it will be easy to form conditionals to test whether actions are possible.
     The upper-bound for the possible number of stars is 2 + (36-4)/2 = 18, meaning I'd need 18 additional masks for this, potentially.
     2x the number of masks I currently have. Rough!

  2. The movement rules aren't exactly straightforward to implement from what I have here. I suppose `star\_mask & size_mask` can tell
     _if_ there are valid move actions that can take place, but not where they are, precisely. I need to turn a one-hot binary uint64 into the indicies that are nonzero, sounds annoying to me.

  3. Movement means that if a ship at a new star moves to an old one, I need to scooch all newer stars over one to accommodate the new ship. Even worse for multi-yellow sacrifices, but maybe I can process those in serial instead of parallel.

  4. Might make sense to keep a count of stars, and star-specific stuff to make it easy to execute the scooch

  5. To propose a move is not to make the move, so could it make sense to develop a string-based method for describing moves, and letting the board execute them in the easiest way? For this to work, I'd need to name the stars (at least number them), so that they can be referred to.

  6. Sounds like I just need to name the stars from left-to-right, without unique names (the numbers will be context sensitive based on how many stars exist right now. 
