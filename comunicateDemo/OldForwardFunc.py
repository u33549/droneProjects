def go_forward(distance, speed):
    """
    Dronu belirtilen mesafeye kadar ileri götürür.
    - distance: Gitmek istediğin mesafe (metre cinsinden)
    - speed: Hedef hız (m/s)
    """
    
    lat1 = vehicle.location.global_relative_frame.lat
    lon1 = vehicle.location.global_relative_frame.lon
    onlineDist = 0
    timeLine = 0
    speedTime = 0
    isSpeedTimeCalced = False
    accWay = 0
    realWay = 0
    timeStamp = 0.001  # Daha hassas ölçüm için 0.1 saniyeye ayarlandı
    oldSpeed = 0
    
    onlineSpeedData = []
    oldSpeedData = []
    realWayData = []
    timeStampData = []
    
    while vehicle.groundspeed>0.3 or not isSpeedTimeCalced:
        # Şu anki konumu ve hızı güncelle
        lat2 = vehicle.location.global_relative_frame.lat
        lon2 = vehicle.location.global_relative_frame.lon
        onlineDist = mathFuncs.lat_lon_to_meters(lat1, lon1, lat2, lon2)
        onlineSpeed = vehicle.groundspeed  # Hava hızı yerine yer hızını kullanıyoruz
        
        # Trapez yöntemiyle geçen mesafeyi (realWay) hesapla
        realWay += (oldSpeed + onlineSpeed) / 2 * timeStamp
        
        time.sleep(timeStamp)
        timeLine += timeStamp
        
        # Hedef hıza ulaşmak için hızlanma süresini hesapla
        if not mathFuncs.lower_error_margin_check(onlineSpeed, speed, 1) and not isSpeedTimeCalced:
            speedTime += timeStamp
            accWay += (oldSpeed + onlineSpeed) / 2 * timeStamp
        elif mathFuncs.lower_error_margin_check(onlineSpeed, speed, 1):
            isSpeedTimeCalced = True
        
        if(mathFuncs.lower_error_margin_check(accWay+realWay , distance, 5)):
            set_drone_velocity(0, 0)
            isSpeedTimeCalced = True
            
        else:
            set_drone_velocity(speed, 0)
            
        
        # Verileri kaydet ve güncelle
        onlineSpeedData.append(onlineSpeed)
        oldSpeedData.append(oldSpeed)
        realWayData.append(realWay)
        timeStampData.append(timeLine)
        # print(f"Geçen Zaman: {timeLine} s, Gerçek Mesafe: {realWay} m,Anlık Hız: {onlineSpeed} m/s, Hızlanma Süresi: {speedTime} s, İvme Yolu: {accWay} m")
        
        oldSpeed = onlineSpeed
    
    print("Vardım Babuşki")
    print("---------------------")
    print(f"Geçen Zaman: {timeLine} s, Gerçek Mesafe: {realWay} m,Anlık Hız: {onlineSpeed} m/s, Hızlanma Süresi: {speedTime} s, İvme Yolu: {accWay} m")
    print("*******************")
    
    # Son konumu ve toplam mesafeyi kontrol et
    lat2 = vehicle.location.global_relative_frame.lat
    lon2 = vehicle.location.global_relative_frame.lon
    print("Gerçek Mesafe (GPS):", mathFuncs.lat_lon_to_meters(lat1, lon1, lat2, lon2), "m")
    print("Mevcut Hava Hızı:", vehicle.groundspeed, "m/s")
    
    # Grafik çizimi
    plt.plot(timeStampData, onlineSpeedData, linestyle='-', color='b', linewidth=1, label="Yer Hızı")
    plt.plot(timeStampData, oldSpeedData, linestyle='-', color='r', linewidth=1, label="Önceki Hız")
    plt.plot(timeStampData, realWayData, linestyle='-', color='g', linewidth=1, label="Alınan Yol")
    
    # Eksen etiketleri ve başlık
    plt.xlabel("Zaman (saniye)")
    plt.ylabel("Hız/Yol (m/s veya m)")
    plt.title("Zaman ile Hız ve Yol Grafiği")
    
    # Gösterge ve ızgara
    plt.legend()
    plt.grid(True)
    
    # Grafiği gösterme
    plt.show()
