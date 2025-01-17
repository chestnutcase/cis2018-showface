from itertools import chain, combinations

def powerset(iterable):
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))

def sum(iterable):
    ans = 0
    for x in iterable:
        ans = ans + x;
    return ans

nFoods = 20;
#rFoods = [2,62,86,85,8,86,25,85,88,20,38,93,55,19,43,83,58,90,90,27,53,46,11,100,38,47,13,60,87,96,99,71,19,29,93,91,61,25,28,28,61,54,13,15,64,89,99,61,52,26,46,24,34,16,28,53,9,48,60,7,78,39,67,85,38,62,79,38,45,82,76,18,70,32,29,24,51,93,55,77,43,14,76,33,2,78,66,29,61,36,68,48,15,74,36,25,16,77,47,65,78,100,81,73,15,4,90,8,100,37,80,12,99,75,1,63,3,29,40,24,67,41,50,74,54,62,73,72,85,61,48,70,98,24,2,7,21,34,81,77,71,6,42,30,70,94,83,55,55,92,78,17,99,40,27,48,43,45,85,30,58,87,9,64,63,12,97,49,52,84,22,98,44,94,58,25,67,7,13,26,87,75,28,70,16,20,78,23,77,9,14,59,18,36,58,85,81,16,95,95];
#lFoods = [82,60,86,95,42,23,50,72,52,25,79,50,68,29,27,71,60,41,66,18,24,74,3,16,12,25,93,39,81,22,96,69,90,42,87,87,59,41,83,62,38,9,43,81,50,68,99,76,73,45,46,89,69,35,45,90,86,14,37,78,40,87,28,64,57,16,4,81,40,81,27,18,98,17,23,80,53,35,64,13,82,43,1,1,8,63,1,65,50,65,34,22,84,10,6,7,64,37,91,37,22,86,100,60,95,7,44,35,47,15,90,92,43,93,84,25,29,80,5,38,10,57,10,43,30,73,15,14,71,76,98,14,91,80,14,44,32,96,54,24,16,17,82,34,71,48,23,92,82,38,62,84,78,42,70,84,64,5,52,90,67,83,35,76,91,7,49,59,65,54,22,52,74,90,95,43,28,60,22,62,21,76,75,58,51,54,89,56,17,27,33,98,62,48,16,78,65,75,38,28];
rFoods = [95,61,24,67,27,39,66,78,27,12,37,82,84,33,92,68,24,53,48,44];
lFoods = [95,61,24,67,27,39,66,78,27,12,37,82,84,33,92,68,24,53,48,44];
#rFoods = [4,5];
#lFoods = [3,6];
maxDiff = 20;
rFoods = sorted(rFoods);
lFoods = sorted(lFoods);

rFoodsS = powerset(rFoods);
lFoodsS = powerset(lFoods);

#print(lFoodsS);
#print(rFoodsS);
result = 0;

for rFood in rFoodsS:
    skipTheRest = False;
    for lFood in lFoodsS:
        if(abs(sum(rFood)-sum(lFood))<=maxDiff):
            result = result + 1;
        else:
            skipTheRest = True;
print(result);
