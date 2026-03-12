import duckdb
import os
import glob
def data_load():
    # 1. Define paths (using r"" to handle Windows backslashes)
    base_path = r"C:\Users\lenno\AppData\Local\Microsoft\Olk\Attachments\ooa-387b2934-0fd6-44e9-8616-f32438799efb\eac88b8c87dc4ce77fd2fbfd2587472823640dda862428f6496fe99acfd14e46\Candidate Task\Candidate Task\task_b"
    epc_pattern = os.path.join(base_path, "all-domestic-certificates", "**", "certificates.csv").replace('\\', '/')
    onspd_path = 'ONSPD_NOV_2025_UK.csv'
    constituency_geo = constituency_geo = r"C:\Users\lenno\OneDrive\Desktop\task_b\Parliamentary_Constituencies_July_2024.geojson"

    # 2. Setup DuckDB
    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial;")
    return con, epc_pattern, onspd_path, constituency_geo
    
def query_execution(con, epc_pattern, onspd_path, constituency_geo):
# 3. Execution Query
    query = f"""
        -- Step A: Load Postcode lookup table
        CREATE OR REPLACE TABLE postcode_map AS 
        SELECT 
            pcds AS postcode, 
            st_point(long, lat) AS point_geom
        FROM read_csv_auto('{onspd_path}')
        WHERE long IS NOT NULL AND lat IS NOT NULL;

        -- Step B: Load and aggregate EPC data
        -- We use QUALIFY to ensure one EPC per property
        CREATE OR REPLACE TABLE epc_latest AS 
        SELECT 
            POSTCODE, 
            CAST(NUMBER_HABITABLE_ROOMS AS INTEGER) AS habitable_rooms
        FROM read_csv_auto('{epc_pattern}', ignore_errors=True)
        WHERE NUMBER_HABITABLE_ROOMS IS NOT NULL
        QUALIFY ROW_NUMBER() OVER (PARTITION BY UPRN ORDER BY INSPECTION_DATE DESC) = 1;

        -- Step C: Spatial Join and Analysis
        SELECT 
            c.pcon24nm AS constituency_name, 
            median(e.habitable_rooms) AS median_habitable_rooms
        FROM st_read('{constituency_geo.replace('\\', '/')}') AS c
        JOIN postcode_map p ON st_intersects(c.geom, p.point_geom)
        JOIN epc_latest e ON p.postcode = e.POSTCODE
        GROUP BY c.pcon24nm
        ORDER BY median_habitable_rooms DESC;
    """
    return query
def main():
    con, epc_pattern, onspd_path, constituency_geo = data_load()
    query = query_execution(con, epc_pattern, onspd_path, constituency_geo)
    result_df = con.execute(query).df()
    print(result_df.head(10))
    return result_df  # Show top 10 results for quick viewing

if __name__ == "__main__":
# Run the analysis
    result_df = main()

# 4. Display Results
    print("\n--- Median Habitable Rooms by Constituency ---")
    print(result_df)

    # Optional: Save to file for easy viewing in GIS
    result_df.to_csv("median_habitable_rooms_by_constituency.csv", index=False)
    print("\nResults saved to 'median_habitable_rooms_by_constituency.csv'")

