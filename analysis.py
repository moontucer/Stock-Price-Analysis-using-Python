#Imported libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import tqdm as tqdm

#Table of daily $AMZN stock return creation and adding return columns based on higher price 

return_quot_amzn=pd.read_csv("C:\Users\YourUserName\Downloads\AMZN.csv",index_col=0)
return_quot_amzn['daily_return'] = (return_quot_amzn['High']/ return_quot_amzn['High'].shift(1)) -1
return_quot_amzn.dropna(inplace = True)
return_quot_amzn.head(5)

#Table of daily $MSFT stock return creation and adding return columns based on higher price 

return_quot_MSFT=pd.read_csv("C:\Users\YourUserName\Downloads\MSFT.csv",index_col=0)
return_quot_MSFT['daily_return'] = (return_quot_MSFT['High']/ return_quot_MSFT['High'].shift(1)) -1
return_quot_MSFT.dropna(inplace = True)
return_quot_MSFT.head(5)

#Joining the two tables making use of return values

portfolio=pd.DataFrame().assign(Return_AMZN=return_quot_amzn['daily_return'],Return_MSFT=return_quot_MSFT['daily_return'])
portfolio.head(5)

#Annual return in $$ when we're able to trade (no. 252)

mus=((1+portfolio.mean()))**252 - 1
mus

#Covariance

cov=portfolio.cov()*252
cov

#Monte-Carlo Approach to generate Portfolios

n_stocks=2 #In the portfolio
n_portefeuille=1000 #when testing
moyenne_variance_pairs=[] #Stocking list of pairs of averages and variances
np.random.seed(75)

#Loop for generating porfolios
for i in range(n_portefeuille):

    # Choosing randomly portfolio variations
    stocks = np.random.choice(list(portfolio.columns), n_stocks, replace=False)

    # Choosing weights randomly
    poids = np.random.rand(n_stocks)
    poids = poids/sum(poids) #sum=1

    # Loop for calculating return and variance of portfolios
    portfolio_E_Variance = 0
    portfolio_E_Retour = 0
    for i in range(len(stocks)):
        portfolio_E_Retour += poids[i] * mus.loc[stocks[i]]
        for j in range(len(stocks)):
            
            # Add variance & covariance
            portfolio_E_Variance += poids[i] * poids[j] * cov.loc[stocks[i], stocks[j]]
            
    # Add average return to the list
    moyenne_variance_pairs.append([portfolio_E_Retour, portfolio_E_Variance])

averages=[]
variances=[]
for i in range(len(moyenne_variance_pairs)):
    averages.append(moyenne_variance_pairs[i][0])
    variances.append(moyenne_variance_pairs[i][1])
risk_free_rate=0.5
for i in range(len(averages)):
    averages[i]=averages[i]-risk_free_rate
plt.scatter(variances,averages)
plt.xlabel('Variances')
plt.ylabel('Averages')
plt.title('Final plot ')
plt.show()