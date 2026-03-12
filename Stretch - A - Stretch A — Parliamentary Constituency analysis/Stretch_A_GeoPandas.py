import pandas as pd
import geopandas as gpd


def load_data_sources():
    """Load all required datasets."""
    postcodes = pd.read_csv("postcodes_100k.csv")
    constituencies = gpd.read_file("Parliamentary_Constituencies_July_2024.geojson")
    epc = pd.read_csv("epc_subset.csv")

    return postcodes, constituencies, epc


def create_postcode_geodataframe(postcodes):
    """Convert postcode dataframe into a GeoDataFrame."""
    postcodes_gdf = gpd.GeoDataFrame(
        postcodes,
        geometry=gpd.points_from_xy(postcodes["long"], postcodes["lat"]),
        crs="EPSG:4326"
    )

    return postcodes_gdf


def perform_spatial_join(postcodes_gdf, constituencies):
    """Assign each postcode to a constituency."""
    constituencies = constituencies.to_crs(postcodes_gdf.crs)

    postcode_constituency = gpd.sjoin(
        postcodes_gdf,
        constituencies,
        how="inner",
        predicate="within"
    )

    return postcode_constituency


def merge_epc_with_constituency(epc, postcode_constituency):
    """Merge EPC data with postcode → constituency mapping."""
    epc_constituency = epc.merge(
        postcode_constituency[["pcds", "PCON24NM"]],
        left_on="POSTCODE",
        right_on="pcds",
        how="inner"
    )

    return epc_constituency


def analyse_median_rooms(epc_constituency):
    """Calculate median habitable rooms by constituency."""

    epc_valid = epc_constituency[
        (epc_constituency["NUMBER_HABITABLE_ROOMS"].notna()) &
        (epc_constituency["NUMBER_HABITABLE_ROOMS"] > 0)
    ]

    result = (
        epc_valid
        .groupby("PCON24NM")
        .agg(
            median_habitable_rooms=("NUMBER_HABITABLE_ROOMS", "median"),
            epc_record_count=("NUMBER_HABITABLE_ROOMS", "count")
        )
        .reset_index()
    )

    result = result[result["epc_record_count"] >= 10]

    result = result.sort_values(
        by="median_habitable_rooms",
        ascending=False
    )

    result = result.head(10)

    return result


def main():
    postcodes, constituencies, epc = load_data_sources()

    postcodes_gdf = create_postcode_geodataframe(postcodes)

    postcode_constituency = perform_spatial_join(
        postcodes_gdf,
        constituencies
    )

    epc_constituency = merge_epc_with_constituency(
        epc,
        postcode_constituency
    )

    result = analyse_median_rooms(epc_constituency)
    print(result)
    return result


if __name__ == "__main__":
    main()