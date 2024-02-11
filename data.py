from typing import Union
from pydantic import BaseModel


class Point(BaseModel):
    x: float
    y: float
    z: Union[float, None] = None
    confidence: float = 1.0
    
    @property
    def xy(self) -> tuple:
        return self.x, self.y
    
    @property
    def xyz(self) -> tuple:
        return self.x, self.y, self.z


class Rectangle(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float = 1.0
    
    @property
    def xyxy(self) -> tuple:
        return self.x1, self.y1, self.x2, self.y2
    
    @property
    def cxywh(self) -> tuple:
        # (center_x, center_y, w, h)
        cx = (self.x1 + self.x2) / 2
        cy = (self.y1 + self.y2) / 2
        w = abs(self.x2 - self.x1)
        h = abs(self.y2 - self.y1)
        return cx, cy, w, h


class PoseData(BaseModel):
    """
    A set of a golf pose 
    """
    player:     Union[Rectangle, None] = None
    nose:       Union[Point, None] = None
    lEye:       Union[Point, None] = None
    rEye:       Union[Point, None] = None
    lEar:       Union[Point, None] = None
    rEar:       Union[Point, None] = None
    lShoulder:  Union[Point, None] = None
    rShoulder:  Union[Point, None] = None
    lElbow:     Union[Point, None] = None
    rElbow:     Union[Point, None] = None
    lWrist:     Union[Point, None] = None
    rWrist:     Union[Point, None] = None
    lHip:       Union[Point, None] = None
    rHip:       Union[Point, None] = None
    lKnee:      Union[Point, None] = None
    rKnee:      Union[Point, None] = None
    lAnkle:     Union[Point, None] = None
    rAnkle:     Union[Point, None] = None
    
    def __iter__(self):
        for attr in self.model_fields.keys():
            yield getattr(self, attr)
            
    def __setitem__(self, index: int, value: Union[Rectangle, Point]):
        name = self.names[index]
        setattr(self, name, value)
        
    def __getitem__(self, index: int):
        name = self.names[index]
        return getattr(self, name)
    
    @property
    def names(self):
        return list(self.__dict__.keys())