import pandas as pd
df = pd.DataFrame([[1,2,3]], columns=["A","B","C"])
df.to_csv("test.csv", index=False)
print("test.csv created")