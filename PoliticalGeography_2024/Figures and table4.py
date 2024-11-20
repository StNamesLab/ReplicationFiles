
'''
*********************************************************************************************************
****                                                                                                 ****
****  Do women commemorate women? How gender and ideology affect decisions on naming female streets  ****
****                                                                                                 ****
****                 Caballero-Cordero, Carmona-Derqui & Oto-Peralías                                ****
****                                                                                                 ****
****                                POLITICAL GEOGRAPHY                                              ****
****                                                                                                 ****
*********************************************************************************************************

*********************************************************************************************************
****                                  FIGURES AND TABLE 4                                            ****
*********************************************************************************************************
'''

#%% INITIAL IMPORTS
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mstats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.ticker as ticker
plt.rcParams['font.family'] = 'Arial'

#%% DESCRIPTIVE FIGURE (FIG 2)

# Read and process data
df=pd.read_stata("C:/Users/danie/Dropbox/Alcaldes/Do files/Replication_files/data_figure2.dta")
df01=df.loc[df.year==2001].copy()
df01.rename(columns={"fs":"fs01"},inplace=True)
df=df.merge(df01[["mun_code","fs01"]],on="mun_code",how="left")
df.fs=df.fs-df.fs01
df.fs=mstats.winsorize(df.fs, limits=[0.05, 0.05])
cols=["mun_code","year","left",'woman']
df_group=df[cols].groupby("mun_code", as_index=False).sum()

df_group["left_g"]=0
df_group.loc[df_group.left>df_group.left.median(),"left_g"]=1
df_group["w_g"]=0
df_group.loc[df_group.woman>df_group.woman.median(),"w_g"]=1

df=df.merge(df_group[["mun_code","left_g","w_g"]], on="mun_code",how="left")

# Fitting regression

col_names = df['year'].dropna().unique().tolist()
df[col_names] = pd.get_dummies(df['year'])

# Ideology
Y = df.loc[df.left_g==0,'fs']
X = df.loc[df.left_g==0,col_names]
m_left0 = sm.OLS(Y,X).fit()

Y = df.loc[df.left_g==1,'fs']
X = df.loc[df.left_g==1,col_names]
m_left1 = sm.OLS(Y,X).fit()

# Gender
Y = df.loc[df.w_g==0,'fs']
X = df.loc[df.w_g==0,col_names]
m_wom0 = sm.OLS(Y,X).fit()

Y = df.loc[df.w_g==1,'fs']
X = df.loc[df.w_g==1,col_names]
m_wom1 = sm.OLS(Y,X).fit()



fig,(ax1,ax2)=plt.subplots(1,2,sharey=True,figsize=(8,4), dpi=300)
# Ax1: Gender
    # Initial dot
ax1.plot(2000.8,0,fillstyle="left",c='slateblue', markerfacecoloralt='lightseagreen',marker='.',markeredgecolor='None',markersize=12)
    # 
ax1.plot(m_wom1.params, color='slateblue', label="Some years with a woman mayor")
ax1.fill_between(m_wom1.params.index, m_wom1.conf_int()[0], m_wom1.conf_int()[1], alpha=.1, color='slateblue')
ax1.plot(m_wom0.params, color='lightseagreen', label="No year with a woman mayor")
ax1.fill_between(m_wom0.params.index, m_wom0.conf_int()[0], m_wom0.conf_int()[1], alpha=.1, color='lightseagreen')
ax1.spines[['top','right']].set_visible(False)
ax1.xaxis.set_tick_params(labelsize=9)
ax1.set_title("A. Gender", size=10)
ax1.legend(frameon=False, fontsize=8, loc='lower right')
ax1.yaxis.set_tick_params(labelsize=9)
ax1.xaxis.set_tick_params(labelsize=9)
ax1.set_ylabel("Variation in Female share since 2001 (in pps.)\n", size=8)
# Ax2: Ideology
    # Initial dot
ax2.plot(2000.8,0,fillstyle="left",c='crimson', markerfacecoloralt='deepskyblue',marker='.',markeredgecolor='None',markersize=12)
    # 
