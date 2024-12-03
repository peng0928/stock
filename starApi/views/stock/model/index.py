from pydantic import BaseModel, Field


class StockItem(BaseModel):
    code: str = Field(default=None, title="The code of the stock", max_length=10)


class StockTrend(StockItem):
    hy: str = Field(default=None, max_length=10)
    dp: str = Field(default=None, max_length=10)
