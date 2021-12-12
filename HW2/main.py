import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def linear_regression(covariates, targets):
    covariates = np.array(covariates)
    targets = np.array(targets).reshape(-1,1)
    combination = np.hstack([covariates, targets])
    covariates = covariates[~np.isnan(combination).any(axis=1)]
    targets = targets[~np.isnan(combination).any(axis=1)]
    beta = np.matmul(np.matmul(np.linalg.inv(np.matmul(np.transpose(covariates), covariates)), np.transpose(covariates)), targets)
    y_hat = np.matmul(covariates, beta)
    errors = targets - y_hat
    variance = float(np.matmul(np.transpose(errors), errors) / (covariates.shape[0] - covariates.shape[1] - 1))
    variance_beta = []
    for index, coeff in enumerate(beta.tolist()):
        mean = float(covariates[:, index].mean())
        summation = 0
        for point in covariates[:, index].tolist():
            summation += pow(float(point) - mean, 2)
        variance_beta.append(variance/summation)
    variance_beta = np.array(variance_beta).reshape(-1,1)
    se_beta = np.sqrt(variance_beta)
    lower_bounds = beta - (2 * se_beta)
    upper_bounds = beta + (2 * se_beta)
    return beta[:,0], se_beta[:,0], lower_bounds[:,0], upper_bounds[:,0]


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df = pd.read_csv("games.csv", sep=",")

def manipulate_winner_col(val):
    if val == 'white':
        return 0
    elif val == 'black':
        return 1
    return 2


df['winner'] = df['winner'].apply(lambda x: manipulate_winner_col(x))

df['point_diff'] = df['white_rating'] - df['black_rating']
df['estimated_white_points'] = 1/(1+(10**(-df['point_diff']/400)))

# id,rated,created_at,last_move_at,turns,victory_status,winner,increment_code,white_id,white_rating,black_id,black_rating,moves,opening_eco,opening_name,opening_ply
df = df.drop(columns=["id","rated","created_at","last_move_at","victory_status","increment_code","white_id","black_id","moves","opening_eco","opening_name","opening_ply", "white_rating", "black_rating"])

covariates = df.drop("winner", axis=1).values
targets = df["winner"].values

print(df.drop("winner", axis=1).head())

beta, se_beta, lower_bounds, upper_bounds = linear_regression(covariates, targets)

result_table = pd.DataFrame.from_dict({"lower_bound_for_estimates": lower_bounds,
                                       "estimates": beta,
                                       "upper_bound_for_etimates": upper_bounds,
                                       "standard_errors": se_beta})

print("Result table:")
print(result_table)

plt.plot(lower_bounds)
plt.plot(beta)
plt.plot(upper_bounds)
plt.title("Result plot")
plt.legend(["lower_bound_for_estimates",
            "estimates",
            "upper_bound_for_estimates"])

plt.show()