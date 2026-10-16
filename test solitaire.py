import pygame  # ไลบรารีสำหรับสร้างเกม
import random  # ใช้สุ่มไพ่
from pathlib import Path  # ใช้จัดการตำแหน่งไฟล์รูปภาพ

pygame.init()  # เริ่มต้น Pygame

# ==================== ตั้งค่าหน้าจอ ====================

WIDTH = 1000  # ความกว้างหน้าจอ
HEIGHT = 1000  # ความสูงหน้าจอ

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # สร้างหน้าต่างเกม
pygame.display.set_caption("Scorpion Solitaire")  # ตั้งชื่อหน้าต่าง

font = pygame.font.Font(None, 30)  # ฟอนต์ข้อความทั่วไป
status_font = pygame.font.Font(None, 24)  # ฟอนต์แสดงคะแนนและเวลา
win_font = pygame.font.Font(None, 80)  # ฟอนต์ข้อความชนะและแพ้
clock = pygame.time.Clock()  # ควบคุมความเร็วของเกม

# ==================== ตั้งค่าขนาดและตำแหน่งไพ่ ====================

CARD_WIDTH = 100  # ความกว้างไพ่
CARD_HEIGHT = 140  # ความสูงไพ่

PILE_START_X = 40  # ตำแหน่ง X เริ่มต้นของกองไพ่
PILE_START_Y = 180  # ตำแหน่ง Y เริ่มต้นของกองไพ่
PILE_GAP_X = 135  # ระยะห่างระหว่างกองไพ่

NORMAL_SPACING = 45  # ระยะห่างปกติระหว่างไพ่
BOTTOM_MARGIN = 20  # ระยะเว้นจากขอบล่างหน้าจอ

suits = ["S", "H", "D", "C"]  # ดอกไพ่ทั้ง 4 ดอก

ranks = [
    "A", "2", "3", "4", "5", "6", "7",
    "8", "9", "10", "J", "Q", "K"
]  # ลำดับแต้มไพ่จากน้อยไปมาก

# ==================== กำหนดปุ่ม ====================

restart_rect = pygame.Rect(300, 55, 160, 50)  # ปุ่มเริ่มเกมใหม่
hint_rect = pygame.Rect(30, 920, 120, 50)  # ปุ่มคำใบ้
stock_rect = pygame.Rect(40, 15, 100, 140)  # กองไพ่สำรอง
play_again_rect = pygame.Rect(390, 590, 220, 55)  # ปุ่มเล่นอีกครั้ง

# ==================== ตัวแปรของเกม ====================

piles = [[], [], [], [], [], [], []]  # กองไพ่ 7 กอง
extra_cards = []  # ไพ่สำรองที่ยังไม่ได้แจก
completed_sets = []  # ชุดไพ่ที่เรียงสำเร็จแล้ว

selected_pile = None  # กองไพ่ที่เลือก
selected_index = None  # ตำแหน่งไพ่ที่เลือก
dragging = False  # สถานะการลากไพ่

offset_x = 0  # ระยะห่างเมาส์กับขอบซ้ายของไพ่
offset_y = 0  # ระยะห่างเมาส์กับขอบบนของไพ่

move_count = 0  # จำนวนครั้งที่ย้ายหรือแจกไพ่
start_ticks = pygame.time.get_ticks()  # เวลาเริ่มต้นเกม
elapsed_seconds = 0  # เวลาที่เล่นไปแล้ว
score = 10000  # คะแนนเริ่มต้น

game_won = False  # สถานะชนะเกม
game_over = False  # สถานะแพ้เกม

hint_move = None  # เก็บตำแหน่งไพ่ที่ระบบแนะนำ
hint_start_time = 0  # เวลาเริ่มแสดงคำใบ้
hint_duration = 1500  # แสดงคำใบ้ 1.5 วินาที

hint_message = ""  # ข้อความแจ้งเตือนของ Hint
hint_message_time = 0  # เวลาเริ่มแสดงข้อความ

# ==================== โหลดรูปภาพไพ่ ====================

cards_folder = (
    Path(__file__).resolve().parent / "assets" / "cards"
)  # โฟลเดอร์เก็บรูปไพ่

suit_names = {
    "S": "spades",  # โพดำ
    "H": "hearts",  # โพแดง
    "D": "diamonds",  # ข้าวหลามตัด
    "C": "clubs"  # ดอกจิก
}

card_images = {}  # เก็บรูปภาพไพ่ทั้งหมด