ax2.plot(m_left1.params, color='crimson', label="More years with left-wing mayor")
ax2.fill_between(m_left1.params.index, m_left1.conf_int()[0], m_left1.conf_int()[1], alpha=.1, color='crimson')
ax2.plot(m_left0.params, color='deepskyblue', label="Less years with left-wing mayor")
ax2.fill_between(m_left0.params.index, m_left0.conf_int()[0], m_left0.conf_int()[1], alpha=.1, color='deepskyblue')
ax2.spines[['top','right']].set_visible(False)
ax2.set_title("B. Ideology", size=10)
ax2.legend(frameon=False, fontsize=8, loc='lower right')
fig.text(0.07,-0.02,"Notes: The figure shows the average increase in the female share with respect to 2001 (in pps.). Municipalities are classified into two groups \n\
according to the median of the number of years with a woman (A) or left-wing mayor (B) during the period 2001-2023.",
         size=7.5)
fig.text(0.5,1.07,"Figure 2. Increase in the female share depending on the mayor's gender and ideology", horizontalalignment="center", weight="bold", size=10)
fig.text(0.5,1.01,"Period 2001-2023", horizontalalignment="center")
plt.show()


#%% RDD FIGURE (FIG 3)
df=pd.read_stata("C:/Users/danie/Dropbox/Alcaldes/Do files/Replication_files/DATA2.dta")
c=50

# Ideology variables
df['ideologyrace'] = np.where(((df['left_1'] == 1) & (df['right_2'] == 1)) | ((df['left_2'] == 1) & (df['right_1'] == 1)), 1, 0)
df['votosLeft'] = (df['votes1']*df['left_1'] + df['votes2']*df['left_2'] + df['votes3']*df['left_3'])/df['Totalvotes']*100
df['votosLeft'].fillna(0, inplace=True)
df = df[df['votosLeft'] <= 100]
df['votosLeft2']=df['votosLeft']*df['votosLeft']
df['ZLeft'] = np.where(df['votosLeft'] > c, 1, 0)
df['ZLeft'].fillna(0, inplace=True)
df['v_cLft'] = df['votosLeft'] - c
df['Zv_cLft'] = df['ZLeft']*df['v_cLft']

# Gender variables
df['mixedrace'] = np.where(((df['sexo1'] == "M") & (df['sexo2'] == "F")) | ((df['sexo1'] == "F") & (df['sexo2'] == "M")), 1, 0)
df['votos_female'] = (df['votes1']*df['female_candidate1'] + df['votes2']*df['female_candidate2']) / df['Totalvotes'] * 100
                      
df['votos_female'].fillna(0, inplace=True)
df['votos_female2']=df['votos_female']*df['votos_female']
df['Zfemale'] = np.where(df['votos_female'] > c, 1, 0)
#df['Zfemale'] = np.where(df['sexo1'] == "F", 1, 0)


df['v_cfemale'] = df['votos_female'] - c
df['Zv_cfemale'] = df['Zfemale'] * df['v_cfemale']

def RDDplot_computations(dv,race,cutoffvar,runningvar,nbins=20):
    # <50%
    mask=(df[race] == 1) & (df[cutoffvar]==0) & (df[dv].isnull()==False)
    Y = df.loc[mask,dv]
    X = df.loc[mask,[runningvar,runningvar+"2"]]
    X = sm.add_constant(X)
    pred1 = sm.OLS(Y,X).fit(cov_type='HC0').get_prediction()
    df1=pred1.summary_frame(alpha=0.05)
    df1.index = X[runningvar].values
    df1.sort_index(inplace=True)
    # >50%
    mask=(df[race] == 1) & (df[cutoffvar]==1) & (df[dv].isnull()==False)
    Y = df.loc[mask,dv]
    X = df.loc[mask,[runningvar,runningvar+"2"]]
    X = sm.add_constant(X)
    pred2 = sm.OLS(Y,X).fit(cov_type='HC0').get_prediction()
    df2=pred2.summary_frame(alpha=0.05)
    df2.index = X[runningvar].values
    df2.sort_index(inplace=True)
    # Bins
    df['g']=pd.qcut(df.loc[(df[race] == 1) & (df[dv].isnull()==False),runningvar],q=nbins,labels=range(0,nbins))
    dfg=df.loc[(df[race] == 1) & (df[dv].isnull()==False),[dv,runningvar,"g"]].groupby("g",as_index=False).mean()
    # Return
    return df1, df2, dfg

