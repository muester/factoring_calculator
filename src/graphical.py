import tkinter as tk

from primality import bailie_psw as bp

from factorization import trial_division_factors as td
from factorization import pollard_rho as pr
from factorization import factor_integer as fi
from factorization import lecm as er

class Window:
    
    def run(self):
        
        self.window = tk.Tk()
        self.window.title("Factoring calculator")
        self.window.geometry('300x300')

        self.inputtxt = tk.Text(self.window, height = 5, width = 20) 
        self.inputtxt.pack()
        
        self.options = ['Trial Division', 'Pollard Rho', 'Lenstra ECM', 'Best']
        self.choice = tk.StringVar(value='Best')

        self.choicemenu = tk.OptionMenu(self.window, self.choice, *self.options)
        self.choicemenu.pack()
        

        self.confirmbutton = tk.Button(self.window, text = 'Factor!', command = self.run_factor)
        self.confirmbutton.pack()

        self.label = tk.Label(self.window, text = "",wraplength=250)
        self.label.pack()

        self.window.mainloop()

    def run_factor(self):
        num = self.inputtxt.get(1.0, "end-1c")
        choice = self.choice.get()
        self.label.config(text = 'Calculating!')
        self.window.update()
        try:
            num = int(num) 
            num = best(num,choice)
        except ValueError:
            num = "Error: wrong input format!"
        self.label.config(text = num)

def best(num, choice):
        prefix = f'Factorization of {num}: \n'
        if num <= 0:
            num = "Error: factored number must be positive!"
        elif num == 1:
            num = '[1]'
        elif bp(num):
            num = str(num) + ' is a prime number!' 
        elif choice in ['t','Trial Division']:
            num = prefix + str(td(num))
        elif choice in ['p','Pollard Rho']:
            num = prefix + str(pr(num))
        elif choice in ['e','Lenstra ECM']:
            num = prefix + str(er(num))
        elif choice in ['b','Best']:
            num = prefix + str(fi(num))
        else:
            num = "Error: unrecognized argument!"
        return num