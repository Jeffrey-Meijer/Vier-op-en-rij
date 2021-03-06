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
      return 100
    if b.wins_for(self.opp_ch()):
      return 0
    
    return 50

  def tiebreak_move(self, scores):
    """
    Return the best move based on the strategy 'LEFT'  of 'RIGHT' using scores
    If there is only one high number return that index
    """ 
    # Lijst is leeg
    if scores == [] or scores is None:
      return 0

    # Check of er maar 1 hoge score is
    high = max(scores)
    temp_scores = list(scores)

    temp_scores.remove(high)
    # High is enigste in de lijst
    if not high in temp_scores:
      return scores.index(high)

    # Pak het midden
    mid = len(scores)// 2
    # Zet begin waarde high op midden
    high = scores[mid]
    # Zet begin waarde best_index op het midden
    best_index = mid

    # Kolom met hoogste waarde voor 'LEFT'
    if self.tbt == 'LEFT':
      high = max(scores[:mid+1])
      best_index = scores.index(high)
    # Kolom met hoogste waarde voor 'LEFT'
    elif self.tbt == 'RIGHT':
      high = max(scores[mid:])
      # Loop through list reverse and get the first occurence of high. 
      # Because best_index is used in the loop it doenst need to bee asigned anymore
      for best_index in range(len(scores)-1,mid,-1):
          if scores[best_index] == high:
              break
    else:
      # tbt = random
      all_highs = []
      for n in range(len(scores)):
        if scores[n] == max(scores):
          all_highs += [n]

      import random
      best_index = random.choice(all_highs)

    return best_index

  def scores_for(self, b):
    """
    Returns a list with the same amount of elements as the board's width.
    This list contains the moves it considers to be the best based on the amount of look ahead (self.ply)
    """
    scores = [50.0] * b.width
    
    for x in range(b.width):
      db = b.copy()
      if not db.allows_move(x):
        scores[x] = -1.0
      elif db.wins_for(self.ox):
        scores[x] = 100.0
      elif db.wins_for(self.opp_ch()):
        scores[x] = 0.0
      if self.ply == 0:
        scores[x] = 50.0
      elif self.ply > 0:
        db.add_move(x, self.ox)
        if db.wins_for(self.ox):
          scores[x] = 100.0
        else:
          op = Player(self.opp_ch(), self.tbt, self.ply-1)
          op_scores = op.scores_for(db)
          op_choice = op.tiebreak_move(op_scores)
          scores[x] = 100.0 - op_scores[op_choice]
        db.del_move(x)
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

## Tiebreak_move tests ##
print("Tiebreak_move tests")
b = Board(7, 6)
b.set_board('01020351515')
print(b)
p_left = Player('X', 'LEFT', 0)
p_right = Player('O', 'RIGHT', 0)
p_random = Player('O', 'RANDOM', 0)

# Scores voor left
scores_l = [100,50,50,50,50,100,50]

# Scores voor right
scores_r = [50, 100, 50, 50, 100, 50, 50]

# Scores voor random
scores_r = [50, 100, 100, 50, 100, 50, 100]

assert p_left.tiebreak_move(scores_l) == 0 or 5
assert p_right.tiebreak_move(scores_r) == 4 or 6
print(f"Random strategy result. column chosen was: {p_random.tiebreak_move(scores_r)}")

# scores_for tests
print("Scores_for tests")
b = Board(7, 6)
b.set_board('1211244445')
print(b)

# 0-ply lookahead ziet geen bedreigingen
assert Player('X', 'LEFT', 0).scores_for(b) == [50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0]

# 1-play lookahead ziet een manier om te winnen
# (als het de beurt van 'O' was!)
assert Player('O', 'LEFT', 1).scores_for(b) == [50.0, 50.0, 50.0, 100.0, 50.0, 50.0, 50.0]

# 2-ply lookahead ziet manieren om te verliezen
# ('X' kan maar beter in kolom 3 spelen...)
assert Player('X', 'LEFT', 2).scores_for(b) == [0.0, 0.0, 0.0, 50.0, 0.0, 0.0, 0.0]

# 3-ply lookahead ziet indirecte overwinningen
# ('X' ziet dat kolom 3 een overwinning oplevert!)
assert Player('X', 'LEFT', 3).scores_for(b) == [0.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.0]

# Bij 3-ply ziet 'O' nog geen gevaar
# als hij in een andere kolom speelt
assert Player('O', 'LEFT', 3).scores_for(b) == [50.0, 50.0, 50.0, 100.0, 50.0, 50.0, 50.0]

# Maar bij 4-ply ziet 'O' wel het gevaar!
# weer jammer dat het niet de beurt van 'O' is...
assert Player('O', 'LEFT', 4).scores_for(b) == [0.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.0]

