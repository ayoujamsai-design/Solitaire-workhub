import random  #แจกไพ่แบบสุ่ม

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
        
        if i < 3 and j < 3:  #ไพ่กองที่ 1-3 ใบที่ 1-3 คว่ำหน้า
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

    count = 0  # จำนวนไพ่หงาย
    i = 0      # ตำแหน่งไพ่ที่กำลังตรวจ

    while i < len(pile):
        card = pile[i]

        if card[2] == True:
            count += 1

        i += 1  # ไปตรวจใบถัดไป ทั้งไพ่หงายและไพ่คว่ำ

    return count


print("จำนวนไพ่หงาย:", count_face_up_cards(1))



        







