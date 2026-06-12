print("===BILL SPLITTER===")
Bill=float(input("Enter the bill amount:"))
People=int(input("Enter the number of people:"))
print("1: 10%")
print("2: 15%")
print("3: 20%")
print("4: Custom")
choice=input("Choose an option(1-4):")
if choice=="1":
    Tip=10
elif choice=="2":
    Tip=15
elif choice=="3":
    Tip=20
elif choice=="4":
    Tip=float(input("Enter custom tip percentage:"))
else:
    print("Invalid choice")
    exit()
tip_amount=float(Tip/100*Bill)
Total=float(Bill+tip_amount)
Amount=float(Total/People)
print("=" *35)
print("RECEIPT SUMMARY")
print("=" *35)
print(f"Bill Amount: {Bill:.2f}")
print(f"Tip Amount: {tip_amount:.2f}")
print(f"Total Amount: {Total:.2f}")
print(f"Amount per Person: {Amount:.2f}")