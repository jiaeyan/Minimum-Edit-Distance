from numpy import zeros
'''
 target:      e   x   e   c   u   t   i   o   n --> x-axis: if len(src) = 0, to grow into tgt, just keep inserting, which costs 1 each
 source:   0  1   2   3   4   5   6   7   8   9
         i 1  2   3                             --> diagonal: if len(src) == len(tgt) but totally different chars at each point, just keep replacing, which costs 2 each; otherwise add 0
         n 2  3   4
         t 3  4       6
         e 4              8
         n 5                 10
         t 6                     12
         i 7                         12
         o 8
         n 9                                  ? --> this value is the total cost of converting src to tgt, the output
         --> y-axis: if len(tgt) = 0, just delete chars from src, which costs 1 each
         
         In all: --> means inserting to src, +1; down means deleting from src, +1; diagonal means replaces src with tgt, +2.
         Each cell is the best path for current lengths of src and tgt, e.g.: D[i, j] is the lowest cost for converting substrings from src[:i] to tgt[:j].
         
         Initialize x and y-axis, then fill in diagonal cells. For each diagonal cell, 
         choose the min values from 3 options: the one above it + 1, the one left of it + 1, and the one on the left upper corner of it + x, where x = 2 or 0.
         1. the one above it + 1: delete from src
         2. the one left to it + 1: insert to src
         3. the one at the left upper corner + x: replace src[i] with tgt[j], x = 0 if the two chars are the same, 2 if not.
         
         We use "_" to represent insert or delete position.
'''


class MinEditDistance():
    
    def __init__(self, insert_cost = 1, 
                       delete_cost = 1, 
                       substitute_cost = 2):
        self.i = insert_cost
        self.d = delete_cost
        self.s = substitute_cost

    def mincost(self, source = None, target = None):
        m = len(source) + 1
        n = len(target) + 1                       #additional 1 is for 0 len for each string
        M = zeros((m, n))                      
        B = zeros(M.shape, dtype = 'int, int')    #backpointer matrix
        for i in range(m):
            for j in range(n):
                if i == 0:
                    M[i, j] = j
                elif j == 0:
                    M[i, j] = i
                else:
                    sub_cost = 0 if source[i-1] == target[j-1] else self.s  #source[i-1] rather source[i] because max(i) = len(source) + 1, to get correct current char in the string, need i - 1
                    M[i, j], B[i, j] = min((M[i-1, j] + self.d, (i-1, j)),
                                           (M[i-1, j-1] + sub_cost, (i-1, j-1)),
                                           (M[i, j-1] + self.i, (i, j-1)))
        print('Cost matrix:\n{}\n\nBacktrace matrix:\n{}\n\nMin cost: {}\n'.format(M, B, M[m-1, n-1]))
        src, tgt = self.alignment("", "", source, target, *B[m-1, n-1], m-1, n-1, B)  #not m, n because m-1, n-1 are max indices of matrices
        print('Source: {}\nTarget: {}'.format(src, tgt))
        return M, B
    
    def alignment(self, src, tgt,        #the result strings to show alignment
                        source, target,  #the input source and target strings
                        i, j,            #[i, j] is the best previous cell of [m, n]
                        m, n, 
                        B): 
        if m == 0 and n == 0:            #the x and y-axis are all (0, 0) along, reach this means reach the beginning
            return src[::-1], tgt[::-1]
        if i + 1 == m and j + 1 == n:    #from left upper corner, replace
            src += source[m-1] 
            tgt += target[n-1] 
        elif i == m and j + 1 == n:      #from left, insert to src, relative src position is empty at first place
            src += '_'
            tgt += target[n-1]         
        elif i + 1 == m and j == n:      #from above, delete from src, relative tgt position is empty at first place
            src += source[m-1]
            tgt += '_'         
        return self.alignment(src, tgt, source, target, *B[i, j], i, j, B)
        
        
    
med = MinEditDistance()
med.mincost("intention", "execution")
