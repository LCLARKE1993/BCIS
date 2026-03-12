# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 08:21:40 2026

@author: lenno
"""
from Task_B import PART_1, PART_2
import time
def Option_Choice():

    print("Choice 1: EPC_Analysis")
    print("Choice 2: Median_Habitable_Room_Analysis")

    choice = input("Select option (1 or 2): ").strip()

    if choice == "1":
        print("Running EPC_Analysis...")
        time.sleep(3)
        return PART_1()

    elif choice == "2":
        print("Running Median_Habitable_Room_Analysis...")
        time.sleep(3)
        return PART_2()

    else:
        print("Not a valid option...")
        time.sleep(3)
        print("Default EPC_Analysis has been applied")
        
        return PART_1()
    
if __name__ == "__main__":
    Option_Choice()