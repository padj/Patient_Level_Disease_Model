# Patient_Level_Disease_Model

Patient level, individual-based model of a fictitious disease, loosely based on: Filipović-Pierucci A, Zarca K, Durand-Zaleski I. Markov Models for Health Economic Evaluations: The R Package heemod. ArXiv170203252 Stat [Internet]; 2017. http://arxiv.org/abs/1702.03252

The model considers an heterogeneous population of individuals (sex, age), with three disease states: asymptomatic, sympomatic, and dead. Transition between states is dictated by probability distributions (a la markov model). The disease is the fictitious "shame" disease.

Individuals are created and added to the population based on the nPop variable. Upon creation, individuals are assigned an age based on a normal distribution (controlled by meanAge and stdAge). Sex is assigned randomly with 50% chance each way. Probability of death from all causes is determined based on ONS life tables (p_death_allCause), probability of catching the disease is p_disease_base, probabilty of being spontaneously cured is p_cured, probability of death with shame is p_death_symp = p_death_disease + p_death_allCause.

The model outputs a graph of the percentage of healthy, symptomatic, and dead within the population against time. 

HOW TO:
1. Download and unzip files.
2. Run shameModel.py.
3. Review results.
4. Modify nPop, meanAge, stdAge, p_disease_base, or p_cured within shameModel.py.
5. Review results, and note impact of changes.

Consideratons:
1. Currently the model can only run until 2018 due to the limit of the ONS life table data. Although the model could be modified to run to 2100 using predicted mortalities from my other project (see mortalityPredictor.py within https://github.com/padj/Age_Structure_Predictor)
2. No treatments are currently implemented. 
