import pygame #นำเข้าpygame
import random  #แจกไพ่แบบสุ่ม

pygame.init()

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Solitaire")

font = pygame.font.Font(None, 30)
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

#print("Deck of cards:",deck) test

piles = [[],[],[],[],[],[],[]]  #สร้าง list ว่างเพื่อเก็บกองไพ่ 7 กอง

for i in range(7): #  7 กอง
    for j in range(7): #แจก 7 ใบ
        card = deck.pop()  #แจกไพ่ให้กองละ 7 ใบ โดยเอาไพ่จาก deck ออกไป
        
        if i < 7 and j < 3:  #ไพ่กองที่ 1-3 ใบที่ 1-3 คว่ำหน้า
            card[2] = False  # False แสดงว่าไพ่คว่ำหน้า card = [rank, suit, True] ตน.2
        else:
            card[2] = True  # True แสดงว่าไพ่หงายหน้า
            
        piles[i].append(card)  #เอาไพ่แต่ละใบใส่ในกองไพ่แต่ละกอง
        
extra_cards = deck  #ไพ่ที่เหลือจากการแจกไพ่ 7 กอง
    
#print("Piles of cards:",piles) test
for i in range(7): #แสดงกองไพ่ 7 กอง
    print("pile",i + 1,":",piles[i])  #แสดงกองไพ่แต่ละกอง
    
print("Extra cards:",extra_cards)  #แสดงไพ่ที่เหลือจากการแจกไพ่ 7 กอง

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

print("จำนวนไพ่หงาย:", count_face_up_cards(1))

def can_place(card, destination):
    # กองว่างวางได้เฉพาะ K
    if len(destination) == 0:
        return card[0] == "K"

    # ไพ่ใบสุดท้ายของกองปลายทาง
    top_card = destination[-1]

    # ไพ่ปลายทางต้องหงายหน้า
    if top_card[2] == False:
        return False

    # ต้องเป็นดอกเดียวกัน
    if card[1] != top_card[1]:
        return False

    # ไพ่ที่ย้ายต้องมีแต้มน้อยกว่าปลายทาง 1
    card_value = ranks.index(card[0])
    top_value = ranks.index(top_card[0])

    return card_value + 1 == top_value

running = True

while running:
    #รับเหตุการณ์
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 100, 60))  #พื้นหลังโต๊ะสีเขียว

    # ช่องเก็บไพ่ครบชุด 4 ช่อง ขวาบน
    for i in range(4):
        x = 530 + i * 110
        slot = pygame.Rect(x, 15, 100, 140)

        pygame.draw.rect(
            screen, (20, 75, 45), slot, border_radius=8
        )
        pygame.draw.rect(
            screen, (200, 200, 200), slot, 2, border_radius=8
        )

        text = font.render("K - A", True, (200, 200, 200))
        screen.blit(text, (x + 20, 70))

    # วาดไพ่ทั้ง 7 กอง
    for i in range(7):
        pile = piles[i]

        for j in range(len(pile)):
            card = pile[j]

            x = 40 + i * 135  #ตำแหน่งแนวนอนของแต่ละกอง
            y = 180 + j * 45  #วางไพ่ซ้อนกันลงมา
            rect = pygame.Rect(x, y, 100, 140)

            if card[2] == True:
                #ไพ่หงาย
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
                #ไพ่คว่ำ
                pygame.draw.rect(screen, (50, 70, 160), rect)

            #เส้นขอบไพ่
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

    #แสดงจำนวนไพ่สำรอง
    text = font.render(
        "Extra cards: " + str(len(extra_cards)),
        True,
        (255, 255, 255)
    )
    screen.blit(text, (40, 30))

    pygame.display.flip()  #อัปเดตภาพบนหน้าจอ
    clock.tick(60)         #จำกัดไว้ที่ 60 เฟรมต่อวินาที

pygame.quit()





        







