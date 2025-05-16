import pygame
import sys

pygame.init()

# Ekran ayarları
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alışveriş Sepeti")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont(None, 36)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Sepet listesi
cart = []

# Görselleri yükle (GÖRSEL EKLE la, klasörde bunlar olacak)
elma_img = pygame.image.load("elma.png")
armut_img = pygame.image.load("armut.png")
cikolata_img = pygame.image.load("cikolata.png")
kola_img = pygame.image.load("kola.png")

# Görsel boyutlarını ayarla (80x80 yapak)
elma_img = pygame.transform.scale(elma_img, (80, 80))
armut_img = pygame.transform.scale(armut_img, (80, 80))
cikolata_img = pygame.transform.scale(cikolata_img, (80, 80))
kola_img = pygame.transform.scale(kola_img, (80, 80))

# Ürün konumları
urunler = [
    {"isim": "Elma", "resim": elma_img, "konum": (50, 50)},
    {"isim": "Armut", "resim": armut_img, "konum": (50, 150)},
    {"isim": "Çikolata", "resim": cikolata_img, "konum": (50, 250)},
    {"isim": "Kola", "resim": kola_img, "konum": (50, 350)},
]

# Ana döngü
running = True
while running:
    screen.fill(WHITE)

    # Etkinlik kontrolü
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for urun in urunler:
                x, y = urun["konum"]
                if x <= mx <= x + 80 and y <= my <= y + 80:
                    cart.append(urun["isim"])
                    print(f"{urun['isim']} sepete eklendi!")

    # Ürünleri çiz
    for urun in urunler:
        screen.blit(urun["resim"], urun["konum"])

    # Sepet yazısı
    sepet_yazisi = font.render(f"Sepet: {', '.join(cart)}", True, BLACK)
    screen.blit(sepet_yazisi, (200, 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()