fig,((ax1,ax2),(ax3,ax4))=plt.subplots(2,2,dpi=300,figsize=(12,8))
# Panel A1: First stage
dv,race,cutoffvar,runningvar="left_mayor","ideologyrace",'ZLeft','votosLeft'
df1,df2,dfg=RDDplot_computations(dv,race,cutoffvar,runningvar)
ax1.scatter(dfg.votosLeft,dfg[dv], color='black', s=7,alpha=0.5)
ax1.plot(df1['mean'], color='crimson',linewidth=1)
ax1.fill_between(df1.index, df1.mean_ci_lower, df1.mean_ci_upper, alpha=.1, color='crimson')
ax1.plot(df2['mean'], color='crimson',linewidth=1)
ax1.fill_between(df2.index, df2.mean_ci_lower, df2.mean_ci_upper, alpha=.1, color='crimson')
ax1.set_ylim(0,1.1) # (0,0.25)
ax1.vlines(50,0,1.1, color="black",linestyle=":")
ax1.set_ylabel("Probability of left-wing mayor", size=9)
ax1.set_xlabel("Left vote (%)", size=9)
ax1.spines[['top','right','bottom']].set_visible(False)
ax1.yaxis.set_tick_params(labelsize=9)
ax1.xaxis.set_tick_params(labelsize=9)
ax1.grid(True, linestyle='--')
ax1.set_title("A. Left vote (%) and probability of left-wing mayor\n", size=10)
# Panel B2: Sharp RDD
dv,race,cutoffvar,runningvar="Dfs","ideologyrace",'ZLeft','votosLeft'
df1,df2,dfg=RDDplot_computations(dv,race,cutoffvar,runningvar)
ax2.scatter(dfg.votosLeft,dfg[dv], color='black', s=7,alpha=0.5)
ax2.plot(df1['mean'], color='crimson',linewidth=1)
ax2.fill_between(df1.index, df1.mean_ci_lower, df1.mean_ci_upper, alpha=.1, color='crimson')
ax2.plot(df2['mean'], color='crimson',linewidth=1)
ax2.fill_between(df2.index, df2.mean_ci_lower, df2.mean_ci_upper, alpha=.1, color='crimson')
ax2.set_ylim(0,0.25) # (0,0.25)
ax2.vlines(50,0,0.25, color="black",linestyle=":")
ax2.set_ylabel("Variation in Female share (pps.)", size=9)
ax2.set_xlabel("Left vote (%)", size=9)
ax2.spines[['top','right','bottom']].set_visible(False)
ax2.yaxis.set_tick_params(labelsize=9)
ax2.xaxis.set_tick_params(labelsize=9)
ax2.set_title("B: Left vote (%) and variation in Female share\n", size=10)
ax2.grid(True, linestyle='--')
# Panel B1: Gender: first stage
dv,race,cutoffvar,runningvar="female_mayor","mixedrace",'Zfemale','votos_female'
df1,df2,dfg=RDDplot_computations(dv,race,cutoffvar,runningvar)
ax3.scatter(dfg.votos_female,dfg[dv], color='black', s=7,alpha=0.5)
ax3.plot(df1['mean'], color='crimson',linewidth=1)
ax3.fill_between(df1.index, df1.mean_ci_lower, df1.mean_ci_upper, alpha=.1, color='crimson')
ax3.plot(df2['mean'], color='crimson',linewidth=1)
ax3.fill_between(df2.index, df2.mean_ci_lower, df2.mean_ci_upper, alpha=.1, color='crimson')
ax3.set_ylim(0,1.1) # (0,0.25)
ax3.vlines(50,0,1.1, color="black",linestyle=":")
ax3.set_ylabel("Probability of woman mayor", size=9)
ax3.set_xlabel("Women candidates vote (%)", size=9)
ax3.spines[['top','right','bottom']].set_visible(False)
ax3.yaxis.set_tick_params(labelsize=9)
ax3.xaxis.set_tick_params(labelsize=9)
ax3.grid(True, linestyle='--')
ax3.set_title("C. Women candidates vote (%) and probability of woman mayor\n", size=10)
# Panel B2: Sharp RDD
dv,race,cutoffvar,runningvar="Dfs","mixedrace",'Zfemale','votos_female'
df1,df2,dfg=RDDplot_computations(dv,race,cutoffvar,runningvar)
ax4.scatter(dfg.votos_female,dfg[dv], color='black', s=7,alpha=0.5)
ax4.plot(df1['mean'], color='crimson',linewidth=1)
ax4.fill_between(df1.index, df1.mean_ci_lower, df1.mean_ci_upper, alpha=.1, color='crimson')
ax4.plot(df2['mean'], color='crimson',linewidth=1)
ax4.fill_between(df2.index, df2.mean_ci_lower, df2.mean_ci_upper, alpha=.1, color='crimson')
ax4.set_ylim(0,0.25) # (0,0.25)
ax4.vlines(50,0,0.25, color="black",linestyle=":")
ax4.set_ylabel("Variation in Female share (pps.)", size=9)
ax4.set_xlabel("Women candidates (%)", size=9)
ax4.spines[['top','right','bottom']].set_visible(False)
ax4.yaxis.set_tick_params(labelsize=9)
ax4.xaxis.set_tick_params(labelsize=9)
ax4.set_title("D: Women candidates vote (%) and variation in Female share\n", size=10)
ax4.grid(True, linestyle='--')
# Whole figure
plt.subplots_adjust(hspace=0.5)
fig.text(0.1,0,"Notes: Dots represent local averages (20 equal-size bins). The red lines draw the estimates of the quadratic polynomial of the relationship between the running variables\n\
(either left vote (%) or women candidates vote (%)) and each of the y-axis variables, along with the 95% confidence intervals.", size=9)
fig.text(0.5,1,"Figure 3. RDD analysis: gender, ideology, and variation in the female share", horizontalalignment="center", weight="bold", size=12)
plt.show()


