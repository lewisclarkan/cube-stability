import numpy as np
import pandas as pd
import plotly.express as px

def pos_abs(a):
  if a<0: return 0
  else:   return a

def fkh(lamb,mu,nu,h,k):
  coefficient = 1/(lamb*mu*nu*np.math.factorial(k+2))
  sum = pos_abs((h))**(k+2) - pos_abs((h-lamb))**(k+2) - pos_abs((h-mu))**(k+2) - pos_abs((h-nu))**(k+2) + pos_abs((h-mu-lamb))**(k+2) + pos_abs((h-mu-nu))**(k+2) + pos_abs((h-nu-lamb))**(k+2) - pos_abs((h-lamb-nu-mu))**(k+2)
  e = sum * coefficient
  return e

def potential_energy(lamb,mu,nu,h,density):
  centre_of_mass = (lamb+mu+nu)/(2)
  f2h = fkh(lamb,mu,nu,h,2)
  centre_of_buoy = f2h/density
  potential_energy = centre_of_mass + centre_of_buoy - h

  return potential_energy

def solve_for_h(density, lamb, mu, nu):
  constant = 6 * density * lamb * mu * nu
  h_trials = np.arange(0,1,0.001)
  sums = np.empty(0)

  for h in h_trials:
    sum1=0
    if h>0:
      sum1 = sum1 + h**3
    if (h-lamb)>0:
      sum1 = sum1 - (h-lamb)**3
    if (h-mu)>0:
      sum1 = sum1 - (h-mu)**3
    if (h-nu)>0:
      sum1 = sum1 - (h-nu)**3
    if (h-lamb-nu)>0:
      sum1 = sum1 + (h-lamb-nu)**3
    if (h-lamb-mu)>0:
      sum1 = sum1 + (h-lamb-mu)**3
    if (h-mu-nu)>0:
      sum1 = sum1 + (h-mu-nu)**3
    if (h-lamb-mu-nu)>0:
      sum1 = sum1 - (h-lamb-mu-nu)**3
    sums = np.append(sums,sum1)

  difference = np.subtract(constant,sums)
  difference = np.abs(difference)
  solution_index = np.where(difference==np.min(difference))
  p = h_trials[solution_index]
  return p.item()

densities_to_calc = np.arange(0.200,0.203,0.001)

for density in densities_to_calc:

  density_name = str(int(np.round(density*1000,0)))
  print(density_name)

  Lambda = np.arange(0.0001,0.9999,0.05)
  Mu     = np.arange(0.0001,0.9999,0.05)
  Nu     = np.arange(0.0001,0.9999,0.05)

  df = pd.DataFrame(columns = ['density','h_value', 'lambda_value', 'mu_value', 'nu_value', 'potential_energy'])

  for L in Lambda:
    for M in Mu:
      squared_sum = L**2 + M**2
      if squared_sum < 0.9999:
        N = np.sqrt(1-squared_sum)
        h = solve_for_h(density, L, M, N)
        potential = potential_energy(L,M,N,h,density)
        new_row = pd.Series({'density': density, 'h_value': h, 'lambda_value' : L , 'mu_value': M , 'nu_value': N, 'potential_energy': potential })
        df = pd.concat([df,new_row.to_frame().T],ignore_index=True)

  df.to_csv('data/{}.zip'.format(density_name), index=False)
