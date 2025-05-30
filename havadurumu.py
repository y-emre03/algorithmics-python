"""
Görsel Hava Durumu Uygulaması
Bu uygulama, kullanıcının girdiği şehrin hava durumu görselini gösterir.
wttr.in API'sini kullanarak ASCII sanat formatında hava durumu görselleri alır.
Yanlış şehir adı girilirse hata mesajı gösterir.
"""

import pygame
import requests
import sys
from io import BytesIO
from PIL import Image

# Pygame başlatma
pygame.init()

# Pencere ayarları
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Görsel Hava Durumu")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 100, 255)
RED = (255, 0, 0)

# Fontlar
input_font = pygame.font.SysFont("Arial", 32)
button_font = pygame.font.SysFont("Arial", 24)
error_font = pygame.font.SysFont("Arial", 28, bold=True)

def get_weather_image(city):
    """Verilen şehir için hava durumu görselini alır"""
    try:
        url = f"https://wttr.in/{city}_0qnp_lang=tr.png"
        response = requests.get(url, headers={'User-Agent': 'curl/7.64.1'}, timeout=10)
        
        # 404 hatasını kontrol et (geçersiz şehir)
        if response.status_code == 404:
            return None
            
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return pygame.image.fromstring(img.tobytes(), img.size, img.mode)
    except Exception as e:
        print(f"Görsel alınırken hata: {e}")
        return None

def draw_input_screen():
    """Kullanıcı giriş ekranını çizer"""
    screen.fill(WHITE)
    
    # Giriş kutusu
    pygame.draw.rect(screen, GRAY, (WIDTH//2 - 200, HEIGHT//2 - 25, 400, 50), border_radius=5)
    pygame.draw.rect(screen, BLACK, (WIDTH//2 - 200, HEIGHT//2 - 25, 400, 50), 2, border_radius=5)
    
    # Giriş metni
    if user_input:
        input_text = input_font.render(user_input, True, BLACK)
        screen.blit(input_text, (WIDTH//2 - 190, HEIGHT//2 - 15))
    else:
        prompt = input_font.render("Şehir adı yazın...", True, (100, 100, 100))
        screen.blit(prompt, (WIDTH//2 - 190, HEIGHT//2 - 15))
    
    pygame.display.flip()

def draw_weather_screen():
    """Hava durumu görselini ve yeni sorgu butonunu gösterir"""
    if weather_img:
        # Görseli ölçeklendir
        img_width, img_height = weather_img.get_size()
        scale = min(WIDTH/img_width, (HEIGHT-100)/img_height)
        scaled_img = pygame.transform.scale(
            weather_img, 
            (int(img_width*scale), int(img_height*scale))
        )
        screen.blit(scaled_img, (0, 0))
        
        # Yeni sorgu butonu
        pygame.draw.rect(screen, BLUE, (WIDTH//2 - 100, HEIGHT-70, 200, 40), border_radius=5)
        button_text = button_font.render("YENİ SORGULA", True, WHITE)
        screen.blit(button_text, (WIDTH//2 - button_text.get_width()//2, HEIGHT-60))
    else:
        # Hata mesajı göster
        screen.fill(WHITE)
        error_text = error_font.render("BAĞLANTI HATASI!", True, RED)
        screen.blit(error_text, (WIDTH//2 - error_text.get_width()//2, HEIGHT//2 - 50))
        
        # Yeni sorgu butonu (hata durumunda da göster)
        pygame.draw.rect(screen, BLUE, (WIDTH//2 - 100, HEIGHT//2 + 20, 200, 40), border_radius=5)
        button_text = button_font.render("TEKRAR DENE", True, WHITE)
        screen.blit(button_text, (WIDTH//2 - button_text.get_width()//2, HEIGHT//2 + 30))
    
    pygame.display.flip()

# Ana program değişkenleri
user_input = ""
current_screen = "input"
weather_img = None
error_message = ""

# Ana uygulama döngüsü
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if current_screen == "input":
                if event.key == pygame.K_RETURN:
                    if user_input:
                        weather_img = get_weather_image(user_input)
                        current_screen = "weather"
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
        
        elif event.type == pygame.MOUSEBUTTONDOWN and current_screen == "weather":
            mouse_pos = pygame.mouse.get_pos()
            # Yeni sorgu butonuna tıklama kontrolü
            if ((WIDTH//2 - 100 <= mouse_pos[0] <= WIDTH//2 + 100 and 
                 ((HEIGHT-70 <= mouse_pos[1] <= HEIGHT-30) or 
                  (not weather_img and HEIGHT//2 + 20 <= mouse_pos[1] <= HEIGHT//2 + 60)))):
                current_screen = "input"
                user_input = ""
                weather_img = None
    
    # Ekranı çiz
    if current_screen == "input":
        draw_input_screen()
    elif current_screen == "weather":
        draw_weather_screen()

pygame.quit()
sys.exit()