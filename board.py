class Board:
    def __init__(self):
        self.size = 9
        self.board = [
            [0,4,0,0,0,0,6,8,5],
            [6,0,2,0,9,8,0,0,0],
            [0,5,0,7,6,4,0,1,0],
            [0,9,0,0,0,7,0,6,8],
            [0,6,7,9,0,5,0,4,2],
            [5,2,4,6,0,3,0,0,7],
            [0,0,0,0,0,9,0,0,0],
            [4,0,0,0,7,1,0,0,6],
            [9,8,0,0,5,0,4,0,0]
        ]

    def show(self):
        for row in range(self.size):
            if row % 3 == 0 and row != 0:
                row_text = ""
                # every number 3 dashes -> 3 * 9 = 27
                # plus 6 => 33
                for _ in range(33):
                    row_text += "-"
                print(row_text)
            row_text = ""
            for column in range(self.size):
                if column % 3 == 0 and column != 0:
                    row_text += " | "
                number = self.board[row][column]
                if number:
                    row_text += " "+str(number)+" "
                else:
                    row_text += "   "
            print(row_text)