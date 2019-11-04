import scipy.optimize as opt
import numpy as np
import pylab as plt
import sys
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


########################################
# parametry poczatkowe (u0,t0,tE,mbase,fs)

initialParameters = np.array([0.1, 3560.0, 30.0, 14.0, 1.0])


########################################
# pobierz nazwe pliku

input=(str(sys.argv[1]))
name=input.split(".")


########################################
# definicja modelu mikrosoczewki
# model ma 5 parametrow (u0,t0,tE,mbase,fs)
#

def model(t, u0, t0, tE, mbase, fs):
    u = np.sqrt(u0**2+((t-t0)/tE)**2)
    A = (u**2+2)/u/np.sqrt(u**2+4)
    mag = mbase - 2.5*np.log10(fs*(A-1)+1)
    return mag.ravel()


########################################
# czytanie danych z nieznanymi typami danych -- 3 kolumny

def read_file(filename):  

  f = open(filename, 'r')
  xdata, ydata, edata = [], [], []
  for line in f:
    if len(line) <= 0: continue
    l = line.strip()
    if len(l) <= 0: continue
    if l[0] == '#': continue
    row = l.split()
    xdata_str, ydata_str, edata_str = row[0], row[1], row[2]
    xdata.append(float(xdata_str))
    ydata.append(float(ydata_str))
    edata.append(float(edata_str))
  f.close()
  return np.array(xdata), np.array(ydata), np.array(edata)


########################################
# wczytanie krzywej zmien blasku

t, m, e = read_file(input)
e = np.sqrt(e**2 + 0.02**2)


########################################
# ograniczenia na parametery
lowerBounds = (0.0, 1000.0,   0.1, 12.0, 0.01)
upperBounds = (3.0, 6000.0, 200.0, 21.0, 1.0)
parameterBounds = [lowerBounds, upperBounds]


########################################
# dopasowanie
popt, pcov = curve_fit(model, t, m, p0=initialParameters, sigma=e, bounds = parameterBounds)


########################################
# dopasowane wartosci parametrow
u0, t0, tE, mbase, fs = popt

# bledy parametrow
eu0 = pcov[0,0]**0.5
et0 = pcov[1,1]**0.5
etE = pcov[2,2]**0.5
embase = pcov[3,3]**0.5
efs = pcov[4,4]**0.5

########################################
# jasnosc zrodla

m0 = -2.5*np.log10(fs*10**(-0.4*mbase))
em0 = -2.5*np.log10((fs-efs)*10**(-0.4*(mbase+embase))) - m0


########################################
# wypisz parametery i bledy

print "PARAMETRY MIKROSOCZEWKI:"
print("u0 = %10.4f %10.4f"% (u0, eu0))
print("t0 = %10.4f %10.4f"% (t0, et0))
print("tE = %10.4f %10.4f"% (tE, etE))
print("mb = %10.4f %10.4f"% (mbase, embase))
print("m0 = %10.4f %10.4f"% (m0, em0))
print("fs = %10.4f %10.4f"% (fs, efs))

########################################
# CHI^2

chi2 = np.sum(((m-model(t, *popt))/e)**2)
print("Dobroc dopasowania chi^2/dof = %10.3f"% (chi2/(t.shape[0]-popt.shape[0])) )


########################################
# RYSOWANIE

# zakres obrazka
tleft  = t0 - 5.0*tE
tright = t0 + 5.0*tE
plt.axis([tleft, tright, max(m)+0.3, min(m)-0.1])

# osie i nazwa
plt.title(name[0])
plt.xlabel('HJD-2450000 (days)')
plt.ylabel('I (mag)')

# wyrysuj dane z bledami
plt.errorbar(t, m, yerr=e, fmt='o', ms=3, zorder=1)

# generowanie modelu dla obrazka
x_plot = np.linspace(tleft, tright, 1000)
y_plot = model(x_plot, u0, t0, tE, mbase, fs)

# rysowanie modelu
plt.plot(x_plot, y_plot, zorder=2) 

# zapisywanie obrazka
plt.savefig(name[0]+'.png')

# zapisywanie do pliku
f=open(name[0]+'.txt',"w+")
f.write("plik: %s\n"% input)
f.write("u0 = %10.4f %10.4f\n"% (u0, eu0))
f.write("t0 = %10.4f %10.4f\n"% (t0, et0))
f.write("tE = %10.4f %10.4f\n"% (tE, etE))
f.write("mb = %10.4f %10.4f\n"% (mbase, embase))
f.write("m0 = %10.4f %10.4f\n"% (m0, em0))
f.write("fs = %10.4f %10.4f\n"% (fs, efs))
f.write("chi^2/dof = %10.3f\n"% (chi2/(t.shape[0]-popt.shape[0])) )
f.close() 

