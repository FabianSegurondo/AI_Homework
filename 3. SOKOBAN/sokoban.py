import curses
PLAYER = ('S', '$')
BOX = ('=', '#')
SPACE = (' ', '|')
WALL = ('@', 'ERROR')
DIR = ((0, -1), (1, 0), (-1, 0), (0, 1))
#      left      down    up       right (hjkl)
# (y, x)
LEVELS = \
"""
@@@@@@@@@@@
@$  =  || @
@= =@= @@@@
@   @  @
@@@@@@@@
---
@@@@@
@S=|@
@@@@@
---
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         @|             |@|||||@
@    ===  @        =      @     @
@|   = =        =             = @
@         @          S    @     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
---
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@S                          @
@  = ||=  ##|   # # = |#| = @
@    # =  # #  =|#  = # |=  @
@ = #| == ||#  =|=|  =|||=  @
@                           @
@                           @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
---
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@||||||||||||||||||||||||||||||||||||||||||||||||||||@@@
@======================== ===========================  @
@S                                                     @
@ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @
@ =                                                   @@
@ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@         @@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
---
@@@@@@@@@@@@@@@@@@@@@@@@@
@|  ==  =============  =@
@@  ==                 =@
@   ==  =============  =@
@  @==  =flex========  =@
@       =====S=        =@
@@  =====Tape=======   =@
@@@@@@@@@@@@@@@@@@@@@@@@@
---
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@|||||||||||||||||||||||||||@
@                           @
@    ==   ===   = =   ===   @
@    =   =   =  ==   =   =  @
@   ==    ===   = =   ===   @
@                           @
@@@@@@@@@@@@@ S @@@@@@@@@@@@@
            @@@@@
""".split('---')
class Soko:
  def __init__(self, level=False):
    self.won = False
    self.moves = 0
    self.rows = []
    self.width = 0
    self.boxes = set()
    if level:
      for line in level.split('\n'):
        self.width = max(len(line), self.width)
        l = []
        for ch in line:
          l.append(ch)
        self.rows.append(l)
    else:
      while True:
        line = get()
        if len(line) == 0: break;
      
        l = []
        for ch in line: l.append(ch);
        self.rows.append(l)
    for rown in range(len(self.rows)):
      for coln in range(len(self.rows[rown])):
        ch = self.rows[rown][coln]
        if ch == PLAYER[0] or ch == PLAYER[1]:
          self.player = (rown, coln, PLAYER.index(ch))
        if ch == BOX[0] or ch == BOX[1]:
          self.boxes.add((rown, coln))
  def view(self):
    for row in self.rows:
      for ch in row:
        print(ch, end='')
      print('')
  def at(self, pair):
    return self.rows[pair[0]][pair[1]]
  def setat(self, pair, new):
    self.rows[pair[0]][pair[1]] = new
  def play(self, get=input, out=print):
    """play sokoban, with line-buffered commands"""
    lines = 0
    out("enter a line with moves of hjkl or q to exit")
    out("box:", BOX[0], "player:", PLAYER[0], \
        "goal:", SPACE[1], "wall:", WALL[0])
    while True:
      self.view()
      out('hjklq>', end=' ')
      i = get()
      lines += 1
      for move in i:
        if move == 'q':
          out(" ----")
          return;
        try:
          if self.move(DIR['hjkl'.index(move)]):
            out("You win -- in", self.moves, "moves and", lines, "lines" )
            return
        except ValueError:
          out("Invalid move: " + move)
  def win(self):
    if self.at(self.player) == PLAYER[1]:
      return False
    for row in self.rows:
      for ch in row:
        if ch == SPACE[1]:
          return False
    return True
  def move(self, dir):
    """soko.move( (x, y) ) --> has won"""
    old = self.player
    new = (old[0] + dir[0], old[1] + dir[1])
    if (self.at(new) in SPACE) or \
       ((new in self.boxes) and self.push(new, dir)):
      self.moves += 1
      goalatnew = SPACE.index(self.at(new))
      self.setat(new, PLAYER[goalatnew])
      self.setat(old, SPACE[self.player[2]])
      self.player = new + tuple([goalatnew])
      return self.won
    return False
  def push(self, old, dir):
    new = (old[0] + dir[0], old[1] + dir[1])
    try:
      goalatnew = SPACE.index(self.at(new))
      self.setat(old, SPACE[BOX.index(self.at(old))])
      self.boxes.discard(old)
      self.setat(new, BOX[goalatnew])
      self.boxes.add(new)
      self.won = self.win()
      # checking here if won because the winning move must be a push
      return True
    except ValueError:
      return False # new is not a space, can't move
  def tostring(self):
    s = ""
    for row in self.rows:
      for ch in row:
        s += ch
      s += "\n"
    return s
  def play_curses(self):
    try:
      curses.initscr()
      curses.cbreak()
      curses.noecho()
      height = len(self.rows)
      win = curses.newwin(height+5, max(self.width+1, 36))
      # self.width + 5 so it can fit the newline.
      # height+5 to fit any error/information messages
      def paint():
        win.addstr(0, 0, self.tostring())
        win.addstr(height, 0, \
                   "box: "+BOX[0]+   " player: "+PLAYER[0]+ \
                   "goal: "+SPACE[1]+" wall: "+WALL[0])
        win.addstr(height+1, 0, "enter a move of hjkl or q to exit")
        win.refresh()
      win.clear()
      while True:
        paint()
        move = win.getkey()
        win.clear()
        if move == 'q':
          return
        dirnum = False
        try:
          dirnum = 'hjkl'.index(move)
        except ValueError:
          win.addstr(height+2, 0, "Invalid move: " + move)
          continue
        if self.move(DIR[dirnum]):
          paint()
          win.addstr(height+2, 0, "You win -- in %d moves" % self.moves)
          win.refresh()
          win.getkey()
          return
    finally:
      curses.endwin()
def play(curses=True):
  while True:
    print("Select a level, 0 to", len(LEVELS)-1, end="\nlevel or q> ")
    try:
      s = input()
      s = Soko(LEVELS[int(s)])
    except IndexError:
      print("INVALIDNUMBER!")
      continue
    except (ValueError, EOFError):
      print("Goodbye.")
      break
    except TypeError:
      print("There was a problem with that level.")
      continue
    if curses:
      s.play_curses()
    else:
      s.play()
if True:
   pass;