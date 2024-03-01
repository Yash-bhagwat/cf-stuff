# Prints teamrating for a bunch of users
# Usage : python3 teamRateCalc.py {list of handle}
# for eg. : python3 teamRateCalc.py Blitztage Nisanth Teja-Smart

import math
import sys

import requests

n = len(sys.argv)
if n == 1:
    print("Invalid query")
    sys.exit()
team = [sys.argv[i] for i in range(1, n)]


def getwinprob(ra, rb):
    return 1 / (1 + math.pow(10, (rb - ra) / 400))


def teamrate(given_ratings):
    left, right = 1, 10000
    for _ in range(100):
        mid = (left + right) / 2
        winprob = 1.0
        for v in given_ratings:
            winprob *= getwinprob(mid, v)
        rating = math.log10(1 / winprob - 1) * 400 + mid
        if rating > mid:
            left = mid
        else:
            right = mid
    return round((left + right) / 2)


ratings = []
template = "https://codeforces.com/api/user.rating?handle="
for person in team:
    response = requests.get(template + person)
    response = response.json()
    if response["status"] == "FAILED":
        print(f"{person} is an invalid handle")
        sys.exit()
    response = response["result"]
    if len(response) == 0:
        ratings.append(0)
    else:
        ratings.append(response[-1]["newRating"])
print(teamrate(ratings))
