# 6_Sense
Kişisel Asistan

Bu projemizde görme engelliler için bir kişisel asistan yapacağız. Bu asistanın temel özelliği kullanıcıyı istenilen konuma güvenli bir şekilde ulaştırması olacak. Bunu şu şekilde saglayacak.
Kendi iceriginde bulunan GPS sayesinde konum bilgisine hakim olacak ve bulundurduğu map sayesinde kullanıcı icin uygun bir rota oluşturacak. Bu rotada ilerleme sağlaması icin cihazımızın ön tarafında bulunan kamera sayesinde cevreyi tarayıp analiz edecek cevredeki isimleri bilecek ve kullanıcı için zararsız bir ilerleme saglamasını sağlayacak bunu bulundurduğu kulaklık sayesinde kullanıcıya sesli komut verecek aynı zamanda kullanıcıdan da sesli komut alabilecek.
Bu projede önemli faktör kamera sayesinde yönlendirdiği yolu analiz eden yapımız yolda karşısına çıkan sorunları kullanıcıya bildirecek ve bunlar icin alternatif yollar sunacak.

Kullanacağımız yazılım dili: PYTHON

Gerekli yapı bilgisi:

GPS Modülü: Konum tespiti için bir GPS modülüne ihtiyacınız olacak. Bu, kullanıcının bulunduğu konumu belirlemenize ve hedef konumu belirlemenize yardımcı olur.
Harita Verileri: GPS kullanarak, cihazınıza yüklü olan harita verilerine erişim sağlamanız gerekir. Bu, kullanıcının bulunduğu konum ve hedef arasında uygun bir rota belirlemenize yardımcı olur.
Kamera: Cihazınızın önünde bulunan bir kamera, çevreyi tarayarak görüntüleri analiz edebilir. Nesneleri, engelleri ve diğer önemli özellikleri algılamak için kullanılabilir.
Görüntü İşleme ve Analiz Yazılımı: Kamera görüntülerini işleyecek ve çevredeki nesneleri tanıyacak bir yazılıma ihtiyacınız olacak. Bu, yolları, engelleri ve diğer önemli özellikleri algılamak için gereklidir.
Sesli Komut ve Tanıma Sistemi: Kullanıcıdan gelen sesli komutları algılayacak ve anlayacak bir sistem geliştirmeniz gerekecek. Aynı şekilde, cihazın kullanıcıya sesli geri bildirim sağlaması için bir sistem de kurmanız gerekir.
Engel Tespit ve Alternatif Rota Oluşturma Algoritması: Cihazınızın çevredeki engelleri tespit etmesini ve kullanıcıya bildirmesini sağlayacak bir algoritma geliştirmeniz gerekir. Ayrıca, engellerle karşılaşıldığında alternatif rotalar önermek için bir algoritma da gerekebilir.
Bağlantı ve Güç Kaynağı: Cihazın internete bağlanabilmesi için bir bağlantı seçeneği (Wi-Fi, mobil ağ vb.) ve güç kaynağına (pil, şarj adaptörü vb.) ihtiyacınız olacak.
Kulaklık veya Hoparlör: Kullanıcıya sesli geri bildirim sağlamak için bir kulaklık veya hoparlör eklemeniz gerekecek.
Dokunmatik veya Düğme Kontrolleri: Kullanıcının cihazı kullanmasını sağlayacak dokunmatik ekran veya düğme kontrolleri eklemek önemlidir.


