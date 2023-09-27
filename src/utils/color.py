import random


def randomcolor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    colorr = ""
    colorg =""
    colorb = ""
    for i in range(2):
        colorr += colorArr[random.randint(0, 14)]
    for i in range(1):
        colorg += colorArr[random.randint(0, 14)]
    for i in range(2):
        colorb += colorArr[random.randint(0, 14)]
    return "#" + colorr +   colorg+ "0" + colorb


color_box = [randomcolor() for c in range(10000)]


def random_color(index):
    return color_box[index]
