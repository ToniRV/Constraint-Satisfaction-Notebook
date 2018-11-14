# IMPLEMENTATION OF AC3 ALGORITHM

import queue
# CLASS DESCRIPTION FOR CSP

# INCLUDES THE HELPER FUNCTIONS AND VARIABLES USED BY THE PROGRAM


digits =  cols = "123456789"
rows = "ABCDEFGHI"


#FINDING THE CROSS PRODUCT OF TWO SETS 
def cross(A, B):
	return [a + b for a in A for b in B]

squares = cross(rows, cols)

class csp:
	
	#INITIALIZING THE CSP
	def __init__ (self, domain = digits, grid = ""):
		self.variables = squares
		self.domain = self.getDict(grid)
		self.values = self.getDict(grid)		


		'''
			Unitlist consists of the 27 lists of peers 
			Units is a dictionary consisting of the keys and the corresponding lists of peers 
			Peers is a dictionary consisting of the 81 keys and the corresponding set of 20 peers 
			Constraints denote the various all-different constraints between the variables 
		'''

		self.unitlist = ([cross(rows, c) for c in cols] +
            			 [cross(r, cols) for r in rows] +
            			 [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

		self.units = dict((s, [u for u in self.unitlist if s in u]) for s in squares)
		self.peers = dict((s, set(sum(self.units[s],[]))-set([s])) for s in squares)
		self.constraints = {(variable, peer) for variable in self.variables for peer in self.peers[variable]}




	#GETTING THE STRING AS INPUT AND RETURNING THE CORRESPONDING DICTIONARY
	def getDict(self, grid=""):
		i = 0
		values = dict()
		for cell in self.variables:
			if grid[i]!='0':
				values[cell] = grid[i]
			else:
				values[cell] = digits
			i = i + 1
		return values

#THE MAIN AC-3 ALGORITHM
def AC3(csp):
	q = queue.Queue()

	for arc in csp.constraints:
		q.put(arc)

	i = 0
	while not q.empty():
		(Xi, Xj) = q.get()

		i = i + 1 

		if Revise(csp, Xi, Xj):
			if len(csp.values[Xi]) == 0:
				return False

			for Xk in (csp.peers[Xi] - set(Xj)):
				q.put((Xk, Xi))

	#display(csp.values)
	return csp.values



#WORKING OF THE REVISE ALGORITHM
def Revise(csp, Xi, Xj):
	revised = False
	values = set(csp.values[Xi])

	for x in values:
		if not isconsistent(csp, x, Xi, Xj):
			csp.values[Xi] = csp.values[Xi].replace(x, '')
			revised = True 

	return revised 



#CHECKS IF THE GIVEN ASSIGNMENT IS CONSISTENT
def isconsistent(csp, x, Xi, Xj):
	for y in csp.values[Xj]:
		if Xj in csp.peers[Xi] and y!=x:
			return True

	return False


#DISPLAYS THE SUDOKU IN THE GRID FORMAT
def display(values):
    for r in rows:
    	if r in 'DG':
    		print ("------------------------------------------------------------------------------")
    	for c in cols:
    		if c in '47':
    			print (' | ', values[r+c], ' ',end=' ')
    		else:
    			print (values[r+c], ' ',end=' ')
    	print (end='\n')

        

#CHECKS IF THE SUDOKU IS COMPLETE OR NOT
def isComplete(csp):
	for variable in squares:
		if len(csp.values[variable])>1:
			return False
	return True


#WRITES THE SOLVED SUDOKU IN THE FORM OF A STRING
def write(values):
	output = ""
	for variable in squares:
		output = output + values[variable]
	return output
