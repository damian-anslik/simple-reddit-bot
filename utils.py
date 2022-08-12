from time import strftime


def is_valid_ticker(ticker_symbol: str) -> bool:
    if not ticker_symbol.isupper():
        return False
    return True

def is_access_token_valid(token_expiry_time: str) -> bool:
    if token_expiry_time is None:
        return False
    return token_expiry_time > strftime("%Y-%m-%d %H:%M:%S")