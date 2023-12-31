#trafik simülasyonu sonuçları üzerinde grafik oluşturma işlemi 
import numpy as np
from matplotlib import pyplot as plt
def plots(vehicles):
    vel=np.zeros(len(vehicles))
    nc=np.zeros(len(vehicles))
    flux=np.zeros(len(vehicles))
    for i in range(0,len(vehicles)):
        txt=np.loadtxt('velm'+str(vehicles[i])+'.txt')
        nc[i] = np.mean(txt[95:100, 0])
        vel[i] = np.mean(txt[95:100, 1])
        flux[i]=np.mean(txt[95:100,2])
        print(nc[i],vel[i],flux[i])
    fig=plt.figure()
    plt.plot(nc/3000,vel,'o')
    plt.plot(nc / 3000, vel, color='k')
    plt.xlabel('Density')
    plt.ylabel('Velocity')
    plt.tight_layout()
    plt.savefig('vel-density.png',dpi=600)
    plt.show()

    fig=plt.figure()
    plt.plot(nc / 3000,flux,'o',label='Traffic Simulation')
    plt.plot(nc / 3000, flux, color='k')
    plt.plot(vehicles/3000,vehicles*vel[0],'r--',label='No Interaction')
    plt.ylim(0,2800)
    plt.legend()
    plt.xlabel('Density')
    plt.ylabel('Flux')
    plt.tight_layout()
    plt.savefig('flux-density.png', dpi=600)