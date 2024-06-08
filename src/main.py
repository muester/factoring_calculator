import sys
import graphical

def main():
    args = sys.argv[1:]
    if not args:
        g = graphical.Window()
        g.run()
    else:
        if not args[0].isdigit():
            print("Error: incorrect input format!")
        elif len(args) > 1:
            print(graphical.best(int(args[0]),args[1]))
        else:
            print(graphical.best(int(args[0]),'b'))

if __name__ == "__main__": 
    main() 