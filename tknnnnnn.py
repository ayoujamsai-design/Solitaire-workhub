import random  #แจกไพ่แบบสุ่ม

suits = ["S", "H", "D", "C"]
ranks = ["A", "2", "3", "4", "5", "6", "7",
"8", "9", "10", "J", "Q", "K"]

deck = []  #สร้าง list ว่างเพื่อเก็บไพ่ทั้งหมด

for suit in suits:  #สร้างไพ่ทั้งหมด 52 ใบ
    for rank in ranks:
        card = [rank, suit]   #เอาไพ่แต่ละใบใส่ใน list
        deck.append(card)  #เอาไพ่แต่ละใบใส่ใน list deck
        
random.shuffle(deck)  #สับไพ่แบบสุ่ม

print("Deck of cards:",deck)





        







