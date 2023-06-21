#Sumo ile ağ oluşturma ve ağı dosyaya kaydetme işlemi , grids (kavşak sayısı) , lanes (kavşakta bulunan şerit sayısı) , length (her şeridin uzunluğu) 
def initialize(grids=5,lanes=3,length=200):
    os.system("netgenerate --grid --grid.number=5 -L="+str(lanes)+" --grid.length="+str(length)+" --output-file=grid.net.xml")

# Oluşturulan ağı ve belirli araç sayısını kullanarak tek trafik simülasyonunu çalıştırma işlemi , path (sumo araçlarının bulunduğu dizin) , vehicles (simülasyondaki araç sayısı)
def single(path,vehicles):
    # araçların trafiğe dahil olduğu flow.xml dosyası oluşturulur
    os.system(path + "randomTrips.py -n grid.net.xml -o flows.xml --begin 0 --end 1 --period 1 --flows "+str(vehicles))
    # rotalar hesaplanır ve hesap sonuçları grid.rou.xml dosyasına kaydedilir
    os.system("jtrrouter --route-files=flows.xml --net-file=grid.net.xml --output-file=grid.rou.xml --begin 0 --end 10000 --accept-all-destinations")
    #simülasyon sırasında sürekli yeniden yönlendirme yapılır ve sonuçlar rerouter.add.xml dosyasına kaydedilir 
    os.system(path + "generateContinuousRerouters.py -n grid.net.xml --end 10000 -o rerouter.add.xml")
    #simülasyon grid.sumocfg dosyası kullanarak başlatılır 
    tree = ET.parse("grid.sumocfg")
    root = tree.getroot()
    for child in root:
        if (child.tag == 'output'):
            for child2 in child:
                child2.attrib['value'] = 'grid.output'+str(vehicles)+'.xml'
    with open('grid.sumocfg', 'wb') as f:
        tree.write(f)
    os.system("sumo -c grid.sumocfg --device.fcd.period 100")


# simülasyon sonuçlarını için analiz işlemi 
def textify(vehicles):
    # sonuçları analiz etmek için grid.outputX.xml dosyası okunur
    tree = ET.parse("grid.output"+str(vehicles)+".xml")
    root = tree.getroot()

    l = 0
    for child in root:
        for child2 in child:
            l += 1

    c = 0
    t = 0
    a = ''
    speeds = np.zeros(l)
    times = np.zeros(l)
    ids = np.zeros(l)
    for child in root:
        for child2 in child:
            # print(child2.tag, child2.attrib)
            if (child2.tag == 'vehicle'):
                a = (child2.attrib)
                speeds[c] = np.float(a['speed'])
                ids[c] = np.float(a['id'])
                times[c] = t
                c = c + 1
        t = t + 1
        # print(t)
    data = np.c_[ids, times, speeds]

    tt = len(np.unique(data[:, 1]))
    vel = np.zeros(tt)
    nc = np.zeros(tt)
    flux = np.zeros(tt)

    for i in range(0, tt):
        w = np.where(data[:, 1] == i)
        vel[i] = np.mean(data[w, 2])
        nc[i] = len(w[0])
        flux[i] = np.sum(data[w, 2])
        velm = np.c_[nc, vel, flux]
    # araçların hızlarını ve kimliklerini içeren bir dizi oluşturulur ve bu verileri kullanarak  ortalama hız , araç sayısı, akış gibi istatistikler hesaplanır ve velmX.txt dosyasına kaydedilir 
    np.savetxt('velm'+str(vehicles)+'.txt',velm)



if __name__ == '__main__':
    import os
    import numpy as np
    import analysis
    from matplotlib import pyplot as plt

    import xml.etree.ElementTree as ET
    path = "C:\\Progra~2\\Eclipse\\Sumo\\tools\\"
    
    #ağ oluşturma fonksiyonu çağrılır
    initialize()

    #oluşturulan dizi, simülasyonun farklı araç sayılarıyla çalıştırılacağı noktaları belirtir , 10 ile 100 arasında 10 adet araç sayısı eklenir ardından 100 ile 2000 arasında 20 adet araç sayısı eklenir 
    vehicles_arr=np.r_[np.linspace(10,100,10).astype(int),np.linspace(100,2000,20).astype(int)]

    #her araç sayısı için single ve textify fonksiyonları çağrılır
    for i in range(0,len(vehicles_arr)):
        #fonksiyonu, simülasyonu belirli bir araç sayısıyla çalıştırılırken 
        single(path,vehicles_arr[i])
        #fonksiyonu simülasyon sonuçlarını analiz eder
        textify(vehicles_arr[i])
    print(np.r_[np.linspace(10,100,10).astype(int),np.linspace(100,2000,20).astype(int)])

    #simülasyon sonuçları gösterilir
    analysis.plots(vehicles_arr)