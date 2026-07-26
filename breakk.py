marks = {
    "phy" : 52,
    "math" : 45,
    "bio" : 56,
    "soc" : 78
}

for subject, score  in marks.items():
    if score   <= 50:
        print(f"failed in : {subject} ({score})")
        break 
    print(f"passed : {subject} ({score})")
print("check complete")