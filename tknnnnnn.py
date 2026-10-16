import pygame #นำเข้าpygame
import random  #แจกไพ่แบบสุ่ม
from pathlib import Path #นำเข้าpath

pygame.init()

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Solitaire")

font = pygame.font.Font(None, 30)
status_font = pygame.font.Font(None, 24)
result_font = pygame.font.Font(None, 64)
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



# ตำแหน่งปุ่ม Hint
hint_rect = pygame.Rect(30, 920, 120, 50)

# เก็บตำแหน่งไพ่ที่ระบบแนะนำ
hint_move = None
hint_start_time = 0
hint_duration = 1500  # แสดงคำใบ้ 1.5 วินาที

# ข้อความเมื่อไม่มีไพ่ที่ย้ายได้
hint_message = ""
hint_message_time = 0


def find_hint():
    # ตรวจสอบไพ่จากทั้ง 7 กอง
    for i in range(7):
        source = piles[i]

        # ตรวจไพ่แต่ละใบในกองต้นทาง
        for j in range(len(source)):

            # ข้ามไพ่คว่ำ
            if source[j][2] == False:
                continue

            card = source[j]

            # ตรวจสอบกองปลายทางทั้ง 7 กอง
            for k in range(7):

                # ห้ามย้ายกลับกองเดิม
                if i == k:
                    continue

                # ใช้กติกาจากฟังก์ชันเดิม
                if can_place(card, piles[k]):

                    # ป้องกัน Hint ที่ย้าย K กองเดียว
                    # ไปยังกองว่างโดยไม่เกิดประโยชน์
                    if j == 0 and len(piles[k]) == 0:
                        continue

                    # คืนตำแหน่งต้นทาง, ไพ่, ปลายทาง
                    return (i, j, k)

    # ไม่พบการย้ายที่ทำได้
    return None


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
hint_move = None
hint_message = ""
offset_x = 0
offset_y = 0

def has_available_move():
    # ยังแจกไพ่สำรองได้ ถือว่ายังเล่นต่อได้
    if len(extra_cards) > 0:
        return True

    # ตรวจไพ่หงายทุกใบ ไม่ใช่เฉพาะใบสุดท้าย
    for source_index in range(7):
        for card in piles[source_index]:
            if card[2] == False:
                continue

            for destination_index in range(7):
                if source_index == destination_index:
                    continue

                if can_place(card, piles[destination_index]):
                    return True

    return False

def restart_game():
    global piles, extra_cards
    global selected_pile, selected_index, dragging
    global move_count
    global start_ticks, elapsed_seconds, game_won, score
    global game_over

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
    move_count = 0
    start_ticks = pygame.time.get_ticks()
    elapsed_seconds = 0
    game_won = False
    score = 10000
    game_over = False

restart_rect = pygame.Rect(300, 55, 160, 50) # ตำแหน่งปุ่มรีสตาร์ท

# โฟลเดอร์รูปไพ่
cards_folder = (
    Path(__file__).resolve().parent / "assets" / "cards"
)

suit_names = {
    "S": "spades",
    "H": "hearts",
    "D": "diamonds",
    "C": "clubs"
}

card_images = {}

# โหลดหน้าไพ่ทั้งหมด
for suit in suits:
    for rank in ranks:
        if rank.isdigit():
            file_rank = rank.zfill(2)  # 2 เปลี่ยนเป็น 02
        else:
            file_rank = rank

        filename = (
            "card_" + suit_names[suit] + "_" + file_rank + ".png"
        )

        image = pygame.image.load(
            str(cards_folder / filename)
        ).convert_alpha()

        card_images[(rank, suit)] = pygame.transform.smoothscale(
            image, (100, 140)
        )

# โหลดหลังไพ่
back_image = pygame.image.load(
    str(cards_folder / "card_back.png")
).convert_alpha()

back_image = pygame.transform.smoothscale(
    back_image, (100, 140)
)

move_count = 0

start_ticks = pygame.time.get_ticks()
elapsed_seconds = 0
game_won = False
game_over = False
score = 10000

completed_sets.clear()
extra_cards.clear()

