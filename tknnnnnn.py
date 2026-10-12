import pygame #นำเข้าpygame
import random  #แจกไพ่แบบสุ่ม

pygame.init()

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Solitaire")

font = pygame.font.Font(None, 30)
win_font = pygame.font.Font(None, 100)
clock = pygame.time.Clock()

suits = ["S", "H", "D", "C"]
ranks = ["A", "2", "3", "4", "5", "6", "7",
"8", "9", "10", "J", "Q", "K"]

deck = []  #สร้าง list ว่างเพื่อเก็บไพ่ทั้งหมด

for suit in suits:  #สร้างไพ่ทั้งหมด 52 ใบ
    for rank in ranks:
        card = [rank, suit, True]  # True แสดงว่าไพ่หงายหน้า 
        deck.append(card)  #เอาไพ่แต่ละใบใส่ใน list deck
        
random.shuffle(deck)  #สับไพ่แบบสุ่ม

piles = [[],[],[],[],[],[],[]]  #สร้าง list ว่างเพื่อเก็บกองไพ่ 7 กอง

for i in range(7): #  7 กอง
    for j in range(7): #แจก 7 ใบ
        card = deck.pop()  #แจกไพ่ให้กองละ 7 ใบ โดยเอาไพ่จาก deck ออกไป
        
        if i < 4 and j < 3:  #ไพ่กองที่ 1-4 คว่ำ 3 ใบแรก
            card[2] = False  # False แสดงว่าไพ่คว่ำหน้า card = [rank, suit, True] ตน.2
        else:
            card[2] = True  # True แสดงว่าไพ่หงายหน้า
            
        piles[i].append(card)  #เอาไพ่แต่ละใบใส่ในกองไพ่แต่ละกอง
        
extra_cards = deck  #ไพ่ที่เหลือจากการแจกไพ่ 7 กอง

def show_piles(pile_number):
    pile = piles[pile_number - 1]  #เลือกกองไพ่ที่ต้องการแสดง
    
    i  = 0
    
    while i < len(pile):
        card = pile[i]
        
        if card[2] == True:  #ถ้าไพ่หงายหน้า
            print(card[0], card[1])  #แสดง rank และ suit ของไพ่
        else:
            print("X")  #แสดง X แทนไพ่คว่ำหน้า
            
        i += 1
        
#show_piles(1) #test แสดงกองไพ่กองที่ 1

def count_face_up_cards(pile_number):
    pile = piles[pile_number - 1]

    count = 0  #จำนวนไพ่หงาย
    i = 0      #ตำแหน่งไพ่ที่กำลังตรวจ

    while i < len(pile):
        card = pile[i]

        if card[2] == True:
            count += 1

        i += 1  #ไปตรวจใบถัดไป ทั้งไพ่หงายและไพ่คว่ำ

    return count

def can_place(card, destination):
    # กองว่างวางได้เฉพาะ K
    if len(destination) == 0:
        return card[0] == "K"

    top_card = destination[-1]

    # ไพ่ปลายทางต้องหงายหน้า
    if top_card[2] == False:
        return False

    # ต้องเป็นดอกเดียวกัน
    if card[1] != top_card[1]:
        return False

    # ไพ่ที่ย้ายต้องน้อยกว่าปลายทาง 1 แต้ม
    card_value = ranks.index(card[0])
    top_value = ranks.index(top_card[0])

    return card_value + 1 == top_value

completed_sets = []  # เก็บชุดไพ่ K ถึง A ที่เรียงสำเร็จ

def collect_completed_sets():
    for pile in piles:
        # ตรวจ 13 ใบสุดท้ายของกอง
        while len(pile) >= 13:
            cards = pile[-13:]
            suit = cards[0][1]
            complete = True

            for i in range(13):
                card = cards[i]

                # ต้องหงาย ดอกเดียวกัน และเรียง K ถึง A
                if (
                    card[2] == False
                    or card[1] != suit
                    or card[0] != ranks[12 - i]
                ):
                    complete = False
                    break

            if complete == False:
                break

            # เก็บทั้งชุด แล้วนำออกจากกอง
            completed_sets.append(cards)
            del pile[-13:]

            # พลิกไพ่ที่ถูกเปิดเผย
            if pile:
                pile[-1][2] = True

