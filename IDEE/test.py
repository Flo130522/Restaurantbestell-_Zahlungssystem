import pandas as pd
df = pd.read_csv("speisekarte.csv",index_col=False)
df.set_index("ID", inplace=True)
print(df)
