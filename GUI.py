from tkinter import *
from tkinter import font
from fractions import Fraction
import copy

class Calc():
    def __init__(self):
        self.internal_line = f''
        self.counter = 1
        self.display_items = []
        self.internal_items = []
        self.digit_ended = False
        self.prev_digit_ended = False
        
        
class Matrix():
    def __init__(self, num_rows, num_cols, inter_created = False, inter_rows = []):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.rows = []
        self.cols = []
        self.inter_created = inter_created
        self.rows = inter_rows
        self.create_cols()
        
    def create_cols(self):
        '''
        (Matrix) -> (None)

        Creates columns based on the given rows.
        '''
        for i in range(self.num_cols):
            col = []
            for row in self.rows:
                col.append(row[i])
            self.cols.append(col)

    def __repr__(self):
        '''
        (Matrix) -> (String)

        Returns the representation of a matrix.
        '''
        s = 'Matrix('
        for row in self.rows:
                s+= str(row) + ', '
        s = s[:-2] + ')'
        return s

    def __str__(self):
        '''
        (Matrix) -> String

        Returns the string representation of a matrix.
        '''
        s = ''
        for row in self.rows:
            for item in row:
                s += str(item)+ ' '
            s+= '\n'
        return s[:-1]


    def __eq__(self, other):
        '''
        (Matrix, Matrix) -> Boolean

        Returns true is both matrices are the same and false if they are not the same.
        '''
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            return False

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.rows[i][j] != other.rows[i][j]:
                    return False
        return True
    
    
    def __mul__(self, other):
        '''
        (Matrix, int or float or Fraction or Matrix) -> Exception or Matrix

        Returns a new matrix multipled by the other given argument or raises an exception if 2
        matrices cannot be multipled.
        '''
        if type(other) == int or type(other) == float or type(other) == Fraction:
            rows = []
            for row in self.rows:
                new_matrix_rows = []
                for entry in row:
                    new_matrix_rows.append(entry * other)
                rows.append(new_matrix_rows)
            return Matrix(self.num_rows, self.num_cols, True,rows)

        if self.num_cols != other.num_rows:
            raise Exception('Dimensions of matrices are not the same')

        rows = []
        for i in range(self.num_rows):
            new_matrix_row = []
            for j in range(other.num_cols):
                entry_sum = 0
                for z in range(self.num_cols):
                    entry_sum += self.rows[i][z] * other.cols[j][z]
                new_matrix_row.append(entry_sum)
            rows.append(new_matrix_row)
        return Matrix(self.num_rows, other.num_cols, True, rows)

    def __rmul__(self, other):
        '''
        (Matrix, int or float or Fraction or Matrix) -> Exception or Matrix

        Returns a new matrix multipled by the other given argument or raises an exception if 2
        matrices cannot be multipled.
        '''
        return Matrix.__mul__(self, other)

    def __pow__(self, exp):
        a = copy.deepcopy(self)
        for i in range(exp-1):
            a = Matrix.__mul__(a,self)
        return a
            

    def __add__(self, other):
        '''
        (Matrix, Matrix) -> Exception or Matrix

        Returns new matrix if the arguments can be added. If not an exception will be raised.
        '''
        if self.num_cols != other.num_cols or self.num_rows != other.num_rows:
            raise Exception('Dimensions of matrices are not the same.')

        rows = []
        for i in range(self.num_rows):
            new_matrix_rows = []
            for j in range(self.num_cols):
                new_matrix_rows.append(self.rows[i][j] + other.rows[i][j])
            rows.append(new_matrix_rows)
        return Matrix(self.num_rows, self.num_cols, True, rows)

    def __sub__(self, other):
        '''
        (Matrix, Matrix) -> Exception or Matrix

        Returns new matrix if the arguments can be subtracted. If not an exception will be raised.
        '''
        return Matrix.__add__(self, Matrix.__mul__(other, -1))

    def find_pivot(self, z=0, w=0):
        '''
        (Matrix, int, int) -> Tuple or None

        Given a matrix, the function will return a tuple containing the coordinates of the first
        pivot starting from (z, w) or None if no pivots are found from (z, w).

        '''
        for i in range(z, self.num_cols):
            for j in range(w, self.num_rows):
                if self.rows[j][i] != 0:
                    return (j, i)
        
    def swap_rows(self, row1, row2):
        '''
        (Matrix, int, int) -> None

        Swap 2 rows in a given matrix.
        '''
        self.rows[row1], self.rows[row2] = self.rows[row2], self.rows[row1]

    def scale_row(self, row_num, k):
        '''
        (Matrix, int, int or float or fraction) -> None

        Will multiply given row by k.
        '''
        for i in range(self.num_cols):
            self.rows[row_num][i] *= k

    def add_rows(self, row1, row2, k=1):
        '''
        (Matrix, int, int, float or int or fraction) -> None

        Will add k times row2 to row1. 
        '''
        for i in range(self.num_cols):
            self.rows[row1][i] += k*self.rows[row2][i]

    def sub_rows(self, row1, row2, k=1):
        '''
        (Matrix, int, int, float or int or fraction) -> None

        Will subtract k times row2 from row1.
        '''
        for i in range(self.num_cols):
            self.rows[row1][i] -= k*self.rows[row2][i]

    def ref(self):
        '''
        (Matrix) -> None

        Will convert the given matrix is Row Echelon Form.
        '''
        tmp_matrix = copy.deepcopy(self)
        i = 0
        j = 0
        while i < tmp_matrix.num_rows and j < tmp_matrix.num_cols:
            piv = tmp_matrix.find_pivot(i, j)
            if not piv:
                break
            piv_row, piv_col = piv
            tmp_matrix.swap_rows(piv_row, i)
            piv_row = i
            j = piv_col

            if tmp_matrix.rows[piv_row][piv_col] > 0:
                const = Fraction(Fraction('1/1')/Fraction(tmp_matrix.rows[piv_row][piv_col]))
            elif tmp_matrix.rows[i][j] < 0:
                const = Fraction(Fraction('-1/1')/Fraction(-tmp_matrix.rows[piv_row][piv_col]))
            else:
                const = Fraction('0/1')
                
            tmp_matrix.scale_row(i, const)
            for z in range(i+1, tmp_matrix.num_rows):
                if tmp_matrix.rows[z][j] > 0:
                    tmp_matrix.sub_rows(z, i, tmp_matrix.rows[z][j])
                elif tmp_matrix.rows[z][j] < 0:
                    tmp_matrix.add_rows(z, i, -tmp_matrix.rows[z][j])
            i += 1
            j += 1

        for h in range(tmp_matrix.num_rows):
            for k in range(tmp_matrix.num_cols):
                if tmp_matrix.rows[h][k] == 0:
                    tmp_matrix.rows[h][k] = abs(tmp_matrix.rows[h][k])

        return tmp_matrix

    def rref(self):
        '''
        (Matrix)

        Will convert the given matrix to Reduced Row Echelon Form.
        '''
        tmp_matrix = copy.deepcopy(self)
        i = 0
        j = 0
        while i < tmp_matrix.num_rows and j < tmp_matrix.num_cols:
            piv = tmp_matrix.find_pivot(i, j)
            if not piv:
                break
            piv_row, piv_col = piv
            tmp_matrix.swap_rows(piv_row, i)
            piv_row = i
            j = piv_col

            if tmp_matrix.rows[piv_row][piv_col] > 0:
                const = Fraction(Fraction('1/1')/Fraction(tmp_matrix.rows[piv_row][piv_col]))
            elif tmp_matrix.rows[piv_row][piv_col] < 0:
                const = Fraction(Fraction('-1/1')/Fraction(-tmp_matrix.rows[piv_row][piv_col]))
            else:
                const = Fraction('0/1')
                
            tmp_matrix.scale_row(i, const)
            for z in range(tmp_matrix.num_rows):
                if z == i:
                    continue
                if tmp_matrix.rows[z][j] > 0:
                    tmp_matrix.sub_rows(z, i, tmp_matrix.rows[z][j])
                elif tmp_matrix.rows[z][j] < 0:
                    tmp_matrix.add_rows(z, i, -tmp_matrix.rows[z][j])
            i += 1
            j += 1

        for h in range(tmp_matrix.num_rows):
            for k in range(tmp_matrix.num_cols):
                if tmp_matrix.rows[h][k] == 0:
                    tmp_matrix.rows[h][k] = abs(tmp_matrix.rows[h][k])

        return tmp_matrix

    def is_square(self):
        '''
        (Matrix) -> Boolean

        Returns True if matrix is a sqaure matrix and False if matrix isn't a square matrix.
        '''
        return self.num_rows == self.num_cols        

    def determinant(self):        
        '''
        (Matrix) -> Exception or Fraction

        Returns the determinant of the matrix or raises an exception if the matrix is not a sqaure.
        '''
        row_swaps = 0
        total_scale = 1
        temp_matrix = copy.deepcopy(self)

        if not temp_matrix.is_square():
            raise Exception('Can\'t compute determinant of a non square matrix')

        i = 0
        j = 0
        while i < temp_matrix.num_rows and j < temp_matrix.num_cols:
            piv = temp_matrix.find_pivot(i, j)
            if not piv:
                break
            piv_row, piv_col = piv

            if piv_row != i:
                temp_matrix.swap_rows(piv_row, i)
                row_swaps += 1
                piv_row = i
                j = piv_col

            if temp_matrix.rows[piv_row][piv_col] > 0:
                const = Fraction(Fraction('1/1')/Fraction(temp_matrix.rows[piv_row][piv_col]))
            elif temp_matrix.rows[i][j] < 0:
                const = Fraction(Fraction('-1/1')/Fraction(-temp_matrix.rows[piv_row][piv_col]))
            else:
                const = Fraction('0/1')
                
            if const != 1:
                temp_matrix.scale_row(i, const)
                total_scale *= const
            
            for z in range(i+1, temp_matrix.num_rows):
                if temp_matrix.rows[z][j] > 0:
                    temp_matrix.sub_rows(z, i, temp_matrix.rows[z][j])
                elif temp_matrix.rows[z][j] < 0:
                    temp_matrix.add_rows(z, i, -temp_matrix.rows[z][j])
            i += 1
            j += 1

        for i in range(temp_matrix.num_rows):
                if temp_matrix.rows[i][i] != 1:
                    return 0
        return (1/total_scale) * (-1)**(row_swaps)

         