piles = [
    [["A", "S", True]],
    [["A", "H", True]],
    [["A", "D", True]],
    [["A", "C", True]],
    [],
    [],
    []
]
#ใส่กอ่น running true

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
                

                # ถ้าคลิกที่อื่นนอกจากปุ่ม Hint ให้ปิดคำใบ้
                if not hint_rect.collidepoint(mouse_x, mouse_y):
                    hint_move = None
                    hint_message = ""

                # คลิกเริ่มเกมใหม่
                if restart_rect.collidepoint(mouse_x, mouse_y):
                    restart_game()
                    continue
                
                
                if hint_rect.collidepoint(mouse_x, mouse_y):
                    hint_move = find_hint()

                    if hint_move is None:
                        hint_message = "NO AVAILABLE MOVES"
                        hint_message_time = pygame.time.get_ticks()
                    else:
                        hint_message = ""
                        hint_start_time = pygame.time.get_ticks()

                    continue


                # เกมชนะ
                if game_won or game_over:
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

                        # แจกทั้ง 3 ใบ นับเป็น 1 ครั้ง
                        move_count += 1

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

                                move_count += 1

                                # พลิกไพ่ที่ถูกเปิดเผย
                                if piles[selected_pile]:
                                    piles[selected_pile][-1][2] = True
                        break

                dragging = False
                selected_pile = None
                selected_index = None

    # ตรวจและเก็บชุดเมื่อไม่ได้ลาก
    if not dragging and not game_won and not game_over:
        collect_completed_sets()

    # อัปเดตจนกว่าเกมจะจบ
    if not game_won and not game_over:
        elapsed_seconds = (
            pygame.time.get_ticks() - start_ticks
        ) // 1000

        score = max(
            0,
            10000 - elapsed_seconds * 2 - move_count * 20
        )

        # ตรวจชนะก่อนตรวจว่าเล่นต่อไม่ได้
        if len(completed_sets) == 4:
            game_won = True
            
        # ปิดคำใบ้อัตโนมัติหลัง 1.5 วินาที
        if hint_move is not None:
            current_time = pygame.time.get_ticks()

        elif not dragging and not has_available_move():
            game_over = True

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
    
    
    # วาดปุ่ม Hint
    pygame.draw.rect(
                    screen, (255, 210, 70),
                    hint_rect, border_radius=8
                )

    pygame.draw.rect(
                    screen, (0, 0, 0),
                    hint_rect, 2, border_radius=8
                )

    hint_text = font.render("Hint", True, (0, 0, 0))
    hint_text_rect = hint_text.get_rect(center=hint_rect.center)

    screen.blit(hint_text, hint_text_rect)


    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60

    status_text = status_font.render(
        f"Score: {score}    "
        f"Time: {minutes:02d}:{seconds:02d}    "
        f"Moves: {move_count}",
        True,
        (255, 255, 255)
    )
    screen.blit(status_text, (40, 160))

    # ช่องเก็บชุดไพ่สำเร็จ 4 ช่อง
    for i in range(4):
        x = 530 + i * 110
        slot = pygame.Rect(x, 15, 100, 140)

        if i < len(completed_sets):
            suit = completed_sets[i][0][1]
            screen.blit(
                card_images[("K", suit)],
                slot.topleft
            )

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

            if card[2]:
                image = card_images[(card[0], card[1])]
            else:
                image = back_image

            screen.blit(image, (x, y))
            
            # ===== แสดงคำแนะนำจากปุ่ม Hint =====
    if hint_move is not None and not dragging:

        source_i, card_j, dest_i = hint_move

        # ไพ่ต้นทาง (สีเหลือง)
        source_x = 40 + source_i * 135
        source_y = 180 + card_j * 45

        pygame.draw.rect(
            screen, (255, 255, 0),
            (source_x, source_y, 100, 140), 5
        )

        # กองปลายทาง (สีฟ้า)
        dest_x = 40 + dest_i * 135

        if len(piles[dest_i]) > 0:
            dest_y = 180 + (len(piles[dest_i]) - 1) * 45
        else:
            dest_y = 180

        pygame.draw.rect(
            screen, (0, 255, 255),
            (dest_x, dest_y, 100, 140), 5
        )

        # กองไพ่สำรองด้านซ้ายบน
    stock_rect = pygame.Rect(40, 15, 100, 140)

    if len(extra_cards) > 0:
        screen.blit(back_image, stock_rect.topleft)
    else:
        pygame.draw.rect(
            screen, (20, 75, 45),
            stock_rect, border_radius=8
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

            image = card_images[(card[0], card[1])]
            screen.blit(image, (x, y))

            pygame.draw.rect(
                screen, (255, 220, 0), rect, 3
            )

    # หน้าสรุปเมื่อเกมจบ
    if game_won or game_over:
        result_box = pygame.Rect(0, 0, 560, 340)
        result_box.center = screen.get_rect().center

        pygame.draw.rect(
            screen, (20, 60, 40),
            result_box, border_radius=15
        )
        pygame.draw.rect(
            screen, (255, 220, 0),
            result_box, 3, border_radius=15
        )

        if game_won:
            title = "YOU WIN!"
        else:
            title = "NO MOVES LEFT"

        title_image = result_font.render(
            title, True, (255, 220, 0)
        )
        title_rect = title_image.get_rect(
            center=(result_box.centerx, result_box.y + 55)
        )
        screen.blit(title_image, title_rect)

        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60

        lines = [
            f"Score: {score}",
            f"Time: {minutes:02d}:{seconds:02d}",
            f"Moves: {move_count}",
            f"Completed sets: {len(completed_sets)} / 4",
            "Click Restart to play again"
        ]

        for i in range(len(lines)):
            line_image = font.render(
                lines[i], True, (255, 255, 255)
            )
            line_rect = line_image.get_rect(
                center=(
                    result_box.centerx,
                    result_box.y + 120 + i * 40
                )
            )
            screen.blit(line_image, line_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()



        
        
        







