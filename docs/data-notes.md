# Yellow Taxi Trip Data Notes

## Source

The source is the [NYC TLC Trip Record Data page](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).
The project downloaded the January, February, and March 2024 Yellow Taxi trip files from:

- [January 2024 parquet](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet)
- [February 2024 parquet](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-02.parquet)
- [March 2024 parquet](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-03.parquet)

The column meanings below come from the local TLC data dictionary: `docs/data_dictionary_trip_records_yellow.pdf`.
The zone IDs are interpreted with `data/taxi_zone_lookup.csv`.

## What's in it

The three files contain 19 columns:

| Column | Meaning |
| --- | --- |
| `VendorID` | Technology provider that recorded the trip. |
| `tpep_pickup_datetime` | Date and time when the meter was engaged. |
| `tpep_dropoff_datetime` | Date and time when the meter was disengaged. |
| `passenger_count` | Number of passengers reported by the driver. |
| `trip_distance` | Trip distance in miles reported by the taximeter. |
| `RatecodeID` | Final rate code in effect for the trip. |
| `store_and_fwd_flag` | Whether the trip record was stored in the vehicle and sent later because of a connectivity issue (`Y`/`N`). |
| `PULocationID` | TLC Taxi Zone where the meter was engaged. Join this ID to the zone lookup. |
| `DOLocationID` | TLC Taxi Zone where the meter was disengaged. Join this ID to the zone lookup. |
| `payment_type` | Numeric code for the payment method used. |
| `fare_amount` | Time-and-distance fare calculated by the meter. |
| `extra` | Extra charges and surcharges, excluding the other separately listed amounts. |
| `mta_tax` | Automatically triggered MTA tax. |
| `tip_amount` | Tip paid by the passenger. Credit-card tips are recorded; cash tips are not included. |
| `tolls_amount` | Total tolls paid during the trip. |
| `improvement_surcharge` | Improvement surcharge assessed on the trip. |
| `total_amount` | Total amount charged to the passenger, excluding cash tips. |
| `congestion_surcharge` | Congestion surcharge, where applicable. |
| `Airport_fee` | Airport fee, where applicable. |

For payment analysis, the TLC codes used in these files are: `1` credit card, `2` cash, `3` no charge, `4` dispute, and `0` unknown.

## Volume

The following figures were measured from the parquet files currently in `data/`. File sizes are the local sizes in decimal MB; row counts include every row in each file.

| Month | Rows | File size |
| --- | ---: | ---: |
| January 2024 | 2,964,624 | 49.96 MB |
| February 2024 | 3,007,526 | 50.35 MB |
| March 2024 | 3,582,628 | 60.08 MB |
| **Total** | **9,554,778** | **160.39 MB** |

## Known issues

These findings came from profiling all three parquet files together:

- Pickup timestamps include 2,801 rows where drop-off is at or before pickup. The files also contain historical-looking pickup timestamps from 2002 and 2008, so date-range validation is required before monthly reporting.
- There are 215,764 rows with zero or negative `trip_distance`.
- There are 139,596 rows with zero or negative `fare_amount`.
- Optional fields are null in 751,962 rows, including `passenger_count`, `RatecodeID`, `store_and_fwd_flag`, `congestion_surcharge`, and `Airport_fee`. These nulls occur together and should not automatically be treated as zero.
- `payment_type` contains 751,962 rows with code `0` (unknown), in addition to the documented codes for credit card, cash, no charge, and dispute.
- The trip files are monthly extracts, so a Gold-layer month or day filter should be based on validated pickup timestamps rather than trusting the filename alone.
- Zone IDs should be joined to the lookup table before presenting zone names. The files contain 262 distinct pickup IDs and 261 distinct drop-off IDs in this sample, so unmatched or unexpected IDs should be checked during ingestion.

## Business questions for the Gold layer

The curated Gold layer should answer questions such as:

- How many trips occurred each day, and what was the total revenue?
- Which 10 pickup zones had the most trips? This requires joining `PULocationID` to `taxi_zone_lookup.csv`.
- What is the payment-type mix by month, day, or zone?
- What is the average tip by hour of day?
- Which pickup and drop-off zone pairs are most common?
- How do average fare, distance, duration, and total amount vary by zone and time period?
- What share of trips has invalid distance, fare, or timestamp values, and how does that affect reported KPIs?
