from sqlmodel import SQLModel, Session, select, Field





class Items(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    name : str
    description : str | None = None
    price : int
    in_stock : bool = True
    
