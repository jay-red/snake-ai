"""
Classic snake game implemented by Jared Flores
"""

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint, randrange
from math import atan, pi, sqrt
import numpy as np 

class SnakeGame():
	def __init__( self, render = False ):
		self.reset( render )
	def step( self, action ):
		ACTION_UP = 0
		ACTION_RIGHT = 1
		ACTION_DOWN = 2
		ACTION_LEFT = 3

		FOOD_THRESHOLD = 500

		if self.render:
			self.win.border( 0 )
			#self.win.addstr( 0, 2, bodyDebug )
			self.win.addstr( 0, 2, 'Score : ' + str( self.score ) + ' ' )
			#self.win.addstr( 0, 2, str( observation[ 0 ] ) + ' ' + str( observation[ 1 ] ) + ' ' + str( observation[ 2 ] ) + ' ' + str( observation[ 3 ] ) + ' ' )
			#self.win.addstr( 0, 2, str( self.snake[ 0 ][ 0 ] ) + ', ' + str( self.snake[ 0 ][ 1 ] ) + ' ' )
			self.win.addstr( 0, 27, ' SNAKE ' )
			self.win.timeout( 150 - ( len( self.snake ) / 5 + len( self.snake ) / 10 ) % 120 )
			#self.win.timeout( 1000 )

		"""
			Actions:
				Type: Discrete(4)
				Num		Action
				0		Up
				1		Right
				2		Downs
				3		Left
		"""
		head = self.snake[ 0 ]
		lastO = head[ 0 ] - self.food[ 0 ]
		lastA = head[ 1 ] - self.food[ 1 ]

		horizontalAdd = 0
		verticalAdd = 0

		if self.lastAction % 2 == action % 2 and len( self.snake ) > 1:
			action = self.lastAction

		if action == ACTION_UP:
			verticalAdd = -1
		elif action == ACTION_RIGHT:
			horizontalAdd = 1
		elif action == ACTION_DOWN:
			verticalAdd = 1
		elif action == ACTION_LEFT:
			horizontalAdd = -1

		self.lastAction = action

		self.snake.insert( 0, [ self.snake[ 0 ][ 0 ] + verticalAdd, self.snake[ 0 ][ 1 ] + horizontalAdd ] )

		if self.snake[ 0 ][ 0 ] == 0 or self.snake[ 0 ][ 0 ] == 19 or self.snake[ 0 ][ 1 ] == 0 or self.snake[ 0 ][ 1 ] == 59:
			self.close()
			return None, -1, self.alive

		if self.snake[ 0 ] in self.snake[ 1 : ]:
			self.close()
			return None, -1, self.alive

		if self.lastFood > FOOD_THRESHOLD:
			self.close()
			return None, -1, self.alive

		observation = self.getState()
		if self.render: self.win.addstr( 0, 2, str( observation[ 0 ] ) + ' ' + str( observation[ 1 ] ) + ' ' + str( observation[ 2 ] ) + ' ' + str( observation[ 3 ] ) + ' ' )
			#self.win.addstr( 0, 2, str( self.snake[ 0 ][ 0 ] ) + ', ' + str( self.snake[ 0 ][ 1 ] ) + ' ' )
		reward = 1
		
		
		if( abs( self.o ) - abs( lastO ) > 0 ):
			reward = 0
		if( abs( self.a ) - abs( lastA ) > 0 ):
			reward = 0
		# """
		if self.snake[ 0 ] == self.food:
			self.map[ self.food[ 0 ] - 1 ][ self.food[ 1 ] - 1 ] = 0
			self.lastFood = 0
			self.food = []
			self.score += 3
			reward = 3
			reward = FOOD_THRESHOLD
			while self.food == []:
				self.food = [ randint( 1, 18 ), randint( 1, 58 ) ]
				if self.food in self.snake: self.food = []
			if self.render: self.win.addch( self.food[ 0 ], self.food[ 1 ], '*' )
			self.map[ self.food[ 0 ] - 1 ][ self.food[ 1 ] - 1 ] = 2	
			if len( self.snake ) >= 2:
				last = self.snake.pop()
				secLast = self.snake.pop()
				self.snake.append( secLast )
				self.snake.append( last )
				if last[ 0 ] - secLast[ 0 ] < 0:
					self.bodyDebug = "up"
					seg1 = [ last[ 0 ] - 1, last[ 1 ] ]
					seg2 = [ last[ 0 ] - 2, last[ 1 ] ]
					seg3 = [ last[ 0 ] - 3, last[ 1 ] ]
				elif last[ 0 ] - secLast[ 0 ] > 0:
					self.bodyDebug = "down"
					seg1 = [ last[ 0 ] + 1, last[ 1 ] ]
					seg2 = [ last[ 0 ] + 2, last[ 1 ] ]
					seg3 = [ last[ 0 ] + 3, last[ 1 ] ]
				elif last[ 1 ] - secLast[ 1 ] < 0:
					self.bodyDebug = "right"
					seg1 = [ last[ 0 ], last[ 1 ] - 1 ]
					seg2 = [ last[ 0 ], last[ 1 ] - 2 ]
					seg3 = [ last[ 0 ], last[ 1 ] - 3 ]
				elif last[ 1 ] - secLast[ 1 ] > 0:
					self.bodyDebug = "left"
					seg1 = [ last[ 0 ], last[ 1 ] + 1 ]
					seg2 = [ last[ 0 ], last[ 1 ] + 2 ]
					seg3 = [ last[ 0 ], last[ 1 ] + 3 ]
				if self.render:
					try:
						self.win.addch( seg1[ 0 ], seg1[ 1 ], '#' )
					except:
						pass
					try:
						self.win.addch( seg2[ 0 ], seg2[ 1 ], '#' )
					except:
						pass
					try:
						self.win.addch( seg3[ 0 ], seg3[ 1 ], '#' )
					except:
						pass
				self.snake.append( seg1 )
				self.snake.append( seg2 )
				self.snake.append( seg3 )
				if seg1[ 0 ] > 0 and seg1[ 1 ] > 0 and seg1[ 0 ] < 19 and seg1[ 1 ] < 59: self.map[ seg1[ 0 ] - 1 ][ seg1[ 1 ] - 1 ] = 1
				if seg2[ 0 ] > 0 and seg2[ 1 ] > 0 and seg2[ 0 ] < 19 and seg2[ 1 ] < 59: self.map[ seg2[ 0 ] - 1 ][ seg2[ 1 ] - 1 ] = 1
				if seg3[ 0 ] > 0 and seg3[ 1 ] > 0 and seg3[ 0 ] < 19 and seg3[ 1 ] < 59: self.map[ seg3[ 0 ] - 1 ][ seg3[ 1 ] - 1 ] = 1
		else:	
			last = self.snake.pop()
			try:
				self.map[ last[ 0 ] - 1 ][ last[ 1 ] - 1 ] = 0
			except:
				pass
			if self.render: self.win.addch( last[ 0 ], last[ 1 ], ' ' )
		if self.render: self.win.addch( self.snake[ 0 ][ 0 ], self.snake[ 0 ][ 1 ], '#' )
		
		self.score += reward
		self.lastFood += 1
		return observation, reward, self.alive

	def cleanMap( self ):
		self.map = []
		for _ in range( 18 ):
			row = []
			for _ in range( 58 ):
				row.append( 0 )
			self.map.append( row )

	def reset( self, render = False ):
		self.score = 0
		self.snake = [ [ randint( 4, 14 ), randint( 4, 54 ) ] ]
		#self.snake.append( [ self.snake[ 0 ][ 0 ] - 1, self.snake[ 0 ][ 1 ] ] )
		#self.snake.append( [ self.snake[ 0 ][ 0 ] - 2, self.snake[ 0 ][ 1 ] ] )
		self.alive = True
		self.food = []
		while self.food == []:
			self.food = [ randint( 1, 18 ), randint( 1, 58 ) ]
			if self.food in self.snake: self.food = []
		self.o = 0
		self.a = 0
		self.bodyDebug = ""
		self.state = None
		self.render = render
		self.lastAction = 2
		self.lastFood = 0
		self.stepsAlive = 0
		self.map = []
		self.cleanMap()
		if render:
			curses.initscr()
			self.win = curses.newwin( 20, 60, 0, 0 )
			self.win.keypad( 1 )
			curses.noecho()
			curses.curs_set( 0 )
			self.win.border( 0 )
			self.win.nodelay( 1 )
			self.win.addch( self.food[ 0 ], self.food[ 1 ], '*' )

	def sample( self ):
		action = randrange( 0, 4 )
		if self.lastAction % 2 == action % 2 and len( self.snake ) > 1:
			action = self.lastAction
		return action

	def getState( self ):
		for segment in self.snake:
			try:
				self.map[ segment[ 0 ] - 1 ][ segment[ 1 ] - 1 ] = 1
			except:
				pass
		self.map[ self.food[ 0 ] - 1 ][ self.food[ 1 ] - 1 ] = 2

		head = self.snake[ 0 ]

		"""upWall = head[ 0 ]
		rightWall = 59 - head[ 1 ]
		downWall = 19 - head[ 0 ]
		leftWall = head[ 1 ]

		upSeg = -1
		rightSeg = -1
		downSeg = -1
		leftSeg = -1

		upFood = -1
		rightFood = -1
		downFood = -1
		leftFood = -1

		rightSegFound = False
		downSegFound = False

		horizontalPos = head[ 1 ] - 1
		verticalPos = head[ 0 ] - 1
		for i in range( 58 ):
			if not i == horizontalPos:
				entry = self.map[ verticalPos ][ i ]
				if entry == 1:
					if i < horizontalPos:
						leftSeg = horizontalPos - i
					elif not rightSegFound:
						rightSeg = i - horizontalPos
						rightSegFound = True
				elif entry == 2:
					if i < horizontalPos:
						leftFood = horizontalPos - i
					else:
						rightFood = i - horizontalPos

		for j in range( 18 ):
			if not j == verticalPos:
				entry = self.map[ j ][ horizontalPos ]
				if entry == 1:
					if j < verticalPos:
						upSeg = verticalPos - j
					elif not downSegFound:
						downSeg = j - verticalPos
						downSegFound = True
				elif entry == 2:
					if j < verticalPos:
						upFood = verticalPos - j
					else:
						downFood = j - verticalPos"""

		upObstacle = 0
		rightObstacle = 0
		downObstacle = 0
		leftObstacle = 0
		headTop = head[ 0 ] - 1
		headLeft = head[ 1 ] - 1
		self.o = head[ 0 ] - self.food[ 0 ]
		self.a = head[ 1 ] - self.food[ 1 ]
		distance = sqrt( pow( self.o, 2 ) + pow( self.a, 2 ) )
		theta = 0
		if self.o == 0:
			if self.a < 0:
				theta = pi
			else:
				theta = 0
		elif self.a == 0:
			if self.o < 0:
				theta = 3 * pi / 2
			else:
				theta = pi / 2
		else:
			theta = atan( abs( self.o ) / abs( self.a ) )
			if self.o < 0 and self.a > 0:
				theta = 2 * pi - theta
			elif self.o < 0 and self.a < 0:
				theta += pi
			elif self.o > 0 and self.a < 0:
				theta = pi - theta
		theta = theta / ( 2 * pi )
		distance = distance / ( sqrt( pow( 58, 2 ) + pow( 18, 2 ) ) )
		if headTop >= 1:
			entry = self.map[ headTop - 1 ][ headLeft ]
			if entry == 1 and not self.lastAction == 2:
				upObstacle = 1
		else:
			upObstacle = 1
		if headTop < 17:
			entry = self.map[ headTop + 1 ][ headLeft ]
			if entry == 1 and not self.lastAction == 0:
				downObstacle = 1
		else:
			downObstacle = 1
		if headLeft >= 1:
			entry = self.map[ headTop ][ headLeft - 1 ]
			if entry == 1 and not self.lastAction == 1:
				leftObstacle = 1
		else:
			leftObstacle = 1
		if headLeft < 57:
			entry = self.map[ headTop ][ headLeft + 1 ]
			if entry == 1 and not self.lastAction == 3:
				rightObstacle = 1
		else:
			rightObstacle = 1

		#return np.array( ( upWall, rightWall, downWall, leftWall, upSeg, rightSeg, downSeg, leftSeg, upFood, rightFood, downFood, leftFood ) )
		return np.array( ( upObstacle, rightObstacle, downObstacle, leftObstacle, self.o, self.a ) )

	def getWindow( self ):
		if self.render:
			return self.win
		else:
			return None

	def close( self ):
		self.alive = False
		if self.render:
			curses.endwin()
		#print( "\nScore - " + str( self.score ) )