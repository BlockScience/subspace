# Time units
Days = float
Blocks = float  # 1 block ~ 6s. Or 1 day ~ 14400 blocks
Seconds = float
PerYear = float  # Yearly rate
Year = float  # Number of years
Picoseconds = float  # Number of Picoseconds

# Measurement units
Credits = float
CreditsPerComputeWeights = float
CreditsPerDay = float
CreditsPerBlock = float
ComputeWeights = float
Shannon = float  # 1e-18 SSC
ShannonPerComputeWeights = float

# Storage
Bytes = float
Chunk = int  # As per Subnomicon: 1 chunk = 32 Bytes
# As per Subnomicon: 2**15 Chunks (~1MB)
RawRecord = Chunk
Piece = int  # As per Subnomicon: 1 piece = 1 record + commitment + witness
# As per Subnomicon: a transformed raw record.
Record = Piece
# As per Subnomicon: 1000 Pieces or ~ 1 GiB
Sector = Piece

# As per Subnomicon: A collection of potential partial or full blocks.
# Can be either a fixed-size portion of the Blockchain History
# or a fixed-size portion of the Archived History
Segment = Bytes
RecordedHistorySegment = Record
ArchivedHistorySegment = Piece

# Taxonomy:
# Chunk < Record/Piece < Sector < Plot < History

# Misc units
Percentage = float
