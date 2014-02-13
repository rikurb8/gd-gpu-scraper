#!/usr/bin/env python
#-*- coding:UTF-8 -*-

#ofcourse some models had boost clks also, so we need to add a column for them also and place the data correctly

if __name__ == "__main__":

    infile = open("gd-gpu-starting_from0.csv", 'r')
    outfile = open("game-debate-gpu-13-02-2014.csv", 'w')


    counter = 0
    for line in infile:

        specs = line.split(';')


        #if both specs[2] and [3] have a MHz reading in them, there was a boost clock also
        if "MHz" not in specs[3]:
            specs[2] += ";-"
            counter += 1


        info_string = ""
        for spec in specs:
            info_string += ';'
            try:
                info_string += spec.strip().encode('utf-8', 'ignore').replace("0xc3", "")
            except UnicodeDecodeError:
                print spec

        #get rid of the first ;
        info_string = info_string.replace(";", "", 1)

        outfile.write(info_string)
        outfile.write('\n')
    print counter