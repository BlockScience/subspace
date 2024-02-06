from typing import Annotated, Callable, NamedTuple, Optional, TypedDict, Union

# Time units
Blocks = Annotated[float, "blocks"]  # 1 block ~ 6s. Or 1 day ~ 14400 blocks
Days = Annotated[float, "days"]  # Number of days
Seconds = Annotated[float, "s"]
PerYear = Annotated[float, "1/year"]  # Yearly rate
Year = Annotated[float, "year"]  # Number of years
Picoseconds = Annotated[float, "ps"]  # Number of Picoseconds

# Measurement units
Credits = Annotated[float, "SSC"]
CreditsPerComputeWeights = Annotated[float, "SSC/CW"]
CreditsPerDay = Annotated[float, "SSC/day"]
ComputeWeights = Annotated[float, "CW"]
Shannon = Annotated[float, "Shannon"]  # 1e-18 SSC
ShannonPerComputeWeights = Annotated[float, "Shannon/CW"]

# Storage
Bytes = Annotated[int, "bytes"]
Chunk = Annotated[int, "chunk"]  # As per Subnomicon: 1 chunk = 32 Bytes
RawRecord = Annotated[Chunk, "raw_record"]  # As per Subnomicon: 2**15 Chunks (~1MB)
Piece = Annotated[
    int, "piece"
]  # As per Subnomicon: 1 piece = 1 record + commitment + witness
Record = Annotated[Piece, "record"]  # As per Subnomicon: a transformed raw record.
Sector = Annotated[Piece, "sector"]  # As per Subnomicon: 1000 Pieces or ~ 1 GiB

# As per Subnomicon: A collection of potential partial or full blocks.
# Can be either a fixed-size portion of the Blockchain History
# or a fixed-size portion of the Archived History
Segment = Annotated[Bytes, "segment"]
RecordedHistorySegment = Annotated[Record, "record_segment"]
ArchivedHistorySegment = Annotated[Piece, "archive_segment"]

# Taxonomy:
# Chunk < Record/Piece < Sector < Plot < History

# Misc units
Percentage = Annotated[float, "%"]

# Logic implementation types
StochasticFunction = Callable[[SubspaceModelParams, SubspaceModelState], float]
