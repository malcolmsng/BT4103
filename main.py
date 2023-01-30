#Hello World
#all functions to be executed here
#trying stuff out
import pandas as pd

sample_data = pd.read_csv("./data/sample_data.csv", skiprows= 1)
df = pd.DataFrame(sample_data)
print(df.head())