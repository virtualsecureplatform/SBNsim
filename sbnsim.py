#!/bin/python3

import numpy as np
from random import randint

# MAX = 4
# data = [randint(0,MAX-1) for i in range(MAX)]
# print(data)

data = [1, 0, 2, 1]
# data = np.array([3,5,8,7,2,4,9,0,1,6])
# data = np.array([9,1,6,0])
RAM = np.zeros(512,dtype=np.int32)
null = -1

# Registers Address
PC = 0
Reg0 = 1
Reg1 = 2
temp = 3
pivot = 4
first = 5
last = 6
i = 7
j = 8
jtemp = 9
temp1 = 10
itemp = 11
accumlator = 12
mem_tempi = 13
mem_tempj =14
product = 15
Reginv1 = 16
Reginv2 = 17
Reginv4  = 18
Reg2 = 19
Regbase = 20
stack = 21
Regstart = 22

#$2000, start point of data
start = 23
for index in range(len(data)): RAM[index+start] = data[index]
base = start+len(data)

# initialize valiables
RAM[stack] = 2
RAM[base] = 0
RAM[base+1] = len(data)-1

# constant
RAM[Reg0] = 0
RAM[Reg1] = 1
RAM[Reg2] = 2
RAM[Reginv1] = -1
RAM[Reginv2] = -2
RAM[Reginv4] = -4
RAM[Regbase] = base
RAM[Regstart] = start

# Labels
SOP = 0
QS = 9
while1 = 14
while2 = 19
wend2 = 26
while3 = 29
wend3 = 34
endif = 44
wend1 = 45
EOP = 512



ROM = [
[stack,Reg2,stack,EOP,False,False,False],#SOP
[Reg0,stack,itemp,null,False,False,False],
[Regbase,itemp,itemp,null,False,False,False],
[itemp,Reg0,temp,null,False,False,False],
[itemp,Reginv1,temp1,null,False,False,False],
[temp,Reg0,first,null,True,False,False],
[temp,Reg0,pivot,null,True,False,False],
[temp1,Reg0,last,null,True,False,False],
[last,Reg1,itemp,null,False,False,False],
[itemp,first,temp,SOP,False,False,False],#QS
[first,Reg0,pivot,null,False,False,False],
[first,Reg0,pivot,null,False,False,False],
[first,Reg0,i,null,False,False,False],
[last,Reg0,j,null,False,False,False],
[i,Reginv1,itemp,null,False,False,False],#while1
[j,itemp,temp,wend1,False,False,False],
[Reg0,pivot,jtemp,null,False,False,False],
[Regstart,jtemp,temp1,null,False,False,False],
[temp1,Reginv1,jtemp,null,True,False,False],
[Reg0,i,itemp,null,False,False,False],#while2
[Regstart,itemp,temp,null,False,False,False],
[jtemp,temp,accumlator,wend2,False,True,False],
[i,Reginv1,itemp,null,False,False,False],
[last,itemp,product,wend2,False,False,False],
[i,Reginv1,i,null,False,False,False],#Deled Moded
[Reg0,Reg1,PC,while2,False,False,False],
[Reg0,pivot,jtemp,null,False,False,False],#Deled wend2
[Regstart,jtemp,temp1,null,False,False,False],
[temp1,Reginv1,itemp,null,True,False,False],
[Reg0,j,jtemp,null,False,False,False], #while3
[Regstart,jtemp,temp,null,False,False,False],
[temp,itemp,accumlator,wend3,True,False,False],#Moded
[j,Reg1,j,null,False,False,False],
[Reg0,Reg1,PC,while3,False,False,False],
[j,i,temp,endif,False,False,False],#wend3
[Reg0,i,itemp,null,False,False,False],
[Regstart,itemp,temp,null,False,False,False],
[Regstart,itemp,mem_tempi,null,False,False,False],
[Reg0,j,jtemp,null,False,False,False],
[Regstart,jtemp,temp1,null,False,False,False],
[Regstart,jtemp,mem_tempj,null,False,False,False],
[temp,Reg0,jtemp,null,True,False,False],
[temp1,Reg0,mem_tempi,null,True,False,True],
[jtemp,Reg0,mem_tempj,null,False,False,True],
[Reg0,Reg1,PC,while1,False,False,False],#Moded endif
[Reg0,pivot,itemp,null,False,False,False], #wend1
[Regstart,itemp,temp,null,False,False,False],
[Regstart,itemp,mem_tempi,null,False,False,False],
[Reg0,j,jtemp,null,False,False,False],
[Regstart,jtemp,temp1,null,False,False,False],
[Regstart,jtemp,mem_tempj,null,False,False,False],
[temp,Reg0,jtemp,null,True,False,False],
[temp1,Reg0,mem_tempi,null,True,False,True],
[jtemp,Reg0,mem_tempj,null,False,False,True],
[Reg0,stack,itemp,null,False,False,False], #push
[Regbase,itemp,itemp,null,False,False,False],
[itemp,Reg0,mem_tempi,null,False,False,False],
[itemp,Reginv1,mem_tempj,null,False,False,False],
[j,Reginv1,jtemp,null,False,False,False],
[jtemp,Reg0,mem_tempi,null,False,False,True],
[last,Reg0,mem_tempj,null,False,False,True],
[itemp,Reginv2,itemp,null,False,False,False],
[itemp,Reg0,mem_tempi,null,False,False,False],
[itemp,Reginv1,mem_tempj,null,False,False,False],
[j,Reg1,jtemp,null,False,False,False],
[first,Reg0,mem_tempi,null,False,False,True],
[jtemp,Reg0,mem_tempj,null,False,False,True],
[stack,Reginv4,stack,null,False,False,False],
[Reg0,Reg1,PC,SOP,False,False,False]
]

def sbn(A,B,resultant,C,flagA,flagB,flagresultant):
    global RAM
    global PC
    PCtemp = RAM[PC]
    addA = A
    addB = B
    addresultant = resultant
    if flagA: addA = RAM[A]
    if flagB: addB = RAM[B]
    if flagresultant: addresultant = RAM[resultant]
    RAM[addresultant] = RAM[addA] - RAM[addB]
    if (RAM[addresultant] < 0) and (C>=0):
        RAM[PC] = C
    else: RAM[PC]=PCtemp+1

cycle = 0
while RAM[PC]!=EOP:
    print([RAM[PC],RAM[first],RAM[last],RAM[temp],RAM[temp1]])
    inst = ROM[RAM[PC]]
    sbn(*inst)
    cycle+=1
    print(RAM[start:start+len(data)])

print(RAM[start:start+len(data)])
print(cycle)