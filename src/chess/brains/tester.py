from wrapper import solver_filter

def lprint(instr):
    print instr

if __name__ == "__main__":
    print solver_filter("2/W:Ka1,Rh1/B:Kh8", lprint)
