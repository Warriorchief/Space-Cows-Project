"""        
************Chris Green SpaceCows Project November,2016************** 
 
[This program is based on an assignment from the MIT edX MOOC 6.00.2x. At the
time I wrote it, it was the most advanced programming project I'd undertaken.
Its purpose was to examine and compare methods of searching and sorting data.
I learned a lot about Python -- especially concerning modularity and scope-- 
in its architecting, editing, extending, and commenting.]


                    TRANSPORTING SPACE COWS!
The farcical proposition was to select the cows, given a dictionary of their
names and weights, that would be put onto each transport ship, in order to
bring them across the galaxy to an alien world. The sorting and filling of the
spaceships is done by either a "Greedy" (packing each ship with the heaviest
remaining cows that will fit) or a "Brute Force" (trying every possible
arrangement of cows) algorithm. 

The main function runs the two methodologies on the same input dictionary and
parameter "limit", which is the maximum total weight that can be loaded onto 
each ship. I went beyond the scope of the original problem by coding a set of 
user inputs that allows for testing and comparison of the two search methods
based on user-input # of cows and maximum weight on each ship. 

In general, the Greedy algorithm will come very CLOSE to a perfect solution 
and, crucially, will do so far, far faster than the BRUTE. This time disparity
grows more pronounced as the initial cow dictionary grows in size. The 
implication is that for large sets of data -- ones that would be constrained
by processing power and time -- a logical search algorithm becomes more
practical (even if not technical preferable) to a unstructured one. How close 
does Greedy come to "perfect"? Well, for the pursposes of this problem, what
matters is the number of ships used. This almost always comes out to be the
same for both algorithms, as is indicated by the final output on the screen. I
have run many, many iterations and the only settings EVER produced a different
number of ships (that is, a non-perfect output for Greedy) was Cows=11 and 
Weight=14. However, even this will usually not happen, and you might have to 
run the program several times using those settings in order for the non-perfect
to occur again. 

""" 

from ps1_partition import get_partitions
import time
import random

def load_cows(filename, numCows):
    """
    load_cows loads the 25 cows -- from another file -- and then randomly
    selects numCows of them to constite the "choice" sub-dictionary based
    on the user unput in MAIN. 
    """
    cow_dict = dict()
    choice_dict=dict()
    f = open(filename, 'r')    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])   
    while numCows>0:
        choiceCow=random.choice(list(cow_dict.keys()))
        #print("have chosen choice cow "+choiceCow)
        choice_dict[choiceCow]=(cow_dict[choiceCow])       
        del cow_dict[choiceCow]
        numCows-=1
    #print(str(choice_dict))
    return choice_dict

   
    
    
"""
_______________________________________
PART A: Constructing the Greeedy Search
_______________________________________
"""    
def fill_one_ship(cows,limit):
    """
    fill_one_ship acts as a subroutine of greedy_cow_transport. It picks the
    heavist available cow, sees whether it will fit, and if so loads it. If it
    doesn't fit, it picks the next heaviest cow. It repeats this process until 
    the ship if full becasue it's either reached its maximum capacity of none
    of remaining cows will fit onto it. 
    """
    loaded = []
    weight=0
    holder=cows.copy()
    while weight<limit and len(holder)>0:
        fat = max(list(holder.values()))
        fatIndex = list(holder.values()).index(fat)
        fatName = list(holder.keys())[fatIndex]
        if fat+weight<=limit:
            loaded.append(fatName)
            weight+=fat
            del holder[fatName]
        else:
            del holder[fatName]
    return loaded

def greedy_cow_transport(cows,limit):
    """
    greedy_cow_transport minimizes the number of spaceship trips via Greedy 
    selection. It does so by repeatedly calling the submodule fill_one_ship. It
    returns a list of lists called 'transits', which enumerates the freight of
    each and all spaceships to be filled. 
    """
    c = cows.copy()
    transits = []
    while len(c)>0:
        thisTrip = fill_one_ship(c,limit)
        transits.append(thisTrip)
        for item in thisTrip:
            del c[item]
    return transits

    
    
    
"""
___________________________________________
PART B: Constructing the Brute Force Search
___________________________________________
"""    

def get_Parts_List(aDict):
    """get_Parts_List builds a list whose elements constitute ALL possible
    subgroupings of the set of cows in the starting dictionary. This will be
    a large number. For example, a dictionary of 10 cows will have 115,975
    such subgroupings. (Here, and elsewhere, I have left some #'d out code in
    order to remind myself of testing and debugging steps.)
    """
    #i=0
    parts=[]
    for item in get_partitions(aDict):
        parts.append(item)
        #i+=1
    #print(str(i))
    return parts

