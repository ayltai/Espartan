from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Relay(SQLModel, table=True):
    id        : Optional[int] = Field(primary_key=True, default=None)
    device_id : str           = Field(foreign_key='device.id', ondelete='CASCADE', description='Device controlling the relay')
    timestamp : datetime      = Field(description='Timestamp of the relay state change')
    state     : int           = Field(description='Relay state: 0 for off, 1 for on')
