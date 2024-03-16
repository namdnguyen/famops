import os
import posixpath
from typing import Iterator

import dlt
from dlt.sources import TDataItems

try:
    from .filesystem import FileItemDict, filesystem, readers, read_csv  # type: ignore
except ImportError:
    from filesystem import (
        FileItemDict,
        filesystem,
        readers,
        read_csv,
    )


def read_csv_with_duckdb() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="quantified_filesystem",
        destination="duckdb",
        dataset_name="quantified_data_duckdb",
    )

    # load all the CSV data, excluding headers
    quantified_files = readers(
        file_glob="*.csv"
    ).read_csv_duckdb(chunk_size=5000, header=True)

    load_info = pipeline.run(quantified_files,
                             table_name = "quantified",
                             write_disposition = "replace")

    print(load_info)
    print(pipeline.last_trace.last_normalize_info)


if __name__ == "__main__":
    read_csv_with_duckdb()
