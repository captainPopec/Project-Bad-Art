from scipy import stats
import pandas as pd


dfb = pd.read_csv('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Fltrd.csv', encoding='latin1')
#dfb = df.dropna(subset=['tActivity', 'H', 'AGI'])
dfa = pd.read_csv('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/nonFltrd.csv', encoding='latin1')
#dfa = df.dropna(subset=['tActivity', 'H', 'AGI'])

#dfb = pd.to_numeric(dfb, errors='coerce')
#dfa = pd.to_numeric(dfa, errors='coerce')

columns=['log(med*ACI*H', 'log(AGI*H*med)','S2N *med ', 'S2N *med *H','Median*Tactivity*H*AGI','log(S2N*AGI*median', 'log(AGI*tAct)']

for name in columns:


    b = dfb[name]  
    a = dfa[name]  

    # Perform the two-sample t-test
    t_statistic, p_value = stats.ttest_ind(a, b)

    #print("T-statistic of "+ name +": ", t_statistic)
    print("P-value_"+ name +": ", p_value)
    print()
