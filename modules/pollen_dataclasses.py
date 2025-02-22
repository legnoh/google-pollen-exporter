from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Date:
    year: int
    month: int
    day: int

@dataclass
class Color:
    green: Optional[float] = None
    blue: Optional[float] = None

@dataclass
class IndexInfo:
    code: str
    displayName: str
    value: int
    category: str
    indexDescription: str
    color: Color

@dataclass
class PollenTypeInfo:
    code: str
    displayName: str
    inSeason: Optional[bool] = None
    indexInfo: Optional[IndexInfo] = None
    healthRecommendations: Optional[List[str]] = None

@dataclass
class PlantDescription:
    type: str
    family: str
    season: str
    specialColors: str
    specialShapes: str
    crossReaction: str
    picture: str
    pictureCloseup: str

@dataclass
class PlantInfo:
    code: str
    displayName: str
    inSeason: Optional[bool] = None
    indexInfo: Optional[IndexInfo] = None
    plantDescription: Optional[PlantDescription] = None

@dataclass
class DailyInfo:
    date: Date
    pollenTypeInfo: List[PollenTypeInfo]
    plantInfo: List[PlantInfo]

@dataclass
class PollenData:
    regionCode: str
    dailyInfo: List[DailyInfo]
