#!/usr/bin/env python3

import sys
import csv
import os
import operator

Dict = {}

def algoPath(start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in Dict:
        return []
    paths = []
    for node in Dict[start][2]:
        if node not in path:
            newpaths = algoPath(node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def newTask(task, tab):
    length = 0
    paths = []
    for key in tab:
        tmp = algoPath(task, key)
        if tmp: paths += tmp
    for path in paths:
        duration = 0
        for loc in path[1:]:
            duration+= Dict[loc][1]
        tmp = duration
        if tmp > length: length = tmp
    return length

### CONSTRUCTION LENGTH ###

def putFloat(duration):
    for task in Dict:
        next_time = duration
        for current in Dict:
            if task in Dict[current][2] and next_time > Dict[current][3]:
                next_time = Dict[current][3]
        Dict[task][5] = next_time - Dict[task][4]

def findDuration(tab):
    duration = 0
    for task in Dict:
        Dict[task][3] = newTask(task, tab)
        Dict[task][4] = Dict[task][3] + Dict[task][1]
        if (Dict[task][4] > duration):
            duration = Dict[task][4]
    putFloat(duration)
    if (duration > 1):
        print("total duration of construction:", duration,"weeks")
    else:
        print("total duration of construction:", duration,"week")
    print()

### GANT ALGO ###

def algoGantt(tab):
    findDuration(tab)
    tmp = []
    for current in Dict:
        tmp.append([current, Dict[current][3], Dict[current][1], Dict[current][5]])
    tmp = sorted(tmp, key=lambda elem: (elem[1], elem[2], elem[3]))
    for elem in tmp:
        current = elem[0]
        if Dict[current][5] > 0:
            print(current, "must begin between",
                  "t=" + str(Dict[current][3]), "and",
                  "t=" + str(Dict[current][3] + Dict[current][5]))
        else:
            print(current, "must begin at" , "t=" + str(Dict[current][3]))
    print()
    for elem in tmp:
        current = elem[0]
        print(current + "\t" + "(" + str(Dict[current][5])
              + ")" + "\t" + str(" "*Dict[current][3])
              + str("="*Dict[current][1]))

def printUsage():
    print("USAGE")
    print("\t./305construction file")
    print("DESCRIPTION")
    print("\tfile\tfile describing the tasks\n\n")
    exit(0)

def main():
    if sys.argv[1] == "-h":
        printUsage()
    try:
        tab = []
        with open(sys.argv[1], newline='') as csvfile:
            roadmap = csv.reader(csvfile, delimiter=';')
            for line in roadmap:
                if len(line) != 0:
                    tmp = []
                    if len(line) < 4:
                        tab.append(line[0])
                    tmp.append(line[1])
                    tmp.append(int(line[2]))
                    tmp.append(line[3:])
                    tmp.extend((0,0,0))
                    Dict[line[0]] = tmp
                    print(Dict[line[0]])
    except Exception as error:
        sys.stdout.write(str(error))
    algoGantt(tab)
    exit(0)

if __name__ == "__main__":
    exit(main())