for suit in suits:  # วนลูปดอกไพ่
    for rank in ranks:  # วนลูปแต้มไพ่

        if rank.isdigit():  # หากแต้มไพ่เป็นตัวเลข
            file_rank = rank.zfill(2)  # เติม 0 ด้านหน้า เช่น 2 เป็น 02
        else:
            file_rank = rank  # ใช้ชื่อเดิมสำหรับ A J Q K

        filename = (
            "card_" + suit_names[suit] + "_"
            + file_rank + ".png"
        )  # สร้างชื่อไฟล์รูปไพ่

        image = pygame.image.load(
            str(cards_folder / filename)
        ).convert_alpha()  # โหลดรูปไพ่พร้อมพื้นหลังโปร่งใส

        card_images[(rank, suit)] = (
            pygame.transform.smoothscale(
                image, (CARD_WIDTH, CARD_HEIGHT)
            )
        )  # ปรับขนาดและเก็บรูปไพ่

back_image = pygame.image.load(
    str(cards_folder / "card_back.png")
).convert_alpha()  # โหลดรูปหลังไพ่

back_image = pygame.transform.smoothscale(
    back_image, (CARD_WIDTH, CARD_HEIGHT)
)  # ปรับขนาดรูปหลังไพ่

# ==================== ฟังก์ชันจัดตำแหน่งไพ่ ====================

def get_card_spacing(card_count):  # คำนวณระยะห่างตามจำนวนไพ่

    available_height = (
        HEIGHT - PILE_START_Y - CARD_HEIGHT - BOTTOM_MARGIN
    )  # คำนวณพื้นที่แนวตั้งที่ใช้วางไพ่ได้

    if card_count <= 1:  # หากมีไพ่ไม่เกิน 1 ใบ
        return NORMAL_SPACING  # ใช้ระยะห่างปกติ

    spacing = available_height / (card_count - 1)  # คำนวณระยะที่พอดีหน้าจอ

    return min(NORMAL_SPACING, spacing)  # จำกัดระยะไม่ให้เกินค่าปกติ


def get_card_y(pile_index, card_index):  # หาตำแหน่ง Y ของไพ่

    card_count = len(piles[pile_index])  # นับจำนวนไพ่ในกอง
    spacing = get_card_spacing(card_count)  # คำนวณระยะห่าง

    return int(
        PILE_START_Y + card_index * spacing
    )  # คืนตำแหน่ง Y ของไพ่


def get_pile_x(pile_index):  # หาตำแหน่ง X ของกองไพ่

    return PILE_START_X + pile_index * PILE_GAP_X  # คืนตำแหน่ง X

# ==================== ฟังก์ชันแสดงข้อมูลไพ่ ====================

def show_piles(pile_number):  # แสดงไพ่ในกองที่ระบุ

    pile = piles[pile_number - 1]  # เลือกกองไพ่
    i = 0  # เริ่มจากไพ่ใบแรก

    while i < len(pile):  # วนจนครบทุกใบ

        card = pile[i]  # อ่านข้อมูลไพ่

        if card[2]:  # หากไพ่หงายหน้า
            print(card[0], card[1])  # แสดงแต้มและดอก
        else:
            print("X")  # แสดง X แทนไพ่คว่ำหน้า

        i += 1  # เลื่อนไปไพ่ใบถัดไป


def count_face_up_cards(pile_number):  # นับไพ่หงายหน้า

    pile = piles[pile_number - 1]  # เลือกกองไพ่
    count = 0  # ตัวนับจำนวนไพ่
    i = 0  # ตำแหน่งเริ่มต้น

    while i < len(pile):  # ตรวจไพ่ทุกใบ

        if pile[i][2]:  # หากไพ่หงายหน้า
            count += 1  # เพิ่มจำนวนไพ่หงาย

        i += 1  # ตรวจใบถัดไป

    return count  # คืนค่าจำนวนไพ่หงาย

# ==================== ฟังก์ชันตรวจสอบการวางไพ่ ====================

def can_place(card, destination):  # ตรวจสอบว่าวางไพ่ได้หรือไม่

    if len(destination) == 0:  # หากกองปลายทางว่าง
        return card[0] == "K"  # วางได้เฉพาะไพ่ K

    top_card = destination[-1]  # อ่านไพ่ใบบนสุดของกองปลายทาง

    if not top_card[2]:  # หากไพ่ปลายทางคว่ำหน้า
        return False  # ไม่อนุญาตให้วาง

    if card[1] != top_card[1]:  # หากไพ่คนละดอก
        return False  # ไม่อนุญาตให้วาง

    card_value = ranks.index(card[0])  # ลำดับแต้มไพ่ต้นทาง
    top_value = ranks.index(top_card[0])  # ลำดับแต้มไพ่ปลายทาง

    return card_value + 1 == top_value  # ต้องมีแต้มต่ำกว่า 1 ลำดับ

