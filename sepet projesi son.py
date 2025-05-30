import pygame
import sys
import os

# Pygame başlatma
pygame.init()

# Ekran ayarları
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alışveriş Sepeti Uygulaması")

# Renk paleti
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 150, 50)
RED = (200, 50, 50)
BLUE = (50, 100, 200)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (100, 100, 100)
YELLOW = (255, 215, 0)

# Fontlar
title_font = pygame.font.SysFont("Arial", 48, bold=True)
font = pygame.font.SysFont("Arial", 32)
small_font = pygame.font.SysFont("Arial", 24)
price_font = pygame.font.SysFont("Arial", 28, bold=True)

# FPS ayarı
clock = pygame.time.Clock()
FPS = 60

# Veri yapıları
class Product:
    def __init__(self, name, image, price, stock):
        self.name = name
        self.image = image
        self.price = price
        self.stock = stock

class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

# Ürün görsellerini yükleme
def load_image(name, size=(100, 100)):
    try:
        img = pygame.image.load(f"images/{name}.png")
        return pygame.transform.scale(img, size)
    except:
        # Varsayılan görsel oluştur
        default_img = pygame.Surface(size)
        default_img.fill(LIGHT_GRAY)
        pygame.draw.rect(default_img, DARK_GRAY, (0, 0, *size), 2)
        text = small_font.render(name[:5], True, BLACK)
        default_img.blit(text, (size[0]//2 - text.get_width()//2, size[1]//2 - text.get_height()//2))
        return default_img

# Ürün veritabanı
products = [
    Product("Elma", load_image("elma"), 3.50, 10),
    Product("Armut", load_image("armut"), 4.75, 8),
    Product("Muz", load_image("muz"), 6.25, 15),
    Product("Çilek", load_image("cilek"), 8.90, 5),
    Product("Çikolata", load_image("cikolata"), 5.50, 20),
    Product("Kola", load_image("kola"), 3.20, 30),
    Product("Su", load_image("su"), 1.25, 50),
    Product("Ekmek", load_image("ekmek"), 2.50, 15),
    Product("Peynir", load_image("peynir"), 12.90, 10),
    Product("Zeytin", load_image("zeytin"), 9.75, 8),
    Product("Yumurta", load_image("yumurta"), 15.00, 5),
    Product("Domates", load_image("domates"), 4.25, 12)
]

# Alışveriş sepeti
cart = []

# Kaydırma özellikleri
scroll = {
    "y": 0,
    "speed": 20,
    "max": 0,
    "dragging": False,
    "start_y": 0
}

# Mesaj sistemi
message = {
    "text": "",
    "show": False,
    "time": 0,
    "duration": 2000
}

# Ekran durumu
current_screen = "main"  # "main" veya "cart"

# Buton çizme fonksiyonu
def draw_button(x, y, width, height, text, color=GREEN, text_color=WHITE, border_radius=10):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect, border_radius=border_radius)
    pygame.draw.rect(screen, BLACK, button_rect, 2, border_radius=border_radius)
    
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    
    return button_rect

# Mesaj gösterme fonksiyonu
def show_message(text, duration=2000):
    message["text"] = text
    message["show"] = True
    message["time"] = pygame.time.get_ticks()
    message["duration"] = duration

# Ana ekranı çiz
def draw_main_screen():
    # Arka plan
    screen.fill(LIGHT_GRAY)
    
    # Başlık
    title = title_font.render("MARKET SEPETİ", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    # Ürün gridi (4 sütun)
    for i, product in enumerate(products):
        col = i % 4
        row = i // 4
        
        x = 50 + col * 240
        y = 100 + row * 200 - scroll["y"]
        
        # Ürün kartı
        pygame.draw.rect(screen, WHITE, (x, y, 200, 180), border_radius=10)
        pygame.draw.rect(screen, DARK_GRAY, (x, y, 200, 180), 2, border_radius=10)
        
        # Ürün resmi
        screen.blit(product.image, (x + 50, y + 20))
        
        # Ürün bilgileri
        name_text = font.render(product.name, True, BLACK)
        screen.blit(name_text, (x + 100 - name_text.get_width()//2, y + 130))
        
        price_text = price_font.render(f"{product.price:.2f} TL", True, GREEN)
        screen.blit(price_text, (x + 100 - price_text.get_width()//2, y + 160))
        
        # Sepete ekle butonu
        add_button = draw_button(x + 30, y + 130, 140, 40, "Sepete Ekle")
    
    # Kaydırma çubuğu
    scrollable_height = ((len(products) + 3) // 4) * 200 + 100
    scroll["max"] = max(0, scrollable_height - HEIGHT)
    
    if scroll["max"] > 0:
        scroll_ratio = scroll["y"] / scroll["max"]
        scroll_bar_height = HEIGHT * (HEIGHT / scrollable_height)
        scroll_bar_y = scroll_ratio * (HEIGHT - scroll_bar_height)
        pygame.draw.rect(screen, BLUE, (WIDTH - 20, scroll_bar_y, 15, scroll_bar_height), border_radius=5)
    
    # Sepet butonu
    total_items = sum(item.quantity for item in cart)
    cart_button = draw_button(WIDTH - 220, 20, 200, 60, f"Sepet ({total_items})", BLUE)
    
    # Mesaj gösterimi
    if message["show"]:
        elapsed = pygame.time.get_ticks() - message["time"]
        if elapsed < message["duration"]:
            msg_surf = font.render(message["text"], True, WHITE)
            msg_rect = pygame.Rect(
                WIDTH//2 - msg_surf.get_width()//2 - 20,
                HEIGHT - 100,
                msg_surf.get_width() + 40,
                50
            )
            pygame.draw.rect(screen, GREEN, msg_rect, border_radius=10)
            screen.blit(msg_surf, (WIDTH//2 - msg_surf.get_width()//2, HEIGHT - 85))
        else:
            message["show"] = False
    
    pygame.display.flip()

# Sepet ekranını çiz
def draw_cart_screen():
    # Arka plan
    screen.fill(LIGHT_GRAY)
    
    # Başlık
    title = title_font.render("ALIŞVERİŞ SEPETİ", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    # Fiyat bilgileri
    subtotal = sum(item.product.price * item.quantity for item in cart)
    tax = subtotal * 0.18
    total = subtotal + tax
    
    # Fiyat paneli
    pygame.draw.rect(screen, WHITE, (WIDTH - 300, 20, 280, 150), border_radius=10)
    pygame.draw.rect(screen, DARK_GRAY, (WIDTH - 300, 20, 280, 150), 2, border_radius=10)
    
    subtotal_text = font.render(f"Ara Toplam: {subtotal:.2f} TL", True, BLACK)
    screen.blit(subtotal_text, (WIDTH - 280, 40))
    
    tax_text = small_font.render(f"KDV (%18): {tax:.2f} TL", True, DARK_GRAY)
    screen.blit(tax_text, (WIDTH - 280, 80))
    
    total_text = price_font.render(f"Toplam: {total:.2f} TL", True, RED)
    screen.blit(total_text, (WIDTH - 280, 120))
    
    # Ürün listesi
    y_offset = 180
    for i, item in enumerate(cart):
        product = item.product
        quantity = item.quantity
        
        # Ürün kartı
        pygame.draw.rect(screen, WHITE, (20, y_offset + i * 100 - scroll["y"], WIDTH - 40, 90), border_radius=10)
        pygame.draw.rect(screen, DARK_GRAY, (20, y_offset + i * 100 - scroll["y"], WIDTH - 40, 90), 2, border_radius=10)
        
        # Ürün resmi
        screen.blit(product.image, (40, y_offset + i * 100 - scroll["y"] + 15))
        
        # Ürün bilgileri
        name_text = font.render(product.name, True, BLACK)
        screen.blit(name_text, (160, y_offset + i * 100 - scroll["y"] + 15))
        
        price_text = small_font.render(f"Birim: {product.price:.2f} TL", True, BLACK)
        screen.blit(price_text, (160, y_offset + i * 100 - scroll["y"] + 50))
        
        # Miktar kontrolü
        quantity_text = font.render(f"Adet: {quantity}", True, BLUE)
        screen.blit(quantity_text, (WIDTH - 400, y_offset + i * 100 - scroll["y"] + 30))
        
        # Butonlar
        dec_button = draw_button(WIDTH - 300, y_offset + i * 100 - scroll["y"] + 20, 40, 40, "-", YELLOW, BLACK, 20)
        inc_button = draw_button(WIDTH - 240, y_offset + i * 100 - scroll["y"] + 20, 40, 40, "+", YELLOW, BLACK, 20)
        remove_button = draw_button(WIDTH - 180, y_offset + i * 100 - scroll["y"] + 20, 120, 40, "Çıkar", RED)
    
    # Kaydırma çubuğu
    scrollable_height = len(cart) * 100 + 200
    scroll["max"] = max(0, scrollable_height - HEIGHT)
    
    if scroll["max"] > 0:
        scroll_ratio = scroll["y"] / scroll["max"]
        scroll_bar_height = HEIGHT * (HEIGHT / scrollable_height)
        scroll_bar_y = scroll_ratio * (HEIGHT - scroll_bar_height)
        pygame.draw.rect(screen, BLUE, (WIDTH - 20, scroll_bar_y, 15, scroll_bar_height), border_radius=5)
    
    # Butonlar
    back_button = draw_button(20, HEIGHT - 100, 200, 60, "Geri Dön", BLUE)
    
    if cart:
        checkout_button = draw_button(WIDTH - 220, HEIGHT - 100, 200, 60, f"Öde {total:.2f} TL", GREEN)
    
    pygame.display.flip()

# Ana döngü
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Fare tıklamaları
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if event.button == 1:  # Sol tık
                if current_screen == "main":
                    # Sepet butonu kontrolü
                    if WIDTH - 220 <= mouse_pos[0] <= WIDTH - 20 and 20 <= mouse_pos[1] <= 80:
                        current_screen = "cart"
                    
                    # Ürün ekleme
                    for i, product in enumerate(products):
                        col = i % 4
                        row = i // 4
                        x = 50 + col * 240
                        y = 100 + row * 200 - scroll["y"]
                        
                        if x + 30 <= mouse_pos[0] <= x + 170 and y + 130 <= mouse_pos[1] <= y + 170:
                            # Sepette var mı kontrolü
                            found = False
                            for item in cart:
                                if item.product == product:
                                    if item.quantity < product.stock:
                                        item.quantity += 1
                                        show_message(f"{product.name} sepete eklendi")
                                    else:
                                        show_message("Stok yetersiz!")
                                    found = True
                                    break
                            
                            if not found:
                                cart.append(CartItem(product, 1))
                                show_message(f"{product.name} sepete eklendi")
                
                elif current_screen == "cart":
                    # Geri dön butonu
                    if 20 <= mouse_pos[0] <= 220 and HEIGHT - 100 <= mouse_pos[1] <= HEIGHT - 40:
                        current_screen = "main"
                    
                    # Ödeme butonu
                    if cart and WIDTH - 220 <= mouse_pos[0] <= WIDTH - 20 and HEIGHT - 100 <= mouse_pos[1] <= HEIGHT - 40:
                        show_message("Ödeme başarıyla tamamlandı!")
                        cart.clear()
                    
                    # Sepet işlemleri
                    for i, item in enumerate(cart):
                        item_y = 180 + i * 100 - scroll["y"]
                        if 20 <= mouse_pos[1] <= item_y + 90:
                            # Azaltma butonu
                            if WIDTH - 300 <= mouse_pos[0] <= WIDTH - 260 and item_y + 20 <= mouse_pos[1] <= item_y + 60:
                                if item.quantity > 1:
                                    item.quantity -= 1
                                else:
                                    removed_product = cart.pop(i)
                                    show_message(f"{removed_product.product.name} sepetten çıkarıldı")
                                break
                            
                            # Artırma butonu
                            elif WIDTH - 240 <= mouse_pos[0] <= WIDTH - 200 and item_y + 20 <= mouse_pos[1] <= item_y + 60:
                                if item.quantity < item.product.stock:
                                    item.quantity += 1
                                else:
                                    show_message("Stok yetersiz!")
                                break
                            
                            # Çıkarma butonu
                            elif WIDTH - 180 <= mouse_pos[0] <= WIDTH - 60 and item_y + 20 <= mouse_pos[1] <= item_y + 60:
                                removed_product = cart.pop(i)
                                show_message(f"{removed_product.product.name} sepetten çıkarıldı")
                                break
            
            # Fare tekerleği ile kaydırma
            elif event.button == 4:  # Yukarı
                scroll["y"] = max(0, scroll["y"] - scroll["speed"])
            elif event.button == 5:  # Aşağı
                scroll["y"] = min(scroll["max"], scroll["y"] + scroll["speed"])
            
            # Kaydırmayı başlat
            elif event.button == 2:  # Orta tuş
                scroll["dragging"] = True
                scroll["start_y"] = mouse_pos[1]
        
        # Fare bırakma
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:  # Orta tuş
                scroll["dragging"] = False
        
        # Fare hareketi
        elif event.type == pygame.MOUSEMOTION:
            if scroll["dragging"]:
                scroll["y"] = max(0, min(scroll["max"], scroll["y"] + (scroll["start_y"] - event.pos[1])))
                scroll["start_y"] = event.pos[1]
    
    # Ekranı çiz
    if current_screen == "main":
        draw_main_screen()
    else:
        draw_cart_screen()
    
    # FPS kontrolü
    clock.tick(FPS)

# Pygame'i kapat
pygame.quit()
sys.exit()