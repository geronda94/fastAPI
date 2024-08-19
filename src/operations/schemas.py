from pydantic import BaseModel
import datetime



class OperationCreate(BaseModel):
    quantity: str
    figi: str
    instrument_type: str
    date: datetime.datetime
    type: str
    
    
class OperationModel(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime.datetime
    type: str