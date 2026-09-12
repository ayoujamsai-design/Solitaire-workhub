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
        
        if i < 3 and j < 3:  #ไพ่กองที่ 1-3 ใบที่ 1-3 หงายหน้า
            card[2] = False  # False แสดงว่าไพ่คว่ำหน้า card = [rank, suit, True] ตน.2
        else:
            card[2] = True  # True แสดงว่าไพ่หงายหน้า
            
        piles[i].append(card)  #เอาไพ่แต่ละใบใส่ในกองไพ่แต่ละกอง
        
extra_cards = deck  #ไพ่ที่เหลือจากการแจกไพ่ 7 กอง
    
#print("Piles of cards:",piles) test
for i in range(7): #แสดงกองไพ่ 7 กอง
    print("pile",i + 1,":",piles[i])  #แสดงกองไพ่แต่ละกอง
    
print("Extra cards:",extra_cards)  #แสดงไพ่ที่เหลือจากการแจกไพ่ 7 กอง





        







