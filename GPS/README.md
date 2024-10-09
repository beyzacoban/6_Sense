![image](https://github.com/user-attachments/assets/33956229-f4d7-4932-90f2-50e384da3398)


## Accessibility Score

-Bu skora göre rota kullanıcı tarafından veya algoritma tarafından dinamik olarak değiştirilebilinir.
- Test için normalde Yolo gibi kütüphanelerden yada kullanıcıdan gelicek engel feedbacklerini, kendim rastgele rotaya yerleştirerek test ettim.
- İki farklı api kullandım. OpenStreetMap de simulasyon çalıştı fakat google maps api nda testi gerçekleştiremedim.

Erişilebilirlik puanı, bir yolun görme engelli yayalar için ne kadar uygun olduğunun bir ölçüsüdür. Düşük puan daha iyi erişilebilirliği gösterir. Puan, aşağıdaki OSM etiketlerine göre hesaplanır:

- **Hissedilebilir Kaplama**: Mevcut ise puanı %20 azaltır, navigasyona yardımcı olur.
- **Kaldırım Varlığı**: Kaldırım varsa puanı %30 azaltır.
- **Kontrollü Geçitler**: Trafik sinyalli geçitler için puanı %40 azaltır.
- **Kaldırım Rampaları**: Mevcut ise puanı %20 azaltır, hareket kolaylığını artırır.
- **Yüzey Tipi**: Asfalt veya beton gibi düz yüzeyler için puanı %10 azaltır.
- **Aydınlatma**: İyi aydınlatılmış alanlar için puanı %10 azaltır.

## Kullanılan OSM Özellikleri

1. **Hissedilebilir Kaplama** (`tactile_paving`): Dokulu zemin yüzeylerini belirtir.
2. **Kaldırımlar** (`sidewalk`): Özel yaya yollarını tanımlar.
3. **Yaya Geçitleri** (`highway=crossing`, `crossing=traffic_signals`): Güvenli geçiş noktalarını belirler.
4. **Kaldırım Bilgisi** (`kerb`, `curb_ramp`): Erişilebilir kaldırım tasarımlarını tanımlar.
5. **Yüzey Tipi** (`surface`): Zemin malzemesini tanımlar.
6. **Sokak Aydınlatması** (`lit`): Sokak lambalarının varlığını gösterir.

## Simülasyon İşlevselliği

- **Rota Hesaplama**: İki nokta arasındaki en erişilebilir rotayı belirler.
- **Engel Tespiti**: Gerçek dünya senaryolarını simüle etmek için rastgele engeller oluşturur.
- **Rota Yeniden Hesaplama**: Engellerle karşılaşıldığında rotayı dinamik olarak ayarlar.
- **Erişilebilirlik Bilgisi**: Mevcut konumun erişilebilirlik özellikleri hakkında gerçek zamanlı bilgi sağlar.

## İzlenen Metrikler

1. **Toplam Mesafe**: Kat edilen kümülatif mesafe.
2. **Kaçınılan Engeller**: Başarıyla etrafından dolaşılan engel sayısı.
3. **Ortalama Erişilebilirlik Puanı**: Gidilen rotanın ortalama erişilebilirlik puanı.
4. **Rota Değişiklikleri**: Engellerden dolayı rotanın yeniden hesaplandığı sayı.

## Görselleştirme

Web arayüzü şunları gösterir:

- Mevcut rotayı, yaya konumunu ve engelleri gösteren bir harita.
- Navigasyon durumu ve erişilebilirlik bilgileri hakkında gerçek zamanlı güncellemeler.
- Devam eden simülasyonun temel metrikleri.



Detaylı işleyiş : 

- **Kütüphanelerin İçe Aktarılması**: `random`, `time`, `flask`, `osmnx`, `networkx` gibi gerekli kütüphaneler ve modüller projeye dahil ediliyor.
- **Flask Uygulaması Başlatılıyor**: Flask web framework'ü kullanılarak uygulama başlatılıyor (`app = Flask(__name__)`). CORS (Cross-Origin Resource Sharing) ayarları, farklı kaynaklardan erişime izin vermek için etkinleştiriliyor.
- **Global Değişkenlerin Tanımlanması**: `current_location`, `target_location`, `route`, `graph`, `obstacles`, `total_distance`, `total_obstacles_avoided`, `average_accessibility_score`, `route_changes` gibi çeşitli global değişkenler tanımlanıyor. Bunlar uygulama boyunca kullanılıyor.
- **İstanbul Koordinatları Tanımlanıyor**: `ISTANBUL_CENTER` ile Sultanahmet Meydanı ve Topkapı Sarayı’nın koordinatları global değişkenler olarak kaydediliyor.
- **Grafiğin Başlatılması (initialize_graph)**:
    - Uygulama başlatıldığında haritanın grafiği oluşturuluyor. Sultanahmet Meydanı başlangıç, Topkapı Sarayı hedef olarak ayarlanıyor.
    - `osmnx` kullanarak yürüyüş yolları (`footway`, `path`, vb.) içeren bir grafik 2 km yarıçapında oluşturuluyor.
    - Grafikteki her düğümün erişilebilirliği hesaplanıyor (`get_node_accessibility` fonksiyonu ile) ve kenarlara ekleniyor.
- **Rota Hesaplama (get_route)**:
    - En yakın düğümler bulunarak başlangıç ve bitiş noktaları arasındaki en kısa yol, erişilebilirlik puanlarına göre hesaplanıyor.
    - Bu rota, harita üzerinde gösterilecek şekilde koordinatlara dönüştürülüyor.
- **Engellerin Algılanması (detect_obstacles)**:
    - Rastgele bir şans ile mevcut konuma yakın bir engel oluşturuluyor.
    - Eğer yeni bir engel bulunduysa, engeller listesine ekleniyor.
- **Alternatif Rota Oluşturma (create_alternative_route)**:
    - Engeller grafikten çıkarılıyor ve yeni bir rota hesaplanıyor.
    - Eğer bir yol bulunamazsa, mevcut rota kullanılmaya devam ediliyor.
- **Erişilebilirlik Puanı Hesaplama (get_node_accessibility)**:
    - Her düğümün erişilebilirliği farklı faktörlere (yaya geçidi, kaldırımlar, yüzey türü, aydınlatma, vb.) göre hesaplanıyor.
- **Ana Sayfa Rota Göstergesi (/ route)**:
    - Flask, HTML/CSS/JS kullanarak bir harita arayüzü sunuyor. Harita üzerinde mevcut konum, hedef konum ve engeller gösteriliyor.
    - Rota, engeller ve erişilebilirlik bilgileri web arayüzünde canlı olarak güncelleniyor (`/update` route).
- **Veri Güncellemeleri (/update)**:
    - Flask sunucusundan her saniyede bir, mevcut rota, engeller ve erişilebilirlik bilgileri tarayıcıya güncelleniyor.
    - Uygulama, rota değişikliklerini, toplam mesafeyi ve diğer metrikleri JSON formatında tarayıcıya iletiyor.

detaylı simulasyon : 

- **Başlangıç Durumu ve Global Değişkenler**:
    - Fonksiyon, global olarak tanımlanan `current_location`, `target_location`, `route`, `obstacles`, `total_distance`, `total_obstacles_avoided`, `average_accessibility_score`, `route_changes` gibi değişkenleri kullanıyor.
    - İlk olarak, `current_location` (mevcut konum) ve `target_location` (hedef konum) arasındaki rota hesaplanıyor (`route = get_route(current_location, target_location)`).
    - İlk rotanın kaç noktadan oluştuğu konsola yazdırılıyor.
- **Başlangıç Değerlerinin Ayarlanması**:
    - `step = 0`: Rota üzerindeki adım sayısını takip eder.
    - `total_accessibility = 0`: Toplam erişilebilirlik puanını hesaplar.
    - `move_interval = 5`: Her 5 iterasyonda bir hareket etmeyi sağlar.
    - `iteration = 0`: Simülasyonun kaç iterasyon sürdüğünü izler.
- **While Döngüsü (Simülasyon Süreci)**:
    - Sonsuz bir döngü başlatılır. Bu döngü simülasyonun sürekli çalışmasını sağlar.
- **Her İterasyon (iteration) İçin**:
    - `iteration` her turda 1 artırılır.
    - Eğer iterasyon sayısı `move_interval`'a bölündüğünde kalan 0 ise ve henüz rotanın sonuna gelinmediyse:
        - Mevcut konum bir önceki konum olarak kaydedilir (`prev_location = current_location`).
        - `current_location`, rota üzerindeki yeni adıma (noktaya) güncellenir.
        
        - `step` (adım sayısı) bir artırılır.
- **Mesafe Hesaplama**:
    - Önceki konum ile güncel konum arasındaki büyük daire mesafesi (great-circle distance) hesaplanır ve toplam mesafeye eklenir (`total_distance`).
- **Erişilebilirlik Puanı Hesaplama**:
    - Mevcut konuma en yakın düğüm bulunur (`ox.nearest_nodes` ile) ve bu düğümün erişilebilirlik puanı hesaplanır (`get_node_accessibility` fonksiyonu ile).
    - Toplam erişilebilirlik puanına eklenir ve adımlar boyunca ortalama erişilebilirlik puanı güncellenir (`average_accessibility_score`).
- **Engel Tespiti ve Alternatif Rota Hesaplama**:
    - Eğer mevcut konumda engel tespit edilirse (`detect_obstacles`):
        - Engellerin sayısı ve yeniden rota hesaplanacağı mesajı konsola yazdırılır.
        - Yeni bir alternatif rota hesaplanır (`create_alternative_route`).
        - Eğer yeni rota, önceki rotadan farklıysa rota güncellenir ve adımlar sıfırlanır (`step = 0`).
        - Rota değişiklik sayısı bir artırılır (`route_changes`).
- **Hedefe Ulaşma Durumu**:
    - Eğer `step`, rotanın uzunluğuna ulaştıysa (yani hedefe varıldıysa):
        - "Hedefe ulaşıldı" mesajı konsola yazdırılır.
        - Simülasyon başa döner ve başlangıç konumuna (`current_location`) resetlenir.
        - Engeller temizlenir (`obstacles.clear()`), yeni bir rota hesaplanır ve tüm metrikler sıfırlanır (mesafe, engel sayısı, ortalama erişilebilirlik puanı vb.).
- **Uyku Süresi (time.sleep)**:
    - Döngü her iterasyonda 0.2 saniye bekletilir, böylece güncellemeler yumuşak olur.
- **Durum Güncellemeleri**:
    - Her 5 iterasyonda bir (yani her hareket ettiğinde), adım sayısı, mevcut konum, toplam mesafe ve diğer bilgiler konsola yazdırılır.

Bu süreç, kullanıcının harita üzerinde ilerleyişini ve engellerden kaçınma stratejisini sürekli olarak simüle eder.