selected_pile = None   # กองที่เลือก
selected_index = None  # ตำแหน่งไพ่ที่เลือก

dragging = False
offset_x = 0
offset_y = 0


def restart_game():
    global piles, extra_cards
    global selected_pile, selected_index, dragging

    # สร้างไพ่ใหม่ 52 ใบ
    new_deck = []

    for suit in suits:
        for rank in ranks:
            new_deck.append([rank, suit, True])

    random.shuffle(new_deck)

    # แจกไพ่ใหม่ 7 กอง
    piles = [[], [], [], [], [], [], []]

    for i in range(7):
        for j in range(7):
            card = new_deck.pop()

            # กอง 1–4 คว่ำ 3 ใบแรก
            if i < 4 and j < 3:
                card[2] = False

            piles[i].append(card)

    extra_cards = new_deck

    # ล้างชุดที่สำเร็จและยกเลิกการลาก
    completed_sets.clear()
    selected_pile = None
    selected_index = None
    dragging = False

restart_rect = pygame.Rect(300, 55, 160, 50) # ตำแหน่งปุ่มรีสตาร์ท

# ทดสอบกติกาการลากไพ่ชั่วคราว
completed_sets.clear()
extra_cards.clear()

running = True

while running:
        # รับเหตุการณ์
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                selected_pile = None
                selected_index = None
                dragging = False

                mouse_x, mouse_y = event.pos

                # คลิกเริ่มเกมใหม่
                if restart_rect.collidepoint(mouse_x, mouse_y):
                    restart_game()
                    continue

                # คลิกกองไพ่สำรองซ้ายบน
                stock_rect = pygame.Rect(40, 15, 100, 140)

                if stock_rect.collidepoint(mouse_x, mouse_y):
                    if len(extra_cards) > 0:
                        for i in range(3):
                            if len(extra_cards) > 0:
                                card = extra_cards.pop()
                                card[2] = True
                                piles[i].append(card)

                    # จบเหตุการณ์นี้ ไม่ตรวจเลือกไพ่ต่อ
                    continue

                for i in range(7):
                    pile = piles[i]
                    x = 40 + i * 135

                    for j in range(len(pile) - 1, -1, -1):
                        y = 180 + j * 45

                        if j == len(pile) - 1:
                            height = 140
                        else:
                            height = 45

                        card_rect = pygame.Rect(x, y, 100, height)

                        if card_rect.collidepoint(mouse_x, mouse_y):
                            if pile[j][2] == True:
                                selected_pile = i
                                selected_index = j
                                dragging = True

                                offset_x = mouse_x - x
                                offset_y = mouse_y - y

                            break

                    if selected_pile is not None:
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging:
                mouse_x, mouse_y = event.pos
                moving_cards = piles[selected_pile][selected_index:]

                for i in range(7):
                    x = 40 + i * 135

                    drop_rect = pygame.Rect(
                        x, 180, 100,
                        screen.get_height() - 180
                    )

                    if drop_rect.collidepoint(mouse_x, mouse_y):
                        if i != selected_pile:
                            if can_place(moving_cards[0], piles[i]):
                                # ย้ายไพ่เพียงครั้งเดียว
                                piles[i].extend(moving_cards)
                                del piles[selected_pile][selected_index:]

                                # พลิกไพ่ที่ถูกเปิดเผย
                                if piles[selected_pile]:
                                    piles[selected_pile][-1][2] = True

                        break

                dragging = False
                selected_pile = None
                selected_index = None

    # ตรวจชุดที่สำเร็จเมื่อไม่ได้ลากไพ่
    if not dragging:
       collect_completed_sets()

    # ล้างภาพเก่าทุกเฟรม
    screen.fill((30, 100, 60))

        # ปุ่ม Restart
    pygame.draw.rect(
        screen, (240, 240, 240),
        restart_rect, border_radius=8
    )
    pygame.draw.rect(
        screen, (0, 0, 0),
        restart_rect, 2, border_radius=8
    )

    restart_text = font.render("Restart", True, (0, 0, 0))
    restart_text_rect = restart_text.get_rect(
        center=restart_rect.center
    )
    screen.blit(restart_text, restart_text_rect)

    # ช่องเก็บชุดไพ่สำเร็จ 4 ช่อง
    for i in range(4):
        x = 530 + i * 110
        slot = pygame.Rect(x, 15, 100, 140)

        if i < len(completed_sets):
            # ใช้ดอกไพ่จากชุดที่เก็บสำเร็จ
            suit = completed_sets[i][0][1]

            pygame.draw.rect(
                screen, (255, 255, 255),
                slot, border_radius=8
            )

            if suit == "H" or suit == "D":
                text_color = (200, 0, 0)
            else:
                text_color = (0, 0, 0)

            text = font.render("K " + suit, True, text_color)
            screen.blit(text, (x + 8, 23))

        else:
            # ช่องที่ยังไม่มีชุดไพ่
            pygame.draw.rect(
                screen, (20, 75, 45),
                slot, border_radius=8
            )

            text = font.render("K - A", True, (200, 200, 200))
            screen.blit(text, (x + 20, 70))

        pygame.draw.rect(
            screen, (200, 200, 200),
            slot, 2, border_radius=8
        )

    # วาดไพ่ทั้ง 7 กอง
    for i in range(7):
        pile = piles[i]

        for j in range(len(pile)):
            # ไม่วาดกลุ่มที่กำลังลากไว้ที่เดิม
            if dragging and selected_pile == i:
                if j >= selected_index:
                    continue

            card = pile[j]

            x = 40 + i * 135
            y = 180 + j * 45
            rect = pygame.Rect(x, y, 100, 140)

            if card[2] == True:
                pygame.draw.rect(screen, (255, 255, 255), rect)

                if card[1] == "H" or card[1] == "D":
                    text_color = (200, 0, 0)
                else:
                    text_color = (0, 0, 0)

                text = font.render(
                    card[0] + " " + card[1],
                    True,
                    text_color
                )
                screen.blit(text, (x + 8, y + 8))

            else:
                pygame.draw.rect(screen, (50, 70, 160), rect)

            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        # กองไพ่สำรองด้านซ้ายบน
    stock_rect = pygame.Rect(40, 15, 100, 140)

    if len(extra_cards) > 0:
        # หลังไพ่
        pygame.draw.rect(
            screen, (50, 70, 160), stock_rect, border_radius=8
        )
    else:
        # ช่องว่างเมื่อแจกหมด
        pygame.draw.rect(
            screen, (20, 75, 45), stock_rect, border_radius=8
        )

    pygame.draw.rect(
        screen, (200, 200, 200), stock_rect, 2, border_radius=8
    )

    text = font.render(
        "Stock: " + str(len(extra_cards)),
        True,
        (255, 255, 255)
    )
    screen.blit(text, (155, 70))

    # วาดกลุ่มไพ่ตามเมาส์เป็นลำดับสุดท้าย
    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        moving_cards = piles[selected_pile][selected_index:]

        for j in range(len(moving_cards)):
            card = moving_cards[j]

            x = mouse_x - offset_x
            y = mouse_y - offset_y + j * 45
            rect = pygame.Rect(x, y, 100, 140)

            pygame.draw.rect(screen, (255, 255, 255), rect)

            if card[1] == "H" or card[1] == "D":
                text_color = (200, 0, 0)
            else:
                text_color = (0, 0, 0)

            text = font.render(
                card[0] + " " + card[1],
                True,
                text_color
            )
            screen.blit(text, (x + 8, y + 8))

            pygame.draw.rect(screen, (255, 220, 0), rect, 3)

            pygame.draw.rect(screen, (255, 220, 0), rect, 3)

    # ตรวจชนะ
    if len(completed_sets) == 4:
        win_box = pygame.Rect(0, 0, 460, 150)
        win_box.center = screen.get_rect().center

        pygame.draw.rect(
            screen, (20, 75, 45), win_box, border_radius=15
        )
        pygame.draw.rect(
            screen, (255, 220, 0), win_box, 3, border_radius=15
        )

        win_text = win_font.render(
            "YOU WIN!", True, (255, 255, 255)
        )
        text_rect = win_text.get_rect(center=win_box.center)
        screen.blit(win_text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()



        
        
        







