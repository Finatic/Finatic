from scipy import optimize
import numpy as np


def portfolio_return(weights, annualized_returns):
    return weights.T @ annualized_returns


def portfolio_vol(weights, cov_mat):
    return np.dot(weights.T,  np.dot(cov_mat*252, weights)) ** 0.5


def max_sharp_ratio(annualized_returns, cov, risk_free):
    n = annualized_returns.shape[0]
    init_guess = np.repeat(1 / n, n)
    bounds = ((0.0, 1.0),) * n  # an N-tuple of 2-tuples!
    # construct the constraints
    weights_sum_to_1 = {'type': 'eq',
                        'fun': lambda weights_: np.sum(weights_) - 1
                        }

    def neg_sharpe(weights_, risk_free_, returns_, cov_):
        r = portfolio_return(weights_, returns_)
        vol = portfolio_vol(weights_, cov_)
        return -(r - risk_free_) / vol

    weights = optimize.minimize(neg_sharpe,
                                init_guess,
                                args=(risk_free, annualized_returns, cov),
                                method='SLSQP',
                                options={'disp': False},
                                constraints=(weights_sum_to_1,),
                                bounds=bounds)
    return weights.x
