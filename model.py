# SIR Model

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('darkgrid')

class SIR:
    def __init__(self, eons=1000, Susceptible=950, Infected=50, Resistant=0, rateSI=0.05, rateIR=0.01, rateBirth=0.0, rateDeath=0.0):
        self.eons = eons
        self.Susceptible = Susceptible
        self.Infected = Infected
        self.Resistant = Resistant
        self.rateSI = rateSI
        self.rateIR = rateIR
        self.rateBirth = rateBirth
        self.rateDeath = rateDeath
        self.numIndividuals = Susceptible + Infected + Resistant
        self.results = None
        self.modelRun = False

    def run(self):
        Susceptible = [self.Susceptible]
        Infected = [self.Infected]
        Resistant = [self.Resistant]

        for step in range(1, self.eons):
            S_to_I = (self.rateSI * Susceptible[-1] * Infected[-1]) / self.numIndividuals
            I_to_R = Infected[-1] * self.rateIR
            mu_N = self.rateBirth * self.numIndividuals
            nu_S = self.rateDeath * Susceptible[-1]
            nu_I = self.rateDeath * Infected[-1]
            nu_R = self.rateDeath * Resistant[-1]
            Susceptible.append(Susceptible[-1] + mu_N - S_to_I - nu_S)
            Infected.append(Infected[-1] + S_to_I - I_to_R - nu_I)
            Resistant.append(Resistant[-1] + I_to_R - nu_R)
            self.numIndividuals = Susceptible[-1] + Infected[-1] + Resistant[-1]

        self.results = pd.DataFrame.from_dict({'Time':list(range(len(Susceptible))),
            'Susceptible':Susceptible, 'Infected':Infected, 'Resistant':Resistant},
            orient='index').transpose()
        self.modelRun = True
        self.results.to_csv('result.csv')


    def plot(self, filename1, filename2):
        if self.modelRun == False:
            print('Error: Model has not run. Please call SIR.run()')
            return
        plt.figure(figsize=(16, 9))
        plt.plot(self.results['Time'], self.results['Susceptible'], color='blue')
        plt.plot(self.results['Time'], self.results['Infected'], color='red')
        plt.plot(self.results['Time'], self.results['Resistant'], color='green')
        plt.xlabel('Time')
        plt.ylabel('Population')
        plt.legend(['Susceptible','Infected','Resistant'], prop={'size': 10}, loc='upper center', bbox_to_anchor=(0.5, 1.02), ncol=3, fancybox=True, shadow=True)
        plt.title(r'$\beta = {0}, \gamma = {1}, \mu = {2}, \nu = {3}$'.format(self.rateSI, self.rateIR, self.rateBirth, self.rateDeath))
        plt.savefig(filename1)
        plt.close()

        plt.figure(figsize=(16, 9))
        plt.plot(self.results['Infected'], self.results['Resistant'], color='blue')
        plt.xlabel('Suspectible')
        plt.ylabel('Infected')
        plt.savefig(filename2)
        plt.close()


if __name__ == '__main__':
    iters = 1000
    Susceptible = 10000
    Infected = 100
    Resistant = 5
    beta = 0.05
    gamma = 0.01
    mu = 0.00001
    nu = 0.007


    sir = SIR(iters, Susceptible, Infected, Resistant, beta, gamma, mu, nu)

    sir.run()
    sir.plot('example_1.png', 'conflict_1.png')