def check_Sub(sub,limit,dick): #avoid using the special word 'dict'
    """
    check_Sub analyzes the innermost element of part (the list of possible
    partitionings of the cows). For example, it checks whether the sublist
    of three cows ['Florence', 'Betsy', 'Henrietta'] goes over the limit and
    returns the appropriate Boolean.
    """
    c=sub.copy()
    d=list(c)
    e=dick.copy()
    #print("going to check whether the sub "+str(d)+" goes over "+str(limit))
    sum = 0
    k=0
    while k<len(d):
        name=d[k]
        #print("dealing with the name "+name)
        sum+=e[name]
        k+=1
    #print("sum of the items in this sub is "+str(sum))
    if sum > limit:
        #print("so this string failed")
        return False
    else: 
        #print("this sub passed")
        #print(" ")
        return True
        
def check_Chunk(chunk,limit,dick):
    """
    check_Chunk analyzes whether a list of "Subs" -- a "Chunk" -- of the 
    partitions list, abides the weight limit constraint. For example, the 
    Chunk given by parts[60000] is:
        [['Florence', 'Betsy'],
         ['Herman', 'Millie', 'Moo Moo', 'Maggie'],
         ['Henrietta'],
         ['Lola', 'Milkshake'],
         ['Oreo']]
    For ths Chunk to pass, each of its five Subs will have to pass. This is 
    evaluated by repeated calls to check_Sub, and again a Boolean is returned.
    """
    #print("will now analyze the chunk "+str(chunk)+" to see if any sub > "+str(limit))
    #print(" ")
    for sub in chunk:
        if check_Sub(sub,limit,dick) != True:
            return False
    #print(" ")
    #print("this chunk passed")
    return True

def get_shortest(aList):
    """
    get_shortest chooses the sublist of least length from a list of lists. 
    This is used in Brute Force to choose an acceptable Chunk from among all
    the Chunks that pass -- which get put into the list "trues".
    """
    shortest = min(len(l) for l in aList)
    #print("the shortest sublist has length "+str(shortest))
    return shortest    
    
def brute_force_cow_transport(cows,limit):
    """
    brute_force_cow_transport uses two layers of modularity -- check_Chunk
    and check_Sub -- to construct of list of acceptable Chunks from among
    the partitions list. The chunks that pass are put "trues". Then the 
    shortest item in this list is selected and returned. (There might be a tie for shortest,
    and that's fine, which is why the #'d comment says 'one such way' rather
    than 'the way'.)
    """
    trues = []
    c=cows.copy()
    parts=get_Parts_List(c)
    #print("will analyze the "+str(len(parts))+" chunks here...")
    numChunks=len(parts)    
    for chunk in parts:
        #print("now checking the chunk "+str(chunk))
        if check_Chunk(chunk,limit,c) == True:
            trues.append(chunk)
            #print("this chunk passed")
    #print("there were "+str(len(trues))+" chunks that work: ")
    #print("  ")
    #print(str(trues))
    shortest = get_shortest(trues)
    #print("shortest that works is "+str(shortest)+" so let's look for one with that length")
    for k in trues:
        if len(k)==shortest:
            #print("one such way that works is to do "+str(k))
            #print(str(k))
            return (k,numChunks)
  
            
            
            
"""
_______________________________________________
PART C: Applying and Comparing Brute and Greedy
based on input from the user. 
_______________________________________________
"""    
def compare_cow_transport_algorithms(cows,limit):
    """
    compare_cow_transport_algorithms calls each of the two algorithms for the same
    input of cows. It gets the results, including the ideal ship listing
    given for each, as well as the time each took, and return this information
    as a tuple containing a subtuple.
    """
    #print("Will now analyze the Greedy and Brute algorithms using )
    gstart=time.time()
    bestGreedy=greedy_cow_transport(cows,limit)
    gend=time.time()
    gElapse=gend-gstart
    gElapseRnd=round(gElapse,3)
    #print(" ")
    #print("Loading via the Greedy algorithm took "+str(gElapseRnd)+" seconds.")
    #print("                AND      ")
    bstart=time.time()
    bB=brute_force_cow_transport(cows,limit)
    bestBrute=bB[0]
    numChunks=bB[1]
    bend=time.time()
    bElapse=bend-bstart
    bElapseRnd=round(bElapse,3)
    #print("Loading via the Brute algorithm took "+str(bElapseRnd)+" seconds.")
    #print("               THEREFORE       ")
    gap=round(abs(gElapseRnd-bElapseRnd),3)
    #print("In this instance the faster algorithm saved "+str(gap)+" seconds.")
    algoTriple = (gElapseRnd,bElapseRnd,gap)
    return (algoTriple,bestGreedy,bestBrute,numChunks)

