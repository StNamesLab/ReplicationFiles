

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
****                               REPLICATION OF TABLE 1                                            ****
*********************************************************************************************************


* Install first the command winsor2 if not already installed on your computer.
*ssc install winsor2
use DATA1.dta, clear

* Generate interacion variables
gen wf= woman*left   
gen interact2001= lef_time01*fem_time01 if year == 2001
gen interact2023= lef_time23*fem_time23 if year == 2023

* Winsorize to reduce the impact of outliers
winsor2 lef_time01 fem_time01 lef_time23 fem_time23, c(0 95)  replace 
winsor2 fs, c(0 95) replace // to reduce the influence to high values which may be due to measurement errors

*Logarithmic controls: population and number of streets 
gen l_pop = ln(pop_t)
gen l_st = ln(st)

* Variation in the female share:
sort mun_code year
by mun_code: gen diFs = fs- fs[_n-1]
winsor2 diFs, c(1 99)  replace  // Because of too extreme negative and positive values. If we use c(5 95) => all values = 0.
gen Ifs =(diFs>0) if diFs!=.  //Incremento binario

* Save data for Figure 2
preserve
keep mun_code year left woman fs pop_t
save data_figure2.dta, replace
restore


// TABLE 1. PANEL A:

* Col 1
reg fs lef_time01 fem_time01 l_st l_pop educ j_avage peso_servic if year==2001, robust
* Col 2
reg fs lef_time01 fem_time01 interact2001 l_st l_pop educ j_avage peso_servic if year == 2001, robust
* Col 3
regress fs lef_time23 fem_time23 l_st l_pop educ j_avage peso_servic if year == 2023, robust
* Col 4
regress fs lef_time23 fem_time23 interact2023 l_st l_pop educ j_avage peso_servic if year == 2023, robust


// TABLE 1. PANEL B:
* Col 1
xtreg diFs left woman l_st l_pop i.year , fe robust 
* Col 2
xtreg diFs left woman wf l_st l_pop i.year , fe robust 
* Col 3
xtreg Ifs left woman l_st l_pop i.year , fe robust
* Col 4
xtreg Ifs left woman wf l_st l_pop i.year , fe robust


// TABLE 1. PANEL C:

* Construct political-term panel 
gen term=.
replace term=0 if year<=2003			  // NO DATA
replace term=1 if year>=2004 & year<=2007 // Political term 2003-2007
replace term=2 if year>=2008 & year<=2011 // Political term 2007-2011
replace term=3 if year>=2012 & year<=2015 // Political term 2011-2015
replace term=4 if year>=2016 & year<=2019 // Political term 2015-2019
replace term=5 if year>=2020 & year<=2023 // Political term 2019-2023

sort mun_code term year
by mun_code: gen fs_nexty=fs // Female Share on January 1 in the last year of each political term.
by mun_code term: egen left_term=total(left) // Years of left mayors governing the town 
by mun_code term: egen woman_term=total(woman) // Years of female mayors governing the town

sort mun_code term year
by mun_code term: keep if _n==_N
ta year
tsset mun_code term

// Generate dependent and independent variables for this political term panel
sort mun_code term
by mun_code: gen diFs_term = fs_nexty - fs_nexty[_n-1]  // Variation in the female share
winsor2 diFs_term, c(5 95)  replace  // Because of too extreme negative and positive values. 
gen Ifs_term =(diFs_term>0) if diFs_term!=. // Binary version

by mun_code: gen left_B =(left_term>2) if left_term!=. // 1 if most of the political term governed by a left-wing mayor
by mun_code: gen woman_B =(woman_term>2) if woman_term!=. // 1 if most of the political term governed by a female mayor
gen w_left_B = woman_B*left_B

* Col 1
xtreg diFs_term left_B woman_B l_st l_pop i.term , fe robust
* Col 2
xtreg diFs_term left_B woman_B w_left_B l_st l_pop i.term , fe robust 
* Col 3
xtreg Ifs_term left_B woman_B l_st l_pop i.term , fe robust
* Col 4
xtreg Ifs_term left_B woman_B w_left_B l_st l_pop i.term , fe robust
	