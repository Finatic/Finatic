from scipy import optimize
import numpy as np
import pandas as pd


def portfolio_return(weights, annualized_returns):
    return weights.T @ annualized_returns


def portfolio_vol(weights, cov_mat):
    return np.dot(weights.T, np.dot(cov_mat * 252, weights)) ** 0.5


def max_sharp_ratio(annualized_returns, cov, risk_free):
    n = annualized_returns.shape[0]
    init_guess = np.repeat(1 / n, n)
    bounds = ((1 / (4 * n), 3 / n),) * n  # an N-tuple of 2-tuples!
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


def minimize_vol(target_return, returns, cov):
    n = returns.shape[0]
    init_guess = np.repeat(1 / n, n)
    bounds = ((0.0, 1.0),) * n  # Range of allowed weights

    # Defining the constraints
    weights_sum_to_1 = {'type': 'eq',
                        'fun': lambda weights: np.sum(weights) - 1
                        }
    return_is_target = {'type': 'eq',
                        'args': (returns,),
                        'fun': lambda weights, returns: target_return - portfolio_return(weights, returns)
                        }
    weights = optimize.minimize(portfolio_vol, init_guess,
                                args=(cov,), method='SLSQP',
                                options={'disp': False},
                                constraints=(weights_sum_to_1, return_is_target),
                                bounds=bounds)
    return weights.x


def calc_optimal_weights(n_points, returns, cov):
    target_rs = np.linspace(returns.min(), returns.max(), n_points)
    weights = [minimize_vol(target_return, returns, cov) for target_return in target_rs]
    return weights


def ef_curve(returns, risk_free_rate, n=50):
    ret = returns.copy()
    annualized_returns = (returns + 1).prod() ** (252 / returns.shape[0]) - 1
    optimal_weights = calc_optimal_weights(n, annualized_returns, ret.cov())
    result = pd.DataFrame(optimal_weights)
    result.columns = ret.columns
    result = result * 100
    result["portfolio_returns"] = [portfolio_return(w, annualized_returns) * 100 for w in optimal_weights]
    result["portfolio_volatility"] = [portfolio_vol(w, returns.cov()) * 100 for w in optimal_weights]
    result["sharpe_ratio"] = (result["portfolio_returns"] - risk_free_rate) / result["portfolio_volatility"]
    result = np.round(result, 2)
    return result
