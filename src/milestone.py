class Board:
    """A data type representing a Connect-4 board
       with an arbitrary number of rows and columns.
    """

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
        self.width = width
        self.height = height
        self.data = [[' ']*width for row in range(height)]

        # We hoeven niets terug te geven vanuit een constructor!

    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        s = ''                          # de string om terug te geven
        for row in range(0, self.height):
            s += '|'
            for col in range(0, self.width):
                s += self.data[row][col] + '|'
            s += '\n'

        s += (2*self.width + 1) * '-'   # onderkant van het bord

        # hier moeten de nummers nog onder gezet worden

        return s       # het bord is compleet, geef het terug
    def add_move(self, col, ox):
      """
      Adds a move to the board
      """
      curr_height = len(self.data)-1
      while curr_height >= 0:
        if self.data[curr_height][col] == ' ':
          self.data[curr_height][col] = ox
          break
        else:
          curr_height -= 1

    def clear(self):
      """
      Clears the board
      """
      self.data = [[' ']*self.width for row in range(self.height)]

    def copy(self):
      """
      Copies the board
      """
      newb = Board(self.width, self.height)
      newb.data = [col[:] for col in self.data]
      return newb

    def set_board(self, move_string):
      """
        Accepts a string of columns and places
        alternating checkers in those columns,
        starting with 'X'.

        For example, call b.set_board('012345')
        to see 'X's and 'O's alternate on the
        bottom row, or b.set_board('000000') to
        see them alternate in the left column.

        move_string must be a string of one-digit integers.
      """
      next_checker = 'X'   # we starten door een 'X' te spelen
      for col_char in move_string:
          col = int(col_char)
          if 0 <= col <= self.width:
              self.add_move(col, next_checker)
          if next_checker == 'X':
              next_checker = 'O'
          else:
              next_checker = 'X'

    def allows_move(self, col):
      """
      Checks if a move is allowed or not based on the col
      """
      max_width = len(self.data[0])
      try:
        if col < 0 or col > max_width or self.data[0][col] != ' ':
          return False
        else:
          return True
      except IndexError: # If the col chosen is outside the array it is not considered a move and thus returns False 
        return False

    def is_full(self):
      """
      Checks if the board is already completely full or not
      """
      width = len(self.data[0])
      for x in range(width):
        if self.allows_move(x):
          return False
      return True

    def del_move(self, col):
      """
      Deletes the top most move based on the given col
      """
      max_height = self.height-1
      height = 0
      while height <= max_height:
        if self.data[height][col] == ' ':
          height += 1
        else:
          self.data[height][col] = ' '
          break
    def wins_for(self, ox):
      """
      Checks if the given player (ox) has any wins on the board.
      It first checks if there are horizontal wins, if not it will continue to check vertical wins
      and if those are not found it will check the diagonal wins
      """
      # Check for horizontal winnings
      for row in range(0, self.height):
        for col in range(0, self.width - 3):
          if self.data[row][col] == ox and \
            self.data[row][col + 1] == ox and \
            self.data[row][col + 2] == ox and \
            self.data[row][col + 3] == ox:
              return True
      # Check for vertical winnings
      for row in range(0, self.height - 3):
        for col in range(0, self.width):
          if self.data[row][col] == ox and \
            self.data[row + 1][col] == ox and \
            self.data[row + 2][col] == ox and \
            self.data[row + 3][col] == ox:
              return True

      # Check for diagonal winnings
      for row in range(0, self.height):
        for col in range(0, self.width):
          if in_a_row_n_northeast(ox, row, col, self.data, 4) or in_a_row_n_southeast(ox,row,col,self.data,4):
            return True
      
      return False


    def host_game(self):
      """
      Starts a game of "Four in a row" using the functions that were
      created in previous assignments.
      
      It gives each player a turn to play a turn and checks if the turn
      was a winning move or not.
      """
      # Clear the board (in case this isn't the first game)
      self.clear()
      
      # Set variables
      current_player = 'X'
      winner = None
      
      # Gameplay loop
      while True:
        print('Welkom bij Vier op een rij!')
        print(self)
        col = int(input("Keuze van " + current_player + ": "))
        
        if self.allows_move(col):
          self.add_move(col, current_player)

          # Check if move wins the game
          if self.wins_for(current_player):
            winner = current_player
            break

          # Check if board is full
          if self.is_full():
            break

          # Toggle between players after a move
          if current_player == 'X':
            current_player = 'O'
          else:
            current_player = 'X'

        else:
          print('Geen geldige input!')
        
      if winner != None:
        print(self)
        print(winner + ' wint -- Gefeliciteerd!')
      else:
        print(self)
        print('Gelijkspel, geen winnaar!')