def __main__():    
    ready = ""
    decision=""
    decision2=""
    numCows=0
    limit=0
    print(" ")
    print("Welcome to SpaceCows! This program compares the efficiencies of a ")
    print("Greedy and Brute sorting algorithm.")
    while not ((4<numCows<12) and type(numCows)==int):
        print(" ")
        print("How many cows should the dictionary consist of?")
        numInput=input("Enter an integer from 5 through 11, inclusive.  ")
        numCows=int(numInput)
        cows = load_cows("cowslist.txt",numCows)
    while not(limit in range(10,21) and type(limit)==int):
        print(" ")    
        print("What should the weight limit for each ship be?")
        limInput=input("Please enter an integer from 10 through 20, inclusive.  ")
        limit=int(limInput)
    print(" ")
    print("Have selected the following cows: ")
    print(cows)
    print("And we will use a weight limit of "+str(limit)+" per ship.")
    ready=input("NOTE: this may take up to 30 seconds. Ready to launch? Enter Y/N  ")
    if ready.upper()!="Y":
        print(" ")
        print ("Okay, see you on the next launch instead!")
    else:
        tests = (compare_cow_transport_algorithms(cows,limit))
        gships=len(tests[1])
        bships=len(tests[2])
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print("********************************************************")
        print("********************************************************")        
        print("The Greedy algorithm took "+str(tests[0][0])+" seconds.")
        print("It returned the following APPROXIMATE ideal loading of ships: "+str(tests[1]))
        print(" ")
        print("The Brute algorithm took "+str(tests[0][1])+" seconds.")
        print("It had to analyze "+str(tests[3])+" chunks.")
        print("It returned the following ABSOLUTE ideal loading of ships: "+str(tests[2]))
        print(" ")
        if gships==bships:
            print("The Greedy and Brute used the same number of ships.")
            print("However, the Greedy took "+str(tests[0][2])+" seconds less.")
        else:
            print("The Brute ended up using "+str(gships-bships)+" fewer ships.")
            print("However, the Greedy took "+str(tests[0][2])+" seconds less.")
        print("********************************************************")
        print("********************************************************") 
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print("Play a few times to guage the effect of adjusting the input paramaters.")
        print("When satisfied, hit 'S' after a trial to see the explanation and a table of outcomes.")
        decision=input("Press P to play again. Press S to see explanation. Press any other key to quit.  ")
        if decision.upper()=="P":
            return __main__()
        elif decision.upper()=="S":
            see_explanation()
            decision2=input("Press P to play again. Press any other key to quit.  ")
            if decision2.upper()=="P":
                return __main__()
            else:
                print(" ")
                print("Okay, see you again some day!")
                return
        else:
            print(" ")
            print("Okay, see you again some day!")
            return

def see_explanation():
    """
    see_explanation allows the user to more formally understand the mechanisms
    at work in comparing the two Algorithms.
    """
    t=[["             ","Weight=10","Weight=15","Weight=20"],["(#Cows)                "],       [5,0.00,0.00,0.00],
      [6,0.00,0.00,0.00],[7,0.01,0.02,0.02],
      [8,0.07,0.12,0.09],[9,0.47,0.45,0.54],[10,2.35,2.53,2.97],
      [11,13.74,15.43,18.54]]

    print(" ")
    print(" ")
    print(" ")
    print("  **************************************************************")
    print("  **************************************************************")
    print("         (OBSERVED PROCESSING TIME OF BRUTE IN SECONDS)")
    
    print(str(t[0][0])+"     "+str(t[0][1])+"      "+str(t[0][2])+"      "+str(t[0][3]))
    print("       "+str(t[1][0]))
    i=2
    while i<4:
        print("          "+str(t[i][0])+"          "+str(t[i][1])+"            "+str(t[i][2])+"            "+str(t[i][3]))
        i+=1
    while i<7:
        print("          "+str(t[i][0])+"          "+str(t[i][1])+"           "+str(t[i][2])+"           "+str(t[i][3]))
        i+=1
    print("         "+str(t[7][0])+"          "+str(t[7][1])+"           "+str(t[7][2])+"           "+str(t[7][3]))
    print("         "+str(t[8][0])+"         "+str(t[8][1])+"          "+str(t[8][2])+"          "+str(t[8][3]))
    print("  **************************************************************")
    print("  **************************************************************")
    print(" ")
    print("In general, increasing the number of cows causes a dramatic increase",
          "in the number of computations for the Brute Algorithm. This is because",
          "the number of possible arrangements of cows -- 'chunks' according",
          "to our labeling -- roughly quadruples or quintuples with the addition",
          "of each additional cows. Loading 5 cows creates 52 chunks, 6 creates",
          "203, 7 creates 877, 8 creates 4,140, 9 creates 21,147, 10 creates 115,975",
          "and 11 creates 678,570. Note that while you could theoretically",
          "extend the parameters much higher, it becomes unrealistic to process",
          "on a normal computer. This of course proves the necessity of sorting",
          "algorithms. As you probably saw, the Greedy algorithm almost always",
          "arrives at the correct answer -- requiring the same number of ships",
          "-- and never takes more than .02 seconds.")
    return
    
if __name__=="__main__": __main__()  
    
    
    
    
    
    
    