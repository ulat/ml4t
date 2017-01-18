import datetime as dt
import numpy as np
import pandas as pd
import scipy.optimize as sco
from mc1_p1 import util as util
from mc1_p1.analysis import compute_daily_returns, compute_portfolio_stats


def optimize_portfolio(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), syms=['GOOG', 'AAPL', 'GLD', 'XOM'],
                       gen_plot=False):
    """ Finds optimal allocations for a given set of stocks. Optimizes for sharp ratio
    :param syms: list of ticker symbols
    :param sd: startdate
    :param ed: enddate
    :param gen_plot: If True, create a plot named plot.png
    :return: list of floats as 1-dim np-array that represents allocation to each of the equities.
    """
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = util.get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    noa = len(syms)
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bnds = tuple((0, 1) for x in range(noa))

    fun = lambda inputs: -compute_portfolio_stats(prices, inputs)[3]
    opts = sco.minimize(fun, noa * [1. / noa, ], method='SLSQP', bounds=bnds, constraints=cons)
    allocs = opts.x.round(4)
    cr, adr, sddr, sr = compute_portfolio_stats(prices, allocs)

    # Get daily portfolio value
    normed = prices / prices.ix[0]
    alloced = normed * allocs
    port_vals = alloced.sum(axis=1)
    port_val = compute_daily_returns(port_vals)  # add code here to compute daily portfolio values

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_vals, prices_SPY / prices_SPY[0]], keys=['Portfolio', 'SPY'], axis=1)
        util.plot_data(df_temp)
        pass

    return allocs, cr, adr, sddr, sr


def test_code():
    # Testcase 1:
    sd = dt.datetime(2010, 1, 1)
    ed = dt.datetime(2010, 12, 31)
    syms = ['GOOG', 'AAPL', 'GLD', 'XOM']
    gen_plot=False

    llocs, cr, adr, sddr, sr = optimize_portfolio(sd, ed, syms, gen_plot)
    print llocs
    print cr
    print adr
    print sddr
    print sr

if __name__ == "__main__":
    test_code()