Python dilinde kullanabileceğiniz yapıları ve cihazları ekleyelim:
GPS Modülü ve Harita Verileri:
GPS Modülü (Örneğin NEO-6M): GPS modülü, seri iletişim aracılığıyla GPS verilerini sağlar. Python'da bu verilere erişmek için serial kütüphanesini kullanabilirsiniz.
Harita Verileri: Harita verilerine erişmek için, Python'da harita hizmetlerine API'ler aracılığıyla erişebilirsiniz. Örneğin, Google Haritalar API veya OpenStreetMap gibi hizmetleri kullanabilirsiniz.
Kamera ve Görüntü İşleme:
Kamera (Örneğin Raspberry Pi Kamera): Python'da Raspberry Pi kamerası gibi USB veya CSI kameralarını kontrol etmek için picamera kütüphanesini kullanabilirsiniz.
Görüntü İşleme ve Analiz Yazılımı: Görüntü işleme için Python'da birçok kütüphane bulunmaktadır. Örneğin, OpenCV veya TensorFlow gibi kütüphaneler, nesne tespiti, yol algılama ve diğer görüntü işleme görevleri için kullanılabilir.
Sesli Komut ve Tanıma Sistemi:
Mikrofon ve Hoparlör: Python'da ses girişi ve çıkışı için pyaudio veya sounddevice gibi kütüphaneleri kullanabilirsiniz.
Sesli Komut ve Tanıma Sistemi: Sesli komutları algılamak için Python'da hazır kütüphaneler bulunmaktadır. Örneğin, SpeechRecognition kütüphanesi, kullanıcıdan gelen sesli komutları tanımak için kullanılabilir.
Engel Tespit ve Alternatif Rota Oluşturma Algoritması:
Görüntü İşleme ve Analiz Yazılımı: Yukarıda bahsedildiği gibi, görüntü işleme kütüphaneleri engelleri tespit etmek için kullanılabilir.
Alternatif Rota Algoritması: Engellerle karşılaşıldığında alternatif rotaları hesaplamak için Python'da birçok yol bulunmaktadır. Örneğin, A* veya Dijkstra gibi yol bulma algoritmalarını uygulayabilirsiniz.
Bağlantı ve Güç Kaynağı:
Wi-Fi veya Mobil Ağ Bağlantısı: Python'da internete bağlanmak için requests veya urllib gibi kütüphaneleri kullanabilirsiniz.
Güç Kaynağı: Python, donanımın güç yönetimi ile ilgili işlevleri gerçekleştirmek için Raspberry Pi GPIO pinlerini kontrol etmek için RPi.GPIO kütüphanesini kullanabilirsiniz.
Kulaklık veya Hoparlör:
Ses Çıkışı: Sesli geri bildirim için Python'da pygame veya pyaudio gibi kütüphaneleri kullanabilirsiniz.

Detaylı Kütüphane ve Modül Bilgileri
GPS Modülü ve Harita Verileri:
serial: Seri iletişim için kullanılır.
requests veya urllib: Harita hizmetlerine API'ler aracılığıyla erişmek için kullanılabilir.
Kamera ve Görüntü İşleme:
picamera: Raspberry Pi kamera modülünü kontrol etmek için kullanılır.
OpenCV: Görüntü işleme ve analiz için popüler bir kütüphanedir.
TensorFlow: Derin öğrenme ve nesne tanıma için kullanılabilir.
Sesli Komut ve Tanıma Sistemi:
pyaudio veya sounddevice: Ses girişi ve çıkışı için kullanılabilir.
SpeechRecognition: Kullanıcıdan gelen sesli komutları tanımak için kullanılabilir.
Engel Tespit ve Alternatif Rota Oluşturma Algoritması:
Görüntü İşleme ve Analiz Yazılımı için:
OpenCV: Nesne tespiti ve görüntü analizi için.
Alternatif Rota Algoritması için:
Özel bir yol bulma algoritması uygulanabilir (örneğin, A* veya Dijkstra).
networkx: Graf ve ağ analizi için kullanılabilir.
Bağlantı ve Güç Kaynağı:
requests veya urllib: İnternete bağlanmak için kullanılabilir.
RPi.GPIO: Raspberry Pi'nin GPIO pinlerini kontrol etmek için kullanılabilir.
Kulaklık veya Hoparlör:
pygame: Ses çıkışı için kullanılabilir.

Ek Donanım İhtiyaçları
Kamera Modülü: Raspberry Pi Camera Module V2.
GPS Modülü: U-blox NEO-6M GPS Modülü.
Mikrofon ve Kulaklık: USB veya 3.5mm jaklı mikrofon ve kulaklık.
Güç Kaynağı: Raspberry Pi için uygun güç kaynağı (5V 3A adaptör).
MicroSD Kart: En az 32GB kapasiteli hızlı bir microSD kart (Raspberry Pi OS ve yazılımlar için).
Koruyucu Kutu: Raspberry Pi ve bağlantı elemanlarını korumak için bir kutu.
