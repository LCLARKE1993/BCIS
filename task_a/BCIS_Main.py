# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 18:00:03 2026

@author: lenno
"""

from collections import deque
from unittest import result
from UI_main import Read_me, default


def simulate_deque(input_line:str, days:int=None) -> int:
    counts = deque([0] * 10)
    days = default(days)
    
    for t in map(int, input_line.split(",")):
        counts[t] += 1

    for _ in range(days):
        # popleft() remove the first element from the queue 
        new_survey = counts.popleft() 
        # reset the pop element to position 8 in the queue
        counts[7] += new_survey  
        brief_description = '''
        Circular buffer, it will contine to remove out of the queue and insertion 
        back into the queue until the range of days has elapsed. Never storing more
        than what is in the queue - less Ram Usage. As a result, it is a robust solution
        handle very large numbers (tested out 1000+ days)
        '''
        counts.append(new_survey) 
    result = sum(counts)    
    print(f"Running for {days}-days Survey Activity")
    print(f"Active Surveys in the system: {result:,}")
    print(f"{brief_description}")
    return result

if __name__ == "__main__":

    simulate_deque(input_line=Read_me(), days = None)
    