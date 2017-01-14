from wrapper import solver_filter

def lprint(instr):
    print instr

if __name__ == "__main__":
    print solver_filter("2/W:Ka1,Nh5/B:Kg8", lprint)
