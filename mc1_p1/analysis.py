"""MC1-P1: Analyze a portfolio."""
import numpy as np
import datetime as dt
import pandas as pd
from util import get_data, plot_data


def compute_daily_returns(df):
    # Compute and return the daily return values
    daily_returns = df.copy()
    daily_returns = daily_returns / daily_returns.shift(1) - 1
    return daily_returns[1:].values


def compute_portfolio_stats(prices, allocs=[0.1, 0.2, 0.3, 0.4], rfr=0.0,
                            sf=252.0):
    normed = prices / prices.ix[0]
    alloced = normed * allocs

    port_vals = alloced.sum(axis=1)

    daily_rets = compute_daily_returns(port_vals)
    daily_rets = daily_rets[1:]

    cr = port_vals[-1] / port_vals[0] - 1
    adr = daily_rets.mean()
    sddr = daily_rets.std()
    sr = (daily_rets - rfr).mean() / (daily_rets).std() * np.sqrt(sf)

    return cr, adr, sddr, sr


# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def assess_portfolio(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1),
                     syms=['GOOG', 'AAPL', 'GLD', 'XOM'],
                     allocs=[0.1, 0.2, 0.3, 0.4],
                     sv=1000000, rfr=0.0, sf=252.0,
                     gen_plot=False):
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get daily portfolio value
    prices_SPY = prices_SPY / prices_SPY[0]
    normed_prices = prices / prices.ix[0]
    alloced = normed_prices * allocs
    pos_vals = alloced * sv
    port_vals = pos_vals.sum(axis=1)

    # Get portfolio statistics (note: std_daily_ret = volatility)
    # cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1]
    # add code here to compute stats
    cr, adr, sddr, sr = compute_portfolio_stats(prices, allocs, rfr, sf)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_vals, normed_prices], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp)
        #pass

    # Add code here to properly compute end value
    ev = sv * (1 + cr)

    return cr, adr, sddr, sr, ev


def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2010, 12, 31)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000
    risk_free_rate = 0.0
    sample_freq = 252
    '''
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2010, 12, 31)
    symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
    allocations = [0.0, 0.0, 0.0, 1.0]
    start_val = 1000000
    risk_free_rate = 0.0
    sample_freq = 252

    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]
    '''
    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd=start_date, ed=end_date,
                                             syms=symbols,
                                             allocs=allocations,
                                             sv=start_val,
                                             gen_plot=False)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    test_code()
