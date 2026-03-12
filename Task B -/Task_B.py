# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 07:24:52 2026

@author: lenno
"""
import duckdb 


def Database_connection():
    
    ''' Create a DuckDB Database Connection  '''
    
    con = duckdb.connect()
    if con:
        
        print ("Database Connection Initialised")
        return con
    else: 
        return print("No Database connection")
  
def Load_Create_DataTables():
    
    ''' Extract from CSV files and load data inside of Table'''
    
    con = Database_connection() 
    postcodes = con.execute("""
    CREATE TABLE postcodes AS
    SELECT *
    FROM read_csv_auto('postcodes_100k.csv')
    """)
    
    EPC = con.execute("""
    CREATE TABLE epc AS
    SELECT *
    FROM read_csv_auto('epc_subset.csv')
    """)
    
    return con

def PART_1 (): 
    
    ''' Query grabs a postcode and transforms to outcode,
    Joined on postcode and grouped '''
    
    con = Load_Create_DataTables()
    result1 = con.execute("""
    SELECT
        split_part(e.POSTCODE, ' ', 1) AS outcode,
        COUNT(*) AS epc_record_count
    FROM epc e
    JOIN postcodes p
    ON e.POSTCODE = p.pcds
    GROUP BY outcode
    ORDER BY epc_record_count DESC
    LIMIT 10
    """).fetchdf()
    print(result1)
    return result1

def PART_2():
    ''' 
    Query: Using the DuckDB (Median) -  To capture the median habitable room 
    
    '''
    con = Load_Create_DataTables()
    result2 = con.execute("""
    SELECT
        split_part(e.POSTCODE, ' ', 1) AS outcode,
        median(NUMBER_HABITABLE_ROOMS) AS median_habitable_rooms,
        COUNT(*) AS epc_record_count
    FROM epc e
    JOIN postcodes p
    ON e.POSTCODE = p.pcds
    WHERE NUMBER_HABITABLE_ROOMS IS NOT NULL
    AND NUMBER_HABITABLE_ROOMS > 0
    GROUP BY outcode
    HAVING COUNT(*) >= 10
    ORDER BY median_habitable_rooms DESC
    LIMIT 10
    """).fetchdf()
    
    print(result2)
    return result2


    
    

