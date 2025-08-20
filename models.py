from pydantic import BaseModel, ConfigDict, Field
from pygments.lexer import default


class Headers(BaseModel):
    host: str
    user_agent: str = Field(alias='user-agent')
    content_encoding: str = Field(alias='content-encoding')
    content_type: str = Field(alias='content-type')
    traceparent: str
    hook_token: str = Field(alias='x-hooktoken')
    spread_batch_id: str = Field(alias='x-spreadbatchid')
    accept_encoding: str = Field(alias='accept-encoding')

    model_config = ConfigDict(
        extra='ignore',
        #populate_by_name=True
    )

class Chain(BaseModel):
    chain: str
    deposit_enabled: bool = Field(alias='depositEnabled')
    withdraw_enabled: bool = Field(alias='withdrawEnabled')
    withdraw_fee: float = Field(alias='withdrawFee')
    min_confirm: int = Field(alias='minConfirm')

    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True
    )

class Spread(BaseModel):
    profit_index_max: float = Field(alias='profitIndexMax')
    profit_index_min: float = Field(alias='profitIndexMin')
    profit_index_avg: float = Field(alias='profitIndexAvg')
    volume: float
    buy_price_min: float = Field(alias='buyPriceMin')
    buy_price_max: float = Field(alias='buyPriceMax')
    buy_price_avg: float = Field(alias='buyPriceAvg')
    sell_price_min: float = Field(alias='sellPriceMin')
    sell_price_max: float = Field(alias='sellPriceMax')
    sell_price_avg: float = Field(alias='sellPriceAvg')
    exchange_buy: str = Field(alias='exchangeBuy')
    exchange_sell: str = Field(alias='exchangeSell')
    symbol: str
    buy_exchange_funding_rate: float = Field(alias='buyExchangeFundingProfitModifier', default=0)
    sell_exchange_funding_rate: float = Field(alias='sellExchangeFundingProfitModifier', default=0)
    buy_exchange_next_funding_apply_time: int = Field(alias='buyExchangeNextFundingTime', default=0)
    sell_exchange_next_funding_apply_time: int = Field(alias='sellExchangeNextFundingTime', default=0)
    overall_profit_index_max: float = Field(alias='overallProfitIndexMax')
    overall_profit_index_min: float = Field(alias='overallProfitIndexMin')
    overall_profit_index_avg: float = Field(alias='overallProfitIndexAvg')
    original_symbol: str = Field(alias='originalSymbol')
    volume_usd: float = Field(alias='volumeUsd')
    lifetime: int
    chains_buy: list[Chain] = Field(alias='chainsBuy', default=[])
    chains_sell: list[Chain] = Field(alias='chainsSell', default=[])
    updated: int
    is_futures: bool = Field(alias='isFutures')

    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True
    )

class HookRecord(BaseModel):
    hook_token: str
    receive_date: int #in milliseconds
    receive_date_str: str
    headers: Headers
    received_body: list[Spread]
    response_date: float | None = Field(default=None)
    response_body: dict
    error: str | None = Field(default=None)

    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True
    )