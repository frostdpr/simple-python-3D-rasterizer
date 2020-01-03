NUMBER_OF_TRIANGLES = 30
RANDOM_W_VALUES = False # Much slower if True
###############################################
import random
y = open("input.txt","w")
y.write("png 1366 768 hw2loadmv.png\n")

def get3points():
    out = []
    for i in range(3):
        r = lambda: str(random.uniform(-1,1))
        a,b,c = r(),r(),r()
        out.append("xyz " + " ".join([a,b,c]))
    return "\n".join(out)

def getRandMatrix():
    global RANDOM_W_VALUES
    out = ["loadmv"]
    for i in range(3 + int(RANDOM_W_VALUES)):
        r = lambda: str(random.uniform(-1,1))
        a,b,c,d = r(),r(),r(),r()
        out.append(" ".join([a,b,c,d]))
    if(not RANDOM_W_VALUES):
        out.append("0 0 0 1")
    return "  ".join(out)

def test(n):
    calls = []
    for i in range(1,n):
        points = get3points()
        print(points,file=y)

        print(getRandMatrix(),file=y)

        x = 3*(i-1)+1
        calls.append("trif " + " ".join(map(str,(x,x+1,x+2))))
        for line in calls:
            print(line,file=y)

        r = random.random
        print("color",r(),r(),r(),file=y)

test(NUMBER_OF_TRIANGLES)
