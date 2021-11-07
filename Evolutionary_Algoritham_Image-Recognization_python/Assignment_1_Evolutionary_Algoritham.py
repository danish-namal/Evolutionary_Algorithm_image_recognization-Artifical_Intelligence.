import numpy as np
import matplotlib
from matplotlib.image import imread
import PIL
from PIL import Image
from numpy import random
import scipy.stats
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
Group_pic = imread('groupGray.jpg')
# print('Group pic dimension',Group_pic.shape)
row,column = Group_pic.shape
babaji_pic = imread('boothiGray.jpg')
# print('template dimension',babaji_pic.shape)


#It initialize 100 random points from big pic in given size
def initial_popul(row,column,size_of_initPopulation):
    list2 = [(np.random.randint(476),np.random.randint(994)) for i in range(size_of_initPopulation)]
    return list2

#Fitness function will cut random pic equal to babaji based on inital population and find corelation
def fitness_popul(group_pic,babaji_pic,initialpop):
    a, b = initialpop
    if a+35 < 512 and b+29 <1024:
        point = Group_pic[a: a+ 35,b: b+29]
        #for corelation or fitness value
        a = np.mean((point - point.mean()) * (babaji_pic - babaji_pic.mean())) / (point.std() * babaji_pic.std())
        return round(a,2)
    else:
        return -1

# The Selection function will genrate 100 random points with 100 co-relation values in sorted acc to higher co-relation value.
def selection(initial_popu,fitness_popul):
    temp =[]
    roundFit=[]
    for i in range(len(fitness_popul)):
        roundFit.append(round(fitness_popul[i],2))
    # print(roundFit)
    merge = sorted(zip(roundFit,initial_popu),reverse=True)
    for value in merge:
        temp.append(value)
    return temp

#After population crossover we evolve new generation
def cross_over(listt):
    List = []
    evolved = []
    for i in range(len(listt)):
        binary = np.binary_repr(listt[i][0], width=9) + np.binary_repr(listt[i][1], width=10)
        # # print(binary)
        # print("Before")
        List.append(binary)
    # print(List)
    evolved.append(listt[0])
    for value in range(1,len(List)-1,2):
        a = np.random.randint(0, 19)
        # print('Random num generated is;',a)
        num1 = List[value]
        num2 = List[value+1]
        num1x = num1[:a]
        num1y = num1[a:]
        num2x = num2[:a]
        num2y = num2[a:]
        num1 = num1x + num2y
        num2 = num2x + num1y
#For evolving x and y after swaping Num1x+Num2y and Num2x + Num1y.......a1=10, a2=9 and b1=10, b2=9
        a1 = num1[:9]
        a2 = num1[9:]
        b1 = num2[:9]
        b2 = num2[9:]
        evolved.append((int(a1, 2),int(a2,2)))
        evolved.append((int(b1,2),int(b2,2)))
    evolved.append(evolved[0])
    return evolved


def mutation(crosover):
    Mutate_List = crosover
    for i in range(4):
        x = random.randint(1,len(crosover)-1)
        binary = np.binary_repr(crosover[x][0], width=9)
        binary1 = np.binary_repr(crosover[x][1], width=10)

        a = np.random.randint(0, 8)
        if binary[a] == "0":
            temp = binary[:a] + "1" + binary[a+1:]
        else:
            temp = binary[:a] + '0' + binary[a+1:]

        b = np.random.randint(0, 9)
        if binary1[b] == "0":
            temp1 = binary1[:b] + "1" + binary1[b+1:]
        else:
            temp1 = binary1[:b] + '0' + binary1[b+1:]

        Mutate_List[x] = (int(temp,2), int(temp1,2))
    return Mutate_List


def geneticalgocallfun():
    #Call function for initilizaation.
    initialpop = initial_popul(row,column,100)

    #This will store 100 corelation values within fitness function.
    maxFitnessValues=[]
    averageFitValues=[]
    fitness = []
    for i in initialpop:
        temp = fitness_popul(Group_pic,babaji_pic,i)
        fitness.append(temp)

    No_of_generation = 0
    while True:
        if No_of_generation == 2500:
            break
        b = selection(initialpop, fitness)
        Ranked = []
        for i in range(len(b)):
            Ranked.append(b[i][1])
        cross_pop = cross_over(Ranked)

        #This function is for mutation
        initialpop = mutation(cross_pop)
        fitness = []
        for i in initialpop:
            temp = fitness_popul(Group_pic,babaji_pic,i)
            fitness.append(temp)
        # save max points of fitness and mean of fitness values for graph
        arrayfit=np.array(fitness)
        maxFitnessValues.append(max(arrayfit))
        averageFitValues.append(round(np.mean(arrayfit),2))

        msg = False
        for i in range(len(fitness)):
            if fitness[i] > 0.9:
                reserve = i
                msg = True
                print('After',No_of_generation,'Generation we found babaji')
                plt.figure(2)
                plt.plot(averageFitValues)
                plt.plot(maxFitnessValues)
                plt.title('Fitness')
                plt.xlabel('Generations')
                plt.ylabel('Values')
                plt.show()
                break
        if msg == True:
            point = initialpop[reserve]
            break
        No_of_generation = No_of_generation + 1


    img = mpimg.imread('groupGray.jpg')
    y,x = initialpop[reserve]
    fig, ax = plt.subplots()
    # Display the image
    ax.imshow(img,cmap = 'gray')
    rect = patches.Rectangle(((x, y)), 30, 30, linewidth=2, edgecolor='g', facecolor='none')
    ax.add_patch(rect)
    plt.show()
if __name__ == "__main__":
    geneticalgocallfun()
