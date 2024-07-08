
from datetime import datetime
from json import JSONEncoder

from auction.balance import Balance
from auction.model import Auction, Bid, Item


class PrivatePropertyEncoder(JSONEncoder):
    def _normalize_keys(self, dict: dict):
        new_dict = {}
        for item in dict.items():
            new_key = item[0][1:]
            new_dict[new_key] = item[1]
        return new_dict


class AuctionEncoder(PrivatePropertyEncoder):
    def default(self, o):
        if isinstance(o, Auction):
            props = o.__dict__.copy()
            props = self._normalize_keys(props)
            del props["bids"]
            return props
        elif isinstance(o, Bid):
            return BidEncoder().default(o)
        elif isinstance(o, Item):
            return ItemEncoder().default(o)
        elif isinstance(o, datetime):
            return DatetimeEncoder().default(o)

        return JSONEncoder.encode(self, o)


class BidEncoder(PrivatePropertyEncoder):
    def default(self, o):
        if isinstance(o, Bid):
            props = o.__dict__.copy()
            props = self._normalize_keys(props)
            return props
        elif isinstance(o, datetime):
            return DatetimeEncoder().default(o)

        return JSONEncoder.encode(self, o)


class ItemEncoder(PrivatePropertyEncoder):
    def default(self, o):
        if isinstance(o, Item):
            props = o.__dict__.copy()
            props = self._normalize_keys(props)
            return props

        return JSONEncoder.encode(self, o)


class DatetimeEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.timestamp()

        return JSONEncoder.encode(self, o)


class BalanceEncoder(PrivatePropertyEncoder):
    def default(self, o):
        if isinstance(o, Balance):
            props = o.__dict__.copy()
            props = self._normalize_keys(props)
            del props["account"]
            return props
        elif isinstance(o, set):
            return list(o)

        return JSONEncoder.encode(self, o)
