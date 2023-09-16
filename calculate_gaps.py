import yfinance as yf
from typing import Dict

def calculate_gaps(ticker: str, start_date: str, end_date: str) -> Dict[str, int]:
    """
    Calculate gap-related statistics for a specified stock ticker within a given date range.

    Parameters:
    - ticker (str): The stock ticker symbol to fetch data for.
    - start_date (str): The start date for the analysis in "YYYY-MM-DD" format.
    - end_date (str): The end date for the analysis in "YYYY-MM-DD" format.

    Returns:
    A dictionary containing the following gap-related counts:
    - "Weekly_Gap_Up_Count" (int): The count of weekly gap up occurrences.
    - "Weekly_Gap_Down_Count" (int): The count of weekly gap down occurrences.
    - "Gap_Fill_Up_Count" (int): The count of gap fill up occurrences.
    - "Gap_Fill_Down_Count" (int): The count of gap fill down occurrences.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date, interval="1wk")
    except Exception as e:
        raise Exception(f"Error fetching data for {ticker}: {e}")

    data["Week_Gap_Up"] = (data["Open"] - data["Close"].shift(1)) > 0
    data["Week_Gap_Down"] = (data["Open"] - data["Close"].shift(1)) < 0

    data["Gap_Fill_Up"] = (data["Low"].shift(1) - data["Open"]) > 0
    data["Gap_Fill_Down"] = (data["High"].shift(1) - data["Open"]) < 0

    data.reset_index(inplace=True)

    gap_up_count: int = data["Week_Gap_Up"].sum()
    gap_down_count: int = data["Week_Gap_Down"].sum()
    gap_fill_up_count: int = data["Gap_Fill_Up"].sum()
    gap_fill_down_count: int = data["Gap_Fill_Down"].sum()

    return {
        "Weekly_Gap_Up_Count": gap_up_count,
        "Weekly_Gap_Down_Count": gap_down_count,
        "Gap_Fill_Up_Count": gap_fill_up_count,
        "Gap_Fill_Down_Count": gap_fill_down_count,
    }

if __name__ == "__main__":
    ticker_symbol = "^NSEBANK"
    start_date = "2017-01-01"
    end_date = "2023-01-01"
    
    try:
        result = calculate_gaps(ticker_symbol, start_date, end_date)
        print(result)
    except Exception as e:
        print(f"An error occurred: {e}")


