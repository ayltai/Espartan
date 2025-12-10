from sqlmodel import SQLModel, Field


class Settings(SQLModel, table=True):
    id                : int   = Field(primary_key=True, default=1)
    threshold_on      : float = Field(default=17.5, description='Temperature threshold to turn heating on')
    threshold_off     : float = Field(default=18.5, description='Temperature threshold to turn heating off')
    decision_strategy : str   = Field(default='min', description='Strategy for heating decision (e.g., min, avg)')
