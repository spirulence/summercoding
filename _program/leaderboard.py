#!/usr/bin/env python

import json
import argparse
from collections import defaultdict
import os.path

import yaml

points_string = """
anagramcounting	3.2
bachetsgame	1.9
bing	3.3
burrowswheeler	4.2
checkingforcorrectness	3.8
collatz	4.6
cross	6.2
dartscoring	4.5
divisible	4.2
flexible	1.6
functionalfun	2.6
fundamentalneighbors	4.3
howmanydigits	3.3
itsasecret	3.9
kastenlauf	3.4
kitchencombinatorics	5.1
mixedbasearithmetic	5.4
moviecollection	8.1
perfectpowers	5.2
permutationencryption	2.6
powerstrings	8.5
prettygoodcuberoot	4.3
primereduction	4.6
raceday	4.0
substrings	5.8
sidewayssorting	2.2
lottery	6.2
trainsorting	4.5
"""

points = {}
for line in points_string.splitlines():
	if line:
		name, point = line.split()
		point = float(point)
		points[name] = point

def compute_problems_solved(student):
	#for each student, compute the tries and status for each attempted problem
	submissions = student["submissions"]
	problems = defaultdict(lambda : {"status":"unsolved"})
	
	for submission in submissions:
		problem = submission["problem"]
		judgement = submission["judgement"]
		
		if judgement == "Accepted":
			problems[problem]["status"] = "solved"
		
	for name, problem in problems.items():
		score = points[name]
		if score:
			yield {"name":name, "score":score}

def compute_scores(students):
	
	scores = defaultdict(list)
	for student in students:
		name = student["name"]
		solved = list(compute_problems_solved(student))
		solved.sort(reverse=True, key = lambda p : (p["score"],p["name"]) )
	
		score = sum(p["score"] for p in solved)
		score = round(score, 2)
					
		scores[score].append({"student":name, "solved":solved})
		
	for score in sorted(scores, reverse=True):
		yield {"score":score, "students":scores[score]}
	

parser = argparse.ArgumentParser()

parser.add_argument("input_json")

args = parser.parse_args()

with open(args.input_json) as input_json_file:
	input_json = json.load(input_json_file)
	
scores = list(compute_scores(input_json["students"]))

output_path = os.path.splitext(args.input_json)[0]+".yml"

with open(output_path, "w") as output_yaml_file:
	yaml.dump(scores, output_yaml_file)