#%% FIGURE SURVEY (FIG 4)

# Read and process data
df=pd.read_stata("C:/Users/danie/Dropbox/Alcaldes/Do files/Replication_files/DATA3.dta")

# % that agree that priority should given to women names
df['f_priority'] = np.where((df['Q234R4'] ==1) | (df['Q234R4'] ==2),1,0)
df.loc[(df['Q234R4'] ==0) | (df['Q234R4'] ==5),'f_priority']=np.nan
print("% that agree...: ", df['f_priority'].mean())

# Low progress made in...
df['f_critic'] = np.where((df['Q163R3']==1),1,0)
df.loc[df.Q163R3.isnull()==True,'f_critic']=np.nan

# Remove observations with null values in ideology
df=df.loc[df.ideology.isnull()==False].copy()

# Other variables
df['ideol']=0
df.loc[(df.ideology<=3),'ideol']=1
df.loc[(df.ideology==4) | (df.ideology==5),'ideol']=2
df.loc[(df.ideology==6),'ideol']=3
df.loc[(df.ideology==7) | (df.ideology==8),'ideol']=4
df.loc[(df.ideology>=9),'ideol']=5

df['man']=np.where(df.woman==1,0,1)
df['i_left'] = np.where((df['ideology'] <= 3),1,0)
df['i_cent'] = np.where((df['ideology'] >= 4) & (df['ideology'] <= 6),1,0)
df['i_right'] = np.where((df['ideology'] >=7),1,0)

def ESTIMATION(depvar):
    df['dv']=df[depvar]    
    result = smf.ols(formula='dv ~ woman:C(ideol) + man:C(ideol) - 1', data=df).fit()
    # Betas
    b_wom= pd.DataFrame(result.params[:5])
    b_wom.reset_index(inplace=True, drop=True)
    b_wom.index=b_wom.index+1
    b_men= pd.DataFrame(result.params[5:])
    b_men.reset_index(inplace=True, drop=True)
    b_men.index=b_men.index+1
    # Conf Int
    ci_wom= pd.DataFrame(result.conf_int()[:5])
    ci_wom.reset_index(inplace=True, drop=True)
    ci_men= pd.DataFrame(result.conf_int()[5:])
    ci_men.reset_index(inplace=True, drop=True)
    return b_wom,b_men,ci_wom,ci_men

fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10,4), dpi=300)
    # Priority should be give to women's names when naming streets
b_wom,b_men,ci_wom,ci_men=ESTIMATION(depvar="f_priority")
ax1.plot(b_wom[0]*100, color='slateblue', label="Women")
ax1.fill_between(b_wom.index, ci_wom[0]*100, ci_wom[1]*100, alpha=.1, color='slateblue')
ax1.plot(b_men[0]*100, color='lightseagreen', label="Men")
ax1.fill_between(b_wom.index, ci_men[0]*100, ci_men[1]*100, alpha=.1, color='lightseagreen')
ax1.spines[['top','right']].set_visible(False)
ax1.xaxis.set_tick_params(labelsize=9)
ax1.set_title("A. Priority should be given to women's names\nwhen naming streets\n", size=10)
ax1.legend(frameon=False, fontsize=8, loc='lower left')
ax1.yaxis.set_tick_params(labelsize=9)
ax1.xaxis.set_tick_params(labelsize=9)
ax1.set_ylim(0,100)
ax1.set_ylabel("% of respondents that agree", size=8)
ax1.annotate('', xy=(0, -0.12), xycoords='axes fraction', xytext=(1, -0.12), 
            arrowprops=dict(arrowstyle="<->"))
ax1.yaxis.set_tick_params(labelsize=8)
ax1.xaxis.set_tick_params(labelsize=8)
ax1.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))                            
ax1.text(1.25,-10,"LEFT", size=7, ha="center")
ax1.text(4.75,-10,"RIGHT", size=7, ha="center")
    # Small progress made in gender equality in housework and care 
b_wom,b_men,ci_wom,ci_men=ESTIMATION(depvar="f_critic")
ax2.plot(b_wom[0]*100, color='slateblue', label="Women")
ax2.fill_between(b_wom.index, ci_wom[0]*100, ci_wom[1]*100, alpha=.1, color='slateblue')
ax2.plot(b_men[0]*100, color='lightseagreen', label="Men")
ax2.fill_between(b_wom.index, ci_men[0]*100, ci_men[1]*100, alpha=.1, color='lightseagreen')
ax2.spines[['top','right']].set_visible(False)
ax2.xaxis.set_tick_params(labelsize=9)
ax2.set_title("B. Small progress made in gender equality\nin housework and care\n", size=10)
ax2.legend(frameon=False, fontsize=8, loc='lower left')
ax2.yaxis.set_tick_params(labelsize=9)
ax2.xaxis.set_tick_params(labelsize=9)
ax2.set_ylim(0,100)
ax2.set_ylabel("% of respondents that agree", size=8)
ax2.annotate('', xy=(0, -0.12), xycoords='axes fraction', xytext=(1, -0.12), 
            arrowprops=dict(arrowstyle="<->"))
ax2.yaxis.set_tick_params(labelsize=8)
ax2.xaxis.set_tick_params(labelsize=8)
ax2.xaxis.set_major_locator(ticker.MaxNLocator(integer=True)) 
ax2.text(1.25,-10,"LEFT", size=7, ha="center")
ax2.text(4.75,-10,"RIGHT", size=7, ha="center")
#
fig.text(0.5,1.1,"Figure 4. Gender role attitudes in the population by gender and ideology"
         , horizontalalignment="center", weight="bold", size=10)

fig.text(0.1,-0.1,
"Notes: The figure shows the percentage of respondents that agree with each statement, depending on their gender and ideology, as well as the 95% confidence interval.\n\
Data come from an online survey of ~2000 Spanish individuals; the effective sample being 1521 observations due to missing values. The original ideological scale (0-10)\n\
is aggregated into a 1-5 one as follows: 1 (0, 1, 2), 2 (3, 4), 3 (5), 4 (6, 7), 5 (8, 9, 10)." ,
         size=7.5)

plt.show()

print(smf.ols(formula='f_priority ~ woman + i_cent + i_left', data=df).fit().summary())
print("-------------------------------------")
print(smf.ols(formula='f_critic ~ woman + i_cent + i_left', data=df).fit().summary())


