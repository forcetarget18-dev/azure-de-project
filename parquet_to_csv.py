from pathlib import Path

import pandas as pd
import pyarrow.parquet as parquet


PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = DATA_DIR / "converted_csv"


def convert_parquet_files() -> None:
	OUTPUT_DIR.mkdir(exist_ok=True)
	parquet_files = sorted(DATA_DIR.glob("*.parquet"))

	if not parquet_files:
		raise FileNotFoundError(f"No Parquet files found in {DATA_DIR}")

	for parquet_file in parquet_files:
		csv_file = OUTPUT_DIR / f"{parquet_file.stem}.csv"
		if csv_file.exists():
			csv_file.unlink()

		parquet_reader = parquet.ParquetFile(parquet_file)
		for batch_number, batch in enumerate(parquet_reader.iter_batches(), start=1):
			dataframe = batch.to_pandas()
			dataframe.to_csv(
				csv_file,
				mode="a",
				header=batch_number == 1,
				index=False,
			)

		print(f"Converted {parquet_file.name} -> {csv_file.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
	convert_parquet_files()