# ==================== ฟังก์ชัน Hint ====================

def find_hint():  # ค้นหาการย้ายไพ่ที่สามารถทำได้

    for i in range(7):  # ตรวจทุกกองต้นทาง

        source = piles[i]  # เลือกกองต้นทาง

        for j in range(len(source)):  # ตรวจไพ่ทุกใบ

            if not source[j][2]:  # หากไพ่คว่ำหน้า
                continue  # ข้ามไพ่ใบนี้

            card = source[j]  # เลือกไพ่ที่หงายหน้า

            for k in range(7):  # ตรวจทุกกองปลายทาง

                if i == k:  # หากเป็นกองเดียวกัน
                    continue  # ข้ามกองนี้

                if can_place(card, piles[k]):  # ตรวจว่าวางได้หรือไม่

                    if j == 0 and len(piles[k]) == 0:
                        continue  # ไม่แนะนำการย้ายทั้งกองไปกองว่าง

                    return (i, j, k)  # คืนกองต้นทาง ตำแหน่งไพ่ และกองปลายทาง

    return None  # ไม่พบการย้ายที่แนะนำได้

# ==================== ฟังก์ชันตรวจชุดไพ่สำเร็จ ====================

def collect_completed_sets():  # ตรวจชุดไพ่ K ถึง A ที่เรียงสำเร็จ

    for pile in piles:  # ตรวจทุกกองไพ่

        while len(pile) >= 13:  # ต้องมีไพ่อย่างน้อย 13 ใบ

            cards = pile[-13:]  # เลือกไพ่ 13 ใบสุดท้าย
            suit = cards[0][1]  # อ่านดอกของไพ่ใบแรก
            complete = True  # กำหนดค่าเริ่มต้นว่าชุดสมบูรณ์

            for i in range(13):  # ตรวจไพ่ทั้ง 13 ใบ

                card = cards[i]  # อ่านไพ่ปัจจุบัน

                if (
                    not card[2]  # ไพ่ต้องหงายหน้า
                    or card[1] != suit  # ไพ่ต้องเป็นดอกเดียวกัน
                    or card[0] != ranks[12 - i]  # ไพ่ต้องเรียง K ถึง A
                ):
                    complete = False  # ชุดไพ่ไม่สมบูรณ์
                    break  # หยุดตรวจ

            if not complete:  # หากชุดไม่สมบูรณ์
                break  # หยุดตรวจชุดนี้

            completed_sets.append(cards)  # เก็บชุดไพ่ที่เรียงสำเร็จ
            del pile[-13:]  # ลบไพ่ 13 ใบออกจากกอง

            if pile:  # หากยังมีไพ่เหลือ
                pile[-1][2] = True  # เปิดไพ่ใบบนสุด

# ==================== ฟังก์ชันตรวจ GAME OVER ====================

def check_game_over():  # ตรวจสอบว่าเกมแพ้แล้วหรือไม่

    if len(extra_cards) > 0:  # หากยังมีไพ่สำรอง
        return False  # ยังไม่จบเกม

    if len(completed_sets) == 4:  # หากเรียงครบ 4 ชุด
        return False  # ถือว่าชนะเกม

    if find_hint() is not None:  # หากยังมีการย้ายที่ Hint ยอมรับ
        return False  # ยังไม่จบเกม

    return True  # ไพ่สำรองหมดและไม่พบการย้ายที่ Hint ยอมรับ

# ==================== ฟังก์ชัน Restart ====================