def in_a_row_n_southeast(ch, r_start, c_start, a, n):
  """
  Checks if there are n amount of pieces in a row on the SOUTH_EAST side
  """
  rows = len(a)
  cols = len(a[0])

  if r_start < 0 or r_start + (n-1) > rows - 1:
      return False  # rij buiten de grenzen
  if c_start < 0 or c_start + (n-1) > cols - 1:
      return False  # kolom buiten de grenzen

  for i in range(n):
    if a[r_start+i][c_start+i] != ch:
      return False
  return True

def in_a_row_n_northeast(ch, r_start, c_start, a, n):
  """
  Checks if there are n amount of pieces in a row on the NORTH_EAST side
  """
  rows = len(a)
  cols = len(a[0])

  if r_start - (n-1) < 0 or r_start > rows - 1:
      return False  # rij buiten de grenzen
  if c_start < 0 or c_start + (n-1) > cols - 1:
      return False  # kolom buiten de grenzen

  for i in range(n):
    if a[r_start-i][c_start+i] != ch:
      return False
  return True


class Player:
  def __init__(self, ox, tbt, ply):
    """
    Constructs the player with the given checker, the tie breaking type and ply
    """
    self.ox = ox
    self.tbt = tbt
    self.ply = ply
    self.col = 0

  def __repr__(self):
    """
    Returns the representation of the Player object.
    Shows the checker it uses, the choice strategy(tbt) and the ply
    """
    return f"Player: ox = {self.ox}, tbt = {self.tbt}, ply = {self.ply}"

  def opp_ch(self):
    """
    Returns the opposite stone for the opponent
    If the player has the "X" stone then the opponent will have the 'O' stone and vice verca
    """
    if self.ox == 'X':
      return 'O'
    return 'X'

  def score_board(self, b) -> float:
    """
    Returns a float bases on what player is winning or has won.
    100 if won by the calling player object, 50 if no one has won and 0 if the opponent has won.
    """
    if b.wins_for(self.ox):
      return 100.0
    if b.wins_for(self.opp_ch()):
      return 0.0
    
    return 50.0

  # def generate_score(self,b,col):
  #   db = b.copy()
    
  #   current_player = self.ox
  #   if self.ply == 0:
  #     return 50.0
  #   else:
  #     for x in range(self.ply):
  #       if not db.allows_move(col):
  #         return -1.0
  #       else:
  #         print(f'{col}: test')
  #         if current_player == self.ox:
  #           db.add_move(col, self.ox)
  #         else:
  #           db.add_move(col,self.opp_ch())
  #         current_player = self.opp_ch()
  #         score = self.score_board(db)
  #         print(score)
  #     for x in range(self.ply):
  #       db.del_move(col)
  #     print(f'returning score:{score}')
  #     return score
  #     # for x in range(self.ply):
  #     #   db.add_move(col, self.ox)
  #     #   scores[col] = self.score_board(db)
  #     # for x in range(self.ply): # moves made being removed
  #     #   db.del_move(col)

  # def scores_for(self, b):
  #   scores = [50.0] * b.width
  #   op = Player(self.opp_ch(), self.tbt, self.ply)
  #   for col in range(b.width):
  #     # op_scores = op.generate_score(col)
  #     scores[col] = self.generate_score(b,col)

  #   return scores

  def generate_score(self, db, col, ply, ox):
    print(f'current_col:{col}')
    if not db.allows_move(col):
      return -1.0
    elif db.wins_for(self.ox):
      return 100.0
    elif db.wins_for(self.opp_ch()):
      return 0.0
    elif ply == 0:
      return 50.0
    else:
      db.add_move(col, ox)
      print(db)
      # ox = self.opp_ch()
      return self.generate_score(db, col, ply-1, ox)
  def scores_for(self, b):
    scores = [50.0] * b.width
    op_scores = [50.0] * b.width
    ply = self.ply
    op = None
    if self.ply > 1:
      op = Player(self.opp_ch(), self.tbt, self.ply)
    for col in range(b.width):
      db = b.copy()
      scores[col] = self.generate_score(db, col, ply, self.ox)
      op_scores[col] = self.generate_score(db, col, ply, op.ox)
      print(scores)
      print(op_scores)
    return scores
      



      


# opp_sh tests
p = Player('X', 'LEFT', 3)
assert p.opp_ch() == 'O'
assert Player('O', 'LEFT', 0).opp_ch() == 'X'

# score_board tests
b = Board(7, 6)
b.set_board('01020305')
print(b)
p = Player('X', 'LEFT', 0)
assert p.score_board(b) == 100.0
assert Player('O', 'LEFT', 0).score_board(b) == 0.0
assert Player('O', 'LEFT', 0).score_board(Board(7, 6)) == 50.0

#scores_for
b = Board(7,6)
b.set_board('1211244445')