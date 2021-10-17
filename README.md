# rectangles

## What can you find here
This repository contains my answers to an algorithmic assigment.
You can find here:
1. code that generates R which is a large rectangle, and smaller non-overlapping, aligned-to-axis rectangles inside it - `gen_valid_data.py`.
3. code that checks if an (R, rectangles) are valid - into `unit_test.py`.
4. Having a valid (R, rectangles), there is a script that fill in R with new rectangles such that all the rectangles - given and new ones - are axis aligned and non overlapping and they cover all R's area - `algo.py`.

## Algorithm - explained
General idea: There are many ways to describe a rectangle, but when it is axes aligned, I find it simplest to do so with its coordinates: x1, x2, y1, y2. Let's assume that {}2>{}1. Two rectangles are overlapped if they have a common range both in x and y axes. In other words, if [x1, x2]intersection[x'1, x'2] is not empty, **and** [y1, y2]intersection[y'1, y'2] is not empty, then rect and rect' are overlapped. I used this perspective coming to write this algorithm.
- To create valid data, I first generated R, then generated N couples of xs, inside R, and sorted them. By sorting and then taking pairs {x1_i,x2_i} for i=1:N I guaranteed non-overlapping.
- To fill the R\given_rectangles area I created a bank of all the given rectangles' coordinates: {x1_i,x2_i}, {y1_i,y2_i} for i=1:N. Those have become my grid and after sorting them, I could have created patches to cover all R. This way, a patch could either be disjoint to all pre-given rectangles, or overlapped with one/few of them - and then I needed to throw it. I detected which is the case by computing each "potential rectangle"'s center, and finding out if it is inside any of the given rectangles. I dealt separately with the rectangles near R's edges, since they are easy to find, and it saves time and complexity in the average case.
_I tried to reduce the number of rectangle by recursively merge rectangles with 2 common vertices, but this part is not yet finished._
- To check validity, I checked overlapping in each axis separately (each rectangle has its own list of 'suspects' - other rectangles that overlapped in each axis) and then looked for common 'suspects' for both x and y axes.


## Usage
Run `unit_test.py` file to see it in action - this unit_test plots visual results.
Attached a .docx file with few observations and thoughts about this task.


## Requierments
I used basic packages only, I guess everyone has them in his basic environment. There is a requierments.txt file that can help you creating the desired environment if you want.