Calculator = Calc()
class Window(Frame):

    widgets= {}
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        
        
    
    def init_window(self):
        self.master.title("Matrix Calculator")

        self.widgets['display']= Frame(self.master, height=230, width=790, bg='white', highlightbackground="black", highlightthickness=1)
        self.widgets['display'].pack_propagate(0)
        
        widget_nameandsym = {
                "add":"+",
                'sub':'_',
                'div':'/',
                'mult':'x',
                'power':'^',
                'det':'det',
                'rref':"RREF",
                'ref':'REF',
                'equal':'=',
                'creatematrix':'Create\nMatrix',
                'clear': 'Clear',
                'backspace': '<---',
                '1':'1',
                '2':'2',
                '3':'3',
                '4':'4',
                '5':'5',
                '6':'6',
                '7':'7',
                '8':'8',
                '9':'9',
                '0':'0'
            }
        for name in widget_nameandsym:
            self.widgets[name]=Button(self.master, text=f"{widget_nameandsym[name]}", height=5, width=13)

        self.widgets['1']['bg'] = 'white'
        self.widgets['2']['bg'] = 'white'
        self.widgets['3']['bg'] = 'white'
        self.widgets['4']['bg'] = 'white'
        self.widgets['5']['bg'] = 'white'
        self.widgets['6']['bg'] = 'white'
        self.widgets['7']['bg'] = 'white'
        self.widgets['8']['bg'] = 'white'
        self.widgets['9']['bg'] = 'white'
        self.widgets['0']['bg'] = 'white'

        self.widgets['display'].grid(row=0, column=0, columnspan=7, padx=5, pady=2)
        self.widgets['creatematrix'].grid(row=2, column=0,rowspan =2, sticky=N, pady=2)
        self.widgets['creatematrix']['height'] = 11
        self.widgets['clear']['width'] = 62
        self.widgets['clear'].grid(row=1, column=0, columnspan =4, sticky=N, pady=2)
        self.widgets['backspace'].grid(row=4, column=0,sticky=N, pady=2)
        self.widgets['add'].grid(row=2, column=1,sticky=N, pady=2)
        self.widgets['sub'].grid(row=2, column=2,sticky=N, pady=2)
        self.widgets['div'].grid(row=2, column=3,sticky=N, pady=2)
        self.widgets['mult'].grid(row=3, column=1, sticky=N, pady=2)
        self.widgets['power'].grid(row=3, column=2,sticky=N, pady=2)
        self.widgets['det'].grid(row=3, column=3,sticky=N, pady=2)
        self.widgets['rref'].grid(row=4, column=1, sticky=N, pady=2)
        self.widgets['ref'].grid(row=4, column=2,sticky=N, pady=2)
        self.widgets['equal'].grid(row=4, column=3,sticky=N, pady=2)
        self.widgets['1'].grid(row=2, column=4, sticky=N, pady=2)
        self.widgets['2'].grid(row=2, column=5, sticky=N, pady=2)
        self.widgets['3'].grid(row=2, column=6, sticky=N, pady=2)
        self.widgets['4'].grid(row=3, column=4, sticky=N, pady=2)
        self.widgets['5'].grid(row=3, column=5, sticky=N, pady=2)
        self.widgets['6'].grid(row=3, column=6, sticky=N, pady=2)
        self.widgets['7'].grid(row=4, column=4, sticky=N, pady=2)
        self.widgets['8'].grid(row=4, column=5, sticky=N, pady=2)
        self.widgets['9'].grid(row=4, column=6, sticky=N, pady=2)
        self.widgets['0'].grid(row=1, column=4, columnspan =4, sticky=N, pady=2)
        self.widgets['0']['width'] = 46
        
        
        self.widgets["creatematrix"]["command"] = lambda: self.create_pop_up()
        self.widgets['add']['command'] = lambda: self.add_symbol("+", "+")
        self.widgets['sub']['command'] = lambda: self.add_symbol("-", "-")
        self.widgets['div']['command'] = lambda: self.add_symbol("/", "/")
        self.widgets['mult']['command'] = lambda: self.add_symbol("x", "*")
        self.widgets['power']['command'] = lambda: self.add_symbol("^", "**")
        self.widgets['det']['command'] = lambda: self.matrix_operation("DET" ,'.determinant()')
        self.widgets['rref']['command'] = lambda: self.matrix_operation("RREF", ".rref()")
        self.widgets['ref']['command'] = lambda: self.matrix_operation("REF", ".ref()")
        self.widgets['equal']['command'] = lambda: self.evaluate(Calculator.internal_line)
        self.widgets['clear']['command'] = lambda: self.clear_calculator_line()
        self.widgets['backspace']['command'] = lambda: self.backspace()
        self.widgets['0']['command'] = lambda: [self.add_symbol("0", "0")]
        self.widgets['1']['command'] = lambda: [self.add_symbol("1", "1")]
        self.widgets['2']['command'] = lambda: [self.add_symbol("2", "2")]
        self.widgets['3']['command'] = lambda: [self.add_symbol("3", "3")]
        self.widgets['4']['command'] = lambda: [self.add_symbol("4", "4")]
        self.widgets['5']['command'] = lambda: [self.add_symbol("5", "5")]
        self.widgets['6']['command'] = lambda: [self.add_symbol("6", "6")]
        self.widgets['7']['command'] = lambda: [self.add_symbol("7", "7")]
        self.widgets['8']['command'] = lambda: [self.add_symbol("8", "8")]
        self.widgets['9']['command'] = lambda: [self.add_symbol("9", "9")]
        
        

    def create_pop_up(self):

        def make_rows_cols():

            try:
                rows = int(rowentryvar.get())
                cols = int(colentryvar.get())
                if rows != rowentryvar.get() or cols != colentryvar.get():
                    self.close_window(newwin)
                    self.create_window_err("Invalid Dimensions, Please Retry", self.master)
                else:
                    if rows <=0 or cols <=0:
                        self.close_window(newwin)
                        self.create_window_err("Invalid Dimensions, Please Retry", self.master)
                    else:
                        self.create_matrix_win(rows, cols)
                        
            except:
                self.close_window(newwin)
                self.create_window_err("Invalid Dimensions, Please Retry", self.master)
            
        newwin= Toplevel(self.master)
        newwin.resizable(0, 0)
        x = self.master.winfo_x()
        y= self.master.winfo_y()
        newwin.grab_set()
        newwin.geometry("+%d+%d" %(x+300, y+300))
        rowlabel = Label(newwin, text="Number of Rows:",width=20).grid(row=0, column=0, sticky=E)
        collabel = Label(newwin, text="Number of Columns:", width=20).grid(row=1, column=0,sticky=E)
        

        rowentryvar = DoubleVar(value=0)
        colentryvar = DoubleVar(value=0)
        rowentry = Entry(newwin, width=10,textvariable=rowentryvar)
        rowentry.grid(row=0, column=1, sticky=W)
        colentry = Entry(newwin, width=10,textvariable = colentryvar)
        colentry.grid(row=1,column=1, sticky=W)

        donebutton = Button(newwin, text="Done", width=10, command=lambda: [make_rows_cols(), self.close_window(newwin)])
        donebutton.grid(row=3,column=1, sticky=E)

        exit_button = Button(newwin, text='Exit', width=10, command=lambda: self.close_window(newwin))
        exit_button.grid(row=3, column=0, sticky=W)
        
        
    def create_matrix_win(self, rows, cols):
        create_matrix_win = Toplevel(self.master)
        create_matrix_win.resizable(0, 0)
        create_matrix_win.grab_set()
        x = self.master.winfo_x()
        y= self.master.winfo_y()
        create_matrix_win.geometry("+%d+%d" %(x+300, y+300))
        create_matrix_win.wm_geometry("%dx%d" % (60*cols, 25*(rows+1)))

        def add_matrix(rows, cols):
            entries_input = []
            z=0
            for i in range(rows):
                tmp = []
                for j in range(cols):
                    entry = entries[z]
                    tmp.append(entry.get())
                    z+=1
                entries_input.append(tmp)

            good = True
            for row in entries_input:
                for j in range(len(row)):
                    try:
                        row[j] = float(row[j])
                    except ValueError:
                        good = False
                        break
                if not good:
                    self.create_window_err('Invalid Input. Please Try Again.', self.master)
                    entries_input = []
                    break
                        
            if good:
                tmp_matrix = Matrix(rows, cols, True, entries_input)
                self.add_symbol(f'{str(tmp_matrix)}', f'Matrix({rows},{cols},True,{entries_input})')
            self.display_text()
            
        
        entries = []
        for i in range(rows):
            for j in range(cols):
                entries.append(Entry(create_matrix_win, width=8))

        entries_grid = []
        i=0
        for z in range(rows):
            for j in range(cols):
                entry = entries[i]
                entries_grid.append(entry.grid(column=j, row=z, sticky=W, padx=2, pady=2))
                i+=1
        done_button = Button(create_matrix_win, text="Done", command= lambda: [add_matrix(rows, cols), self.close_window(create_matrix_win)]).grid(row=rows, column=0, columnspan=cols, sticky=W)
    def create_window_err(self, msg, win):
        err_win = Toplevel(win)
        err_win.resizable(0, 0)
        x = win.winfo_x()
        y= win.winfo_y()
        err_win.geometry("+%d+%d" %(x+250, y+300))
        err_win.grab_set()
        err_label = Label(err_win, text = msg, width=50).grid(row=0, column=0, columnspan=3)
        accept_button = Button(err_win, text="Done", width=10, command= lambda: self.close_window(err_win)).grid(row=1, column=1)
        

    def add_symbol(self, disp_symb, inter_symb):
        digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        if disp_symb not in digits:
            Calculator.digit_ended, Calculator.prev_digit_ended = True, Calculator.digit_ended
        else:
            Calculator.digit_ended, Calculator.prev_digit_ended = False, Calculator.digit_ended
            
        if Calculator.digit_ended:
            display_item = " "+disp_symb + ' '
            internal_item =" "+inter_symb + ' '
            Calculator.display_items.append(display_item)
            Calculator.internal_line += internal_item
            Calculator.internal_items.append(internal_item)
        else:
            Calculator.internal_line += inter_symb
            if len(Calculator.display_items) == 0 or Calculator.prev_digit_ended:
                Calculator.display_items.append(disp_symb)
                Calculator.internal_items.append(inter_symb)
            else:
                Calculator.display_items[-1] = str(int(Calculator.display_items[-1])*10 + int(disp_symb))
                Calculator.internal_items[-1] = str(int(Calculator.internal_items[-1])*10 + int(disp_symb))

        self.display_text()


    def display_text(self):
        label_font = font.Font(self.master, family='Arial', size=12, weight='bold')
        for widget in self.widgets['display'].winfo_children():
            widget.destroy()
        labels = []
        for elem in Calculator.display_items:
            labels.append(Label(self.widgets['display'], text = str(elem.strip()), bg='white'))
            

        for label in labels:
            label.pack(side=LEFT, fill='both')
            label.config(font=label_font)

    def matrix_operation(self, display_item, internal_item):
        if len(Calculator.internal_items) == 0:
            Calculator.internal_items.append(internal_item)
            Calculator.display_items.append(display_item)
            Calculator.internal_line += internal_item
        else:
            Calculator.display_items.insert(-2, display_item)
            Calculator.internal_items.append(internal_item)
            Calculator.internal_line += internal_item

        Calculator.digit_ended, Calculator.prev_digit_ended = True, Calculator.digit_ended

        self.display_text()
    def evaluate(self, line):
        print(Calculator.display_items)
        if len(Calculator.internal_items) == 0:
            pass
        elif len(Calculator.internal_items) == 1:
            pass
        else:
            try:
                result = eval(line)
                if type(result) == Matrix:
                    res_matrix = Matrix(result.num_rows,result.num_cols,True,result.rows)
                    result = f'Matrix({result.num_rows},{result.num_cols},True,{result.rows})'
                    Calculator.display_items = [f'{str(res_matrix)}']
                    Calculator.internal_items = [f'{result}']
                    Calculator.internal_line = f'{result}'
                else:
                    Calculator.display_items = [f'{result}']
                    Calculator.internal_items = [f'{result}']
                    Calculator.internal_line = f'{result}'
                self.display_text()
            except:
                self.create_window_err('Invalid Syntax', self.master)

    def clear_calculator_line(self):
        Calculator.internal_line = ''
        Calculator.display_items = []
        Calculator.internal_items = []
        self.display_text()

    def backspace(self):
        digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        if len(Calculator.internal_items) ==0:
            pass
        else:
            if Calculator.internal_items[-1] in ['.ref()', '.rref()', '.determinant()']:
                if Calculator.internal_items[-1] == '.ref()':
                    del Calculator.display_items[len(Calculator.display_items)-1-Calculator.display_items[::-1].index('REF')]
                elif Calculator.internal_items[-1] == '.rref()':
                    del Calculator.display_items[len(Calculator.display_items)-1-Calculator.display_items[::-1].index('RREF')]
                elif Calculator.internal_items[-1] == '.determinant()':
                    del Calculator.display_items[len(Calculator.display_items)-1-Calculator.display_items[::-1].index('DET')]
            else:
                del Calculator.display_items[-1]
            Calculator.internal_line = Calculator.internal_line[:Calculator.internal_line.rfind(Calculator.internal_items[-1])]
            del Calculator.internal_items[-1]

        if len(Calculator.internal_items) ==0:
            Calculator.digit_ended =False
            Calculator.prev_digit_ended = False
        elif len(Calculator.internal_items) ==1:
            if Calculator.internal_items[-1] in digits:
                Calculator.digit_ended = False
                Calculator.prev_digit_ended=False
            else:
                Calculator.digit_ended = True
                Calculator.prev_digit_ended=False
        else:
            if Calculator.internal_items[-1] in digits and Calculator.internal_items[-2] in digits:
                Calculator.digit_ended = False
                Calculator.prev_digit_ended = False
            elif Calculator.internal_items[-1] in digits and not Calculator.internal_items[-2] in digits:
                Calculator.digit_ended = False
                Calculator.prev_digit_ended = True
            elif not Calculator.internal_items[-1] in digits and Calculator.internal_items[-2] in digits:
                Calculator.digit_ended = True
                Calculator.prev_digit_ended = False
            else:
                Calculator.digit_ended = True
                Calculator.prev_digit_ended = True
        self.display_text()

    def close_window(self, window):
        window.destroy()
        


root = Tk()
root.geometry("800x600")
root.resizable(0, 0)
app = Window(root)
root.mainloop()

