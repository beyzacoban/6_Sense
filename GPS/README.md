## Erişilebilirlik Puanı

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

![image](https://github.com/user-attachments/assets/33956229-f4d7-4932-90f2-50e384da3398)


