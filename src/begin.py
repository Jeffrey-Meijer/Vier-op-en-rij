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
  def __repr__(self):
    pass

  def opp_ch(self):
    """
    Returns the opposite stone for the opponent
    If the player has the "X" stone then the opponent will have the 'O' stone and vice verca
    """
    if self.ox == 'X':
      return 'O'
    return 'X'
  def score_board(self, b):
    pass


# opp_sh tests
p = Player('X', 'LEFT', 3)
assert p.opp_ch() == 'O'
assert Player('O', 'LEFT', 0).opp_ch() == 'X'