def restart_game():  # เริ่มเกมใหม่และรีเซ็ตข้อมูล

    global piles, extra_cards  # อ้างอิงกองไพ่และไพ่สำรอง
    global selected_pile, selected_index, dragging  # อ้างอิงการลากไพ่
    global move_count, start_ticks, elapsed_seconds  # อ้างอิงจำนวนครั้งและเวลา
    global game_won, game_over, score  # อ้างอิงสถานะเกมและคะแนน
    global hint_move, hint_message  # อ้างอิงข้อมูลคำใบ้
    global hint_start_time, hint_message_time  # อ้างอิงเวลาคำใบ้
    global offset_x, offset_y  # อ้างอิงระยะเมาส์กับไพ่

    new_deck = []  # สร้างสำรับไพ่ใหม่

    for suit in suits:  # วนทุกดอกไพ่
        for rank in ranks:  # วนทุกแต้มไพ่
            new_deck.append([rank, suit, True])  # เพิ่มไพ่ลงสำรับ

    random.shuffle(new_deck)  # สับไพ่

    piles = [[], [], [], [], [], [], []]  # สร้างกองไพ่ใหม่ 7 กอง

    for i in range(7):  # แจกไพ่ทั้ง 7 กอง
        for j in range(7):  # แจกกองละ 7 ใบ

            card = new_deck.pop()  # หยิบไพ่จากสำรับ

            if i < 4 and j < 3:  # กอง 1-4 คว่ำ 3 ใบแรก
                card[2] = False  # คว่ำหน้าไพ่
            else:
                card[2] = True  # หงายหน้าไพ่

            piles[i].append(card)  # เพิ่มไพ่ลงกอง

    extra_cards = new_deck  # เก็บไพ่ที่เหลือเป็นไพ่สำรอง
    completed_sets.clear()  # ล้างชุดไพ่สำเร็จ

    selected_pile = None  # ยกเลิกกองที่เลือก
    selected_index = None  # ยกเลิกไพ่ที่เลือก
    dragging = False  # หยุดการลากไพ่

    offset_x = 0  # รีเซ็ตระยะเมาส์แนวนอน
    offset_y = 0  # รีเซ็ตระยะเมาส์แนวตั้ง

    move_count = 0  # รีเซ็ตจำนวนครั้งที่ย้าย
    start_ticks = pygame.time.get_ticks()  # เริ่มจับเวลาใหม่
    elapsed_seconds = 0  # รีเซ็ตเวลาที่เล่น
    score = 10000  # รีเซ็ตคะแนน

    game_won = False  # ยกเลิกสถานะชนะ
    game_over = False  # ยกเลิกสถานะแพ้

    hint_move = None  # ล้างคำใบ้
    hint_message = ""  # ล้างข้อความคำใบ้
    hint_start_time = 0  # รีเซ็ตเวลาคำใบ้
    hint_message_time = 0  # รีเซ็ตเวลาแจ้งเตือน

# ==================== ฟังก์ชันวาดปุ่ม ====================

def draw_button(rect, text, color):  # วาดปุ่มพร้อมข้อความ

    pygame.draw.rect(
        screen, color, rect, border_radius=10
    )  # วาดพื้นหลังปุ่ม

    pygame.draw.rect(
        screen, (0, 0, 0), rect, 2, border_radius=10
    )  # วาดเส้นขอบปุ่ม

    text_surface = font.render(
        text, True, (0, 0, 0)
    )  # สร้างข้อความบนปุ่ม

    screen.blit(
        text_surface,
        text_surface.get_rect(center=rect.center)
    )  # แสดงข้อความกลางปุ่ม

# ==================== ฟังก์ชันหน้าสรุปผล ====================

def draw_game_result():  # แสดงผลหลังชนะหรือแพ้

    overlay = pygame.Surface(
        (WIDTH, HEIGHT), pygame.SRCALPHA
    )  # สร้างพื้นหลังโปร่งใส

    overlay.fill((0, 0, 0, 160))  # เติมสีดำโปร่งแสง
    screen.blit(overlay, (0, 0))  # วาดทับหน้าจอเกม

    result_box = pygame.Rect(
        250, 290, 500, 390
    )  # กำหนดพื้นที่กล่องสรุปผล

    pygame.draw.rect(
        screen, (30, 45, 40),
        result_box, border_radius=18
    )  # วาดพื้นหลังกล่อง

    if game_won:  # หากผู้เล่นชนะ
        border_color = (255, 215, 70)  # ใช้สีเหลือง
        result_title = "YOU WIN!"  # ข้อความชนะ
    else:
        border_color = (255, 80, 80)  # ใช้สีแดง
        result_title = "GAME OVER"  # ข้อความแพ้

    pygame.draw.rect(
        screen, border_color,
        result_box, 4, border_radius=18
    )  # วาดเส้นขอบกล่อง

    title_surface = win_font.render(
        result_title, True, border_color
    )  # สร้างข้อความผลเกม

    screen.blit(
        title_surface,
        title_surface.get_rect(center=(500, 350))
    )  # แสดงหัวข้อผลเกม

    score_text = font.render(
        f"Final Score: {score}",
        True, (255, 255, 255)
    )  # สร้างข้อความคะแนนสุดท้าย

    screen.blit(
        score_text,
        score_text.get_rect(center=(500, 430))
    )  # แสดงคะแนนสุดท้าย

    minutes = elapsed_seconds // 60  # คำนวณนาที
    seconds = elapsed_seconds % 60  # คำนวณวินาที

    time_text = font.render(
        f"Time: {minutes:02d}:{seconds:02d}",
        True, (255, 255, 255)
    )  # สร้างข้อความเวลา

    screen.blit(
        time_text,
        time_text.get_rect(center=(500, 475))
    )  # แสดงเวลาที่ใช้

    moves_text = font.render(
        f"Moves: {move_count}",
        True, (255, 255, 255)
    )  # สร้างข้อความจำนวนครั้งที่ย้าย

    screen.blit(
        moves_text,
        moves_text.get_rect(center=(500, 520))
    )  # แสดงจำนวนครั้งที่ย้าย

    draw_button(
        play_again_rect, "Play Again", (255, 210, 70)
    )  # วาดปุ่มเล่นอีกครั้ง

