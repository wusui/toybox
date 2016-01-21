#!/usr/bin/env python
import copy, itertools
def a084(a098, a099):
    print a098
    with open(''.join(['output.',str(a099),'.txt']), 'a') as f:
        f.write(a098+'\n')
    return False
a017 = lambda a018, a019, a020 : [i for i in a018 if i in a020] == a018 and a019['a000']['a001'].append(-100)
a070 = lambda a018, a019 : ([a017(a018, a019, a020) for a020 in a019['a004'][:-1]] or True) and a071(a018, a019)
a037 = lambda a091, a010, a023, a025, a026, a027, a029 : a091 == [] and a083(a010,a027) or a022(a010, a023, a091, a025 + [a029[1]], a026, a027)     
a016 = lambda : [a009(x) for x in a049()]
a075 = lambda a076, a077 : a045([[x,y] for y in range(1,(a076+1)/2) for x in range(1,(a077+1)/2)][1:], [a077, a076])
a031 = lambda x : min([a[1] for a in x if a[0] == 0])
a069 = lambda x : max([a[1] for a in x])
a082 = lambda a019 : a019['a004'].append(a044(a019))
a065 = lambda a043, a066, a019 : a067([sum(x) for x in zip(a043, a066)], a019)
a045 = lambda a046, a047: sum([a048(x, a047) for x in a046])
a067 = lambda a087, a019 : a087 in a044(a019) or a087[0] < 0 or (a087[0] == 0 and a087[1] < 0) or a088(a019['a000'], a087)
a081 = lambda a089, a090 : a086({'a000': a089, 'a005': [], 'a007': [], 'a004': [], 'a006': a090})
a011 = lambda a012 : [[a013, a014] for a013 in range(0, len(a012[0])) for a014 in range(0, len(a012)) if a012[a014][a013] == 0] or [[]]
a059 = lambda a060, a027, a061, a021 : not a027 == a061[1] and a060 or a060[0:a061[0]] + [a021] + a060[a061[0]+1:]                     
a058 = lambda x : min([a[1] for a in x])
a088 = lambda a096, a097 : a096['a003'].append( a051(a097))
a033 = lambda a073 : sum([x[0] == 0 and 1 or 0 for x in a073]) % 2 == 1
a049 = lambda : a050(a051([0,0]))
a056 = lambda a057 : sum([(2**x[0]) * 10**x[1] for x in a057])
a036 = lambda a012, a061, a021 : [a059(a060,a027,a061,a021) for a027,a060 in enumerate(a012)]
a007 = lambda a006 : [[a078(x,y) for x in a006] for y in [[1,1],[-1,1],[1,-1],[-1,-1]]]
a071 = lambda a018, a019 : len(a018) == 5 and -100 not in list(itertools.chain.from_iterable(a018)) and a019['a000']['a002'].append(a018)
a038 = lambda a010, a023, a025, a026, a027, a029 : a037(a011(a010)[0], a010, a023, a025, a026, a027, a029)
a048 = lambda a043, a047: a022(a092(a043[0], a043[1], a047), a015(), [0,0], [], [a043[1], a043[0]], 0)
a035 = lambda a012, a024, a021 : not a024 and a012 or a036(a035(a012,a024[1:],a021),a024[0],a021)
a072 = lambda a019 : a070(a044(a019), a019)
a083 = lambda a012, a027 : a084(''.join([''.join([{331: 'p', 2311: 'n', 323: 'u', 1311: 'y', 3111: 'l', 711: 'v', 11111: 'i', 227: 't', 623: 'z', 271: 'f', 631: 'w', 1: 'x'}[a085] for a085 in a060] + ['\n']) for a060 in a012]), len(a012)) or a027 + 1
a002 = lambda x : ((a058(x) < 0) and 1) or ((a068(x) > a069(x)) and 1) or a056(x)
a034 = lambda a012, a023, a024, a025, a026, a027, a029 : a052([a053([sum(x) for x in zip(a054,a024)], a012, a023, a025, a026, a027) for a054 in a029[0]], a012, a023, a025, a026, a027, a029)
a028 = lambda a012, a023, a024, a025, a026, a027, a029 : a029[1] in a025 and -1 or (a026[0]*2 + 1) == len(a012) and a029[1] == 2311 and a032(a029[0]) and -1 or (a026[1]*2 + 1) == len(a012[0]) and a029[1] == 331 and a033(a029[0])  and -1 or a034(a012, a023, a024, a025, a026, a027, a029)
a009 = lambda a001 : (a001, max([a002(a003(a004(a005))) for a005 in a000(a001)]))
a068 = lambda x : max([a[0] for a in x])
a032 = lambda a073 : any(y < 0 for _,y in a073)
a050 = lambda a080 : [a081(a080, [a041]) and a081(a080, [a082, a072]) for _ in range(0,4)] and a062(a080, [])
a044 = lambda a019 : map(lambda x : x['a001'], a019['a005'])
a015 = lambda : [(x,y) for x,y in a016() if y > 1]
a051 = lambda a095 : {'a001': a095, 'a003': [], 'a002': []}
a042 = lambda a043, a019 : [a065(a043, a066,a019) for a066 in [[0,1],[1,0],[0,-1],[-1,0]]]
a008 = lambda a006 : [x[::-1] for x in a006]
a000 = lambda a006 : a007(a006) + a007(a008(a006))
a022 = lambda a012, a023, a024, a025, a026, a027 : sum(filter(lambda x : x > 0, [a028(a012, a023, a024, a025, a026, a027, a029) for a029 in a023]))
a053 = lambda a055, a012, a023, a025, a026, a027 : a055[0] >= 0 and a055[1] >= 0 and a055[0] < len(a012[0]) and a055[1] < len(a012) and a012[a055[1]][a055[0]] == 0 and a055
a079 = lambda : [a075(i, 60//i) for i in range(3,7)]
a086 = lambda a019: a019['a005'].append(a019['a000']) or (not a019['a000']['a003'] and [a099(a019) for a099 in a019['a006']]) or ([a086({'a000': a064, 'a005': a019['a005'], 'a004': a019['a004'], 'a007': a019['a007'], 'a006': a019['a006']}) and a019['a005'].pop() for a064 in a019['a000']['a003']]) or a019['a007']
a003 = lambda a030 : [[x[0], x[1]-a031(a030)] for x in a030]
a004 = lambda a005 : [[x[0]-a091(a005), x[1]] for x in a005]
a062 = lambda a019, a063 : (a019['a002'] and a063.append(a019['a002'][0])) or [a062(a064, a063) for a064 in a019['a003']] and a063
a052 = lambda a040, a012, a023, a025, a026, a027, a029: all(a040) and a039(a040, a012, a023, a025, a026, a027, a029)
a041 = lambda a019 : [a042(a043, a019) for a043 in a044(a019)]
a091 = lambda x : min([a[0] for a in x])
a039 = lambda a040, a012, a023, a025, a026, a027, a029 : a038(a035(copy.deepcopy(a012), a040, a029[1]), a023, a025, a026, a027, a029)
a078 = lambda x, y : [a*b for a,b in zip(x,y)]
a092 = lambda a093, a094, a047 : a074([[sum(x) for x in zip([a093,a094],z)] for z in [[0,0],[1,0],[-1,0],[0,1],[0,-1]]], a047, 1)
a074 = lambda a024, a047, a021 : a035([[0]*a047[0] for _ in range(0, a047[1])], a024, a021)
if __name__ == '__main__': print a079()
