
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
****                               REPLICATION OF TABLE 2                                            ****
*********************************************************************************************************

use DATA2.dta, clear

global c = 50


* Ideological electoral race:

preserve
	// Keep only ideological races
keep if (left_1==1 & right_2==1) | (left_2==1 & right_1==1)
	// Variables for sharp model
gen votosLeft = (votes1*left_1+votes2*left_2+votes3*left_3)/Totalvotes*100
gen ZLeft=(votosLeft>$c)
gen v_cLft = votosLeft - $c
gen Zv_cLft= ZLeft*v_cLft
	// REGRESSIONS
* Panel A. Col1 
reg Dfs v_cLft ZLeft Zv_cLft Lpopulation Lst i.term , cluster(mun_code)
* Panel A. Col2 
reg Ifs v_cLft ZLeft Zv_cLft Lpopulation Lst i.term, cluster(mun_code)
* Panel B. Col1 
reg left_mayor v_cLft Zv_cLft ZLeft Lpopulation Lst i.term, cluster(mun_code)
predict a_Left_hat, xb
gen a_Left_v_c = v_cLft*a_Left_hat
reg Dfs v_cLft a_Left_hat a_Left_v_c Lpopulation Lst i.term , cluster(mun_code)
* Panel B. Col2
reg Ifs v_cLft a_Left_hat a_Left_v_c Lpopulation Lst i.term , cluster(mun_code)
restore


* Gender-mixed electoral race:

preserve
	// Keep only gender-mixed races
keep if (sexo1=="M" & sexo2=="F") | (sexo1=="F" & sexo2=="M")
	// Variables for sharp model
gen votos_female = (votes1*female_candidate1+votes2*female_candidate2)/(votes1+votes2)*100
replace votos_female= 0 if votos_female==.
gen Zfemale=(votos_female>$c)
*gen Zfemale=(sexo1=="F")
gen v_cfemale = votos_female  - $c
gen Zv_cfemale= Zfemale*v_cfemale
	// REGRESSIONS
* Panel A. Col3 
reg Dfs v_cfemale Zfemale Zv_cfemale Lpopulation Lst i.term , cluster(mun_code)
* Panel A. Col4
reg Ifs v_cfemale Zfemale Zv_cfemale Lpopulation Lst i.term , cluster(mun_code)
* Panel B. Col3
reg female_mayor v_cfemale Zv_cfemale Zfemale Lpopulation Lst i.term, cluster(mun_code)
predict a_female_hat, xb
gen a_female_v_c = v_cfemale*a_female_hat	
reg Dfs v_cfemale a_female_hat a_female_v_c Lpopulation Lst i.term, cluster(mun_code)
* Panel B. Col4
reg Ifs v_cfemale a_female_hat a_female_v_c Lpopulation Lst i.term, cluster(mun_code)

restore

