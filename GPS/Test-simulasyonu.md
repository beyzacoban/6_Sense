# Test Süreci Açıklaması (Kullanılan Teknolojiler ve Kütüphaneler):
# 1. Program başlatılır ve Flask web uygulaması ayrı bir thread'de çalıştırılır.
#    - Flask: Web uygulaması için kullanılan micro web framework
#    - threading: Çoklu iş parçacığı yönetimi için kullanılan Python modülü
# 2. Başlangıç ve hedef konumları belirlenir (New York City merkezi ve Empire State Binası).
#    - Koordinatlar: Enlem ve boylam değerleri kullanılır
# 3. Şehir haritası için bir graf oluşturulur.
#    - OSMnx: OpenStreetMap verilerinden graf oluşturmak için kullanılan kütüphane
# 4. İlk rota hesaplanır.
#    - NetworkX: Graf üzerinde en kısa yol algoritmaları için kullanılan kütüphane
# 5. Simülasyon döngüsü başlar:
#    a. Mevcut konum güncellenir (rota üzerinde ilerleme).
#    b. Her adımda, engel tespit etme olasılığı kontrol edilir.
#       - Random: Rastgele engel oluşturmak için kullanılan Python modülü
#    c. Engel tespit edilirse, yeni bir rota hesaplanır.
#    d. Yeni rota, mevcut engelleri göz önünde bulundurarak oluşturulur.
#       - NetworkX: Alternatif rota hesaplamak için tekrar kullanılır
# 6. Bu süreç, hedef konuma ulaşılana kadar devam eder.
#    - time: Simülasyon adımları arasında bekleme süresi için kullanılan Python modülü
# Not: Gerçek zamanlı GPS verisi ve gerçek engel tespiti yerine simülasyon kullanılmaktadır.