# ==================== เริ่มเกมครั้งแรก ====================

restart_game()  # สร้างและแจกไพ่เริ่มต้น

# ==================== MAIN LOOP ====================

#ทดสอบกติกาการลากไพ่
completed_sets.clear()
extra_cards.clear()

piles = [
    [
        ["Q", "D", False],
        ["7", "S", True],
        ["3", "H", True],
        ["J", "C", True]
    ],
    [["8", "S", True]],
    [["8", "H", True]],
    [],
    [
        ["K", "D", True],
        ["5", "C", True]
    ],
    [],
    [["9", "S", True]]
] 


running = True  # กำหนดให้เกมทำงาน

while running:  # วนลูปหลักของเกม

    # ==================== รับเหตุการณ์ ====================

    for event in pygame.event.get():  # รับเหตุการณ์จากผู้เล่น

        if event.type == pygame.QUIT:  # หากกดปิดหน้าต่าง
            running = False  # หยุดเกม

        elif event.type == pygame.MOUSEBUTTONDOWN:  # หากกดปุ่มเมาส์

            if event.button != 1:  # หากไม่ใช่คลิกซ้าย
                continue  # ข้ามเหตุการณ์

            mouse_x, mouse_y = event.pos  # อ่านตำแหน่งเมาส์

            if game_over or game_won:  # หากเกมจบแล้ว

                if play_again_rect.collidepoint(
                    mouse_x, mouse_y
                ):  # หากกดปุ่ม Play Again
                    restart_game()  # เริ่มเกมใหม่

                continue  # ไม่รับการคลิกส่วนอื่น

            if restart_rect.collidepoint(mouse_x, mouse_y):
                restart_game()  # เริ่มเกมใหม่เมื่อกด Restart
                continue

            selected_pile = None  # ล้างกองที่เลือก
            selected_index = None  # ล้างตำแหน่งไพ่ที่เลือก
            dragging = False  # ยกเลิกการลากเดิม

            if not hint_rect.collidepoint(mouse_x, mouse_y):
                hint_move = None  # ล้างกรอบคำใบ้
                hint_message = ""  # ล้างข้อความคำใบ้

            # ==================== กดปุ่ม Hint ====================

            if hint_rect.collidepoint(mouse_x, mouse_y):

                hint_move = find_hint()  # ค้นหาการย้ายไพ่
                hint_start_time = pygame.time.get_ticks()  # เริ่มจับเวลาคำใบ้

                if hint_move is None:  # หากไม่พบการย้าย

                    if len(extra_cards) == 0:  # หากไพ่สำรองหมด
                        game_over = True  # กำหนดสถานะแพ้
                        hint_message = ""  # ล้างข้อความ
                    else:
                        hint_message = "NO MOVES - TRY STOCK"  # แจ้งให้ใช้ไพ่สำรอง
                        hint_message_time = pygame.time.get_ticks()  # เริ่มเวลาแจ้งเตือน
                else:
                    hint_message = ""  # ล้างข้อความหากพบคำใบ้

                continue

            # ==================== กดไพ่สำรอง ====================

            if stock_rect.collidepoint(mouse_x, mouse_y):

                if len(extra_cards) > 0:  # หากยังมีไพ่สำรอง

                    for i in range(3):  # แจกให้สามกองแรก

                        if len(extra_cards) > 0:  # หากยังมีไพ่เหลือ

                            card = extra_cards.pop()  # หยิบไพ่สำรอง
                            card[2] = True  # หงายไพ่
                            piles[i].append(card)  # เพิ่มไพ่ลงกอง

                    move_count += 1  # นับการแจกเป็นหนึ่งครั้ง

                continue

            # ==================== เลือกไพ่ ====================

            for i in range(7):  # ตรวจทุกกองไพ่

                pile = piles[i]  # เลือกกอง
                x = get_pile_x(i)  # หาตำแหน่ง X

                for j in range(len(pile) - 1, -1, -1):  # ตรวจไพ่จากบนลงล่าง

                    y = get_card_y(i, j)  # หาตำแหน่ง Y

                    if j == len(pile) - 1:  # หากเป็นไพ่ใบบนสุด
                        height = CARD_HEIGHT  # ใช้ความสูงเต็มใบ
                    else:
                        next_y = get_card_y(i, j + 1)  # ตำแหน่งไพ่ถัดไป
                        height = max(1, next_y - y)  # พื้นที่คลิกที่มองเห็น

                    card_rect = pygame.Rect(
                        x, y, CARD_WIDTH, height
                    )  # สร้างพื้นที่ตรวจการคลิก

                    if card_rect.collidepoint(mouse_x, mouse_y):  # หากคลิกโดนไพ่

                        if pile[j][2]:  # หากไพ่หงายหน้า

                            selected_pile = i  # เก็บกองต้นทาง
                            selected_index = j  # เก็บตำแหน่งไพ่
                            dragging = True  # เริ่มลากไพ่

                            offset_x = mouse_x - x  # ระยะเมาส์แนวนอน
                            offset_y = mouse_y - y  # ระยะเมาส์แนวตั้ง

                        break  # หยุดตรวจไพ่ในกอง

                if selected_pile is not None:  # หากเลือกไพ่ได้
                    break  # หยุดตรวจกองอื่น

        # ==================== ปล่อยไพ่ ====================

        elif event.type == pygame.MOUSEBUTTONUP:  # หากปล่อยปุ่มเมาส์

            if event.button == 1 and dragging:  # หากปล่อยคลิกซ้ายขณะลาก

                if not game_won and not game_over:  # หากเกมยังไม่จบ

                    mouse_x, mouse_y = event.pos  # อ่านตำแหน่งปล่อยเมาส์

                    moving_cards = piles[
                        selected_pile
                    ][selected_index:]  # เลือกไพ่ตั้งแต่ใบที่ลากถึงใบบนสุด

                    for i in range(7):  # ตรวจทุกกองปลายทาง

                        x = get_pile_x(i)  # หาตำแหน่ง X ของกอง

                        drop_rect = pygame.Rect(
                            x, PILE_START_Y,
                            CARD_WIDTH, HEIGHT - PILE_START_Y
                        )  # กำหนดพื้นที่ปล่อยไพ่

                        if drop_rect.collidepoint(mouse_x, mouse_y):  # หากปล่อยในกองนี้

                            if i != selected_pile:  # หากไม่ใช่กองเดิม

                                if can_place(
                                    moving_cards[0], piles[i]
                                ):  # หากวางไพ่ถูกกติกา

                                    piles[i].extend(moving_cards)  # ย้ายไพ่ไปกองปลายทาง

                                    del piles[
                                        selected_pile
                                    ][selected_index:]  # ลบไพ่จากกองต้นทาง

                                    move_count += 1  # เพิ่มจำนวนครั้งที่ย้าย

                                    if piles[selected_pile]:  # หากกองเดิมยังมีไพ่
                                        piles[selected_pile][-1][2] = True  # เปิดไพ่ใบบนสุด

                            break  # หยุดตรวจปลายทาง

                dragging = False  # หยุดลากไพ่
                selected_pile = None  # ล้างกองที่เลือก
                selected_index = None  # ล้างตำแหน่งไพ่

    # ==================== ตรวจสถานะเกม ====================

    if not dragging and not game_won and not game_over:
        collect_completed_sets()  # ตรวจชุดไพ่สำเร็จ

    if not game_won and not game_over:  # หากเกมยังดำเนินอยู่

        elapsed_seconds = (
            pygame.time.get_ticks() - start_ticks
        ) // 1000  # คำนวณเวลาที่เล่น

        score = max(
            0,
            10000 - elapsed_seconds * 2 - move_count * 20
        )  # คำนวณคะแนนตามเวลาและจำนวนครั้งที่ย้าย

        if len(completed_sets) == 4:  # หากเรียงครบสี่ชุด
            game_won = True  # ชนะเกม

        elif check_game_over():  # หากไม่มีการย้ายที่ Hint ยอมรับและ Stock หมด
            game_over = True  # แพ้เกม

    if hint_move is not None:  # หากกำลังแสดงคำใบ้

        if (
            pygame.time.get_ticks() - hint_start_time
            >= hint_duration
        ):  # หากครบเวลาแสดงคำใบ้
            hint_move = None  # ซ่อนคำใบ้

    # ==================== วาดหน้าจอ ====================

    screen.fill((30, 100, 60))  # ระบายพื้นหลังสีเขียว

    draw_button(
        restart_rect, "Restart", (240, 240, 240)
    )  # วาดปุ่ม Restart

    draw_button(
        hint_rect, "Hint", (255, 210, 70)
    )  # วาดปุ่ม Hint

    minutes = elapsed_seconds // 60  # คำนวณนาที
    seconds = elapsed_seconds % 60  # คำนวณวินาที

    status_text = status_font.render(
        f"Score: {score}    "
        f"Time: {minutes:02d}:{seconds:02d}    "
        f"Moves: {move_count}",
        True,
        (255, 255, 255)
    )  # สร้างข้อความคะแนน เวลา และจำนวนครั้งที่ย้าย

    screen.blit(status_text, (40, 160))  # แสดงสถานะเกม

    # ==================== วาดช่องชุดไพ่สำเร็จ ====================

    for i in range(4):  # วาดช่องเก็บไพ่ 4 ช่อง

        x = 530 + i * 110  # ตำแหน่ง X ของช่อง
        slot = pygame.Rect(
            x, 15, CARD_WIDTH, CARD_HEIGHT
        )  # กำหนดพื้นที่ช่อง

        if i < len(completed_sets):  # หากมีชุดไพ่สำเร็จ

            suit = completed_sets[i][0][1]  # อ่านดอกไพ่

            screen.blit(
                card_images[("K", suit)], slot.topleft
            )  # แสดงไพ่ K แทนชุดสำเร็จ

        else:  # หากช่องยังว่าง

            pygame.draw.rect(
                screen, (20, 75, 45),
                slot, border_radius=8
            )  # วาดช่องว่าง

            text_surface = font.render(
                "K - A", True, (200, 200, 200)
            )  # สร้างข้อความ K - A

            screen.blit(
                text_surface, (x + 20, 70)
            )  # แสดงข้อความในช่อง

        pygame.draw.rect(
            screen, (200, 200, 200),
            slot, 2, border_radius=8
        )  # วาดขอบช่อง

    # ==================== วาดกองไพ่ ====================

    for i in range(7):  # วาดกองไพ่ทั้งเจ็ด

        pile = piles[i]  # เลือกกองไพ่

        for j in range(len(pile)):  # วาดไพ่ทุกใบ

            if dragging and selected_pile == i:  # หากลากไพ่จากกองนี้
                if j >= selected_index:  # หากเป็นไพ่ที่ลาก
                    continue  # ไม่วาดที่เดิม

            card = pile[j]  # อ่านข้อมูลไพ่
            x = get_pile_x(i)  # ตำแหน่ง X
            y = get_card_y(i, j)  # ตำแหน่ง Y แบบปรับระยะอัตโนมัติ

            if card[2]:  # หากไพ่หงายหน้า
                image = card_images[(card[0], card[1])]  # ใช้รูปหน้าไพ่
            else:
                image = back_image  # ใช้รูปหลังไพ่

            screen.blit(image, (x, y))  # วาดไพ่บนหน้าจอ

    # ==================== วาดคำใบ้ ====================

    if hint_move is not None and not dragging:  # หากมีคำใบ้และไม่ได้ลากไพ่

        source_i, card_j, dest_i = hint_move  # แยกตำแหน่งคำใบ้

        source_x = get_pile_x(source_i)  # ตำแหน่ง X ของไพ่ต้นทาง
        source_y = get_card_y(source_i, card_j)  # ตำแหน่ง Y ของไพ่ต้นทาง

        pygame.draw.rect(
            screen, (255, 255, 0),
            (source_x, source_y, CARD_WIDTH, CARD_HEIGHT), 5
        )  # วาดกรอบสีเหลืองที่ไพ่ต้นทาง

        dest_x = get_pile_x(dest_i)  # ตำแหน่ง X ของกองปลายทาง

        if len(piles[dest_i]) > 0:  # หากกองปลายทางมีไพ่
            dest_y = get_card_y(
                dest_i, len(piles[dest_i]) - 1
            )  # ตำแหน่งไพ่ใบบนสุด
        else:
            dest_y = PILE_START_Y  # ตำแหน่งเมื่อกองว่าง

        pygame.draw.rect(
            screen, (0, 255, 255),
            (dest_x, dest_y, CARD_WIDTH, CARD_HEIGHT), 5
        )  # วาดกรอบสีฟ้าที่กองปลายทาง

    # ==================== วาดกองไพ่สำรอง ====================

    if len(extra_cards) > 0:  # หากยังมีไพ่สำรอง

        screen.blit(
            back_image, stock_rect.topleft
        )  # แสดงรูปหลังไพ่

    else:  # หากไพ่สำรองหมด

        pygame.draw.rect(
            screen, (20, 75, 45),
            stock_rect, border_radius=8
        )  # วาดช่องสำรองว่าง

    pygame.draw.rect(
        screen, (200, 200, 200),
        stock_rect, 2, border_radius=8
    )  # วาดขอบกองสำรอง

    stock_text = font.render(
        "Stock: " + str(len(extra_cards)),
        True, (255, 255, 255)
    )  # สร้างข้อความจำนวนไพ่สำรอง

    screen.blit(stock_text, (155, 70))  # แสดงจำนวนไพ่สำรอง

    # ==================== วาดไพ่ขณะลาก ====================

    if dragging:  # หากกำลังลากไพ่

        mouse_x, mouse_y = pygame.mouse.get_pos()  # อ่านตำแหน่งเมาส์

        moving_cards = piles[
            selected_pile
        ][selected_index:]  # เลือกกลุ่มไพ่ที่กำลังลาก

        drag_spacing = get_card_spacing(
            len(moving_cards)
        )  # คำนวณระยะห่างของไพ่ที่ลาก

        group_height = (
            (len(moving_cards) - 1) * drag_spacing
            + CARD_HEIGHT
        )  # คำนวณความสูงรวมของกลุ่มไพ่

        drag_x = mouse_x - offset_x  # ตำแหน่ง X ขณะลาก
        drag_y = mouse_y - offset_y  # ตำแหน่ง Y ขณะลาก

        drag_y = max(
            0, min(drag_y, HEIGHT - group_height)
        )  # จำกัดไม่ให้ไพ่เลยขอบบนหรือล่าง

        for j in range(len(moving_cards)):  # วาดไพ่ทุกใบที่ลาก

            card = moving_cards[j]  # อ่านข้อมูลไพ่

            x = int(drag_x)  # ตำแหน่ง X
            y = int(drag_y + j * drag_spacing)  # ตำแหน่ง Y

            rect = pygame.Rect(
                x, y, CARD_WIDTH, CARD_HEIGHT
            )  # สร้างกรอบไพ่

            image = card_images[(card[0], card[1])]  # เลือกรูปไพ่

            screen.blit(image, (x, y))  # วาดไพ่ตามเมาส์

            pygame.draw.rect(
                screen, (255, 220, 0), rect, 3
            )  # วาดกรอบสีเหลืองรอบไพ่ที่ลาก

    # ==================== แสดงข้อความ Hint ====================

    if hint_message != "" and not game_over:  # หากมีข้อความแจ้งเตือน

        current_time = pygame.time.get_ticks()  # อ่านเวลาปัจจุบัน

        if current_time - hint_message_time < 2000:  # แสดงไม่เกิน 2 วินาที

            message_box = pygame.Rect(
                250, 400, 500, 150
            )  # กำหนดพื้นที่ข้อความ

            pygame.draw.rect(
                screen, (30, 40, 40),
                message_box, border_radius=12
            )  # วาดพื้นหลังกล่องข้อความ

            pygame.draw.rect(
                screen, (255, 80, 80),
                message_box, 3, border_radius=12
            )  # วาดขอบสีแดง

            message_text = font.render(
                hint_message, True, (255, 255, 255)
            )  # สร้างข้อความแจ้งเตือน

            screen.blit(
                message_text,
                message_text.get_rect(center=message_box.center)
            )  # แสดงข้อความกลางกล่อง

        else:
            hint_message = ""  # ล้างข้อความเมื่อครบเวลา

    # ==================== แสดงหน้าสรุปผล ====================

    if game_over or game_won:  # หากเกมชนะหรือแพ้
        draw_game_result()  # แสดงคะแนน เวลา และจำนวนครั้งที่ย้าย

    pygame.display.flip()  # อัปเดตหน้าจอเกม
    clock.tick(60)  # จำกัดความเร็วที่ 60 FPS

pygame.quit()  # ปิดการทำงานของ Pygame