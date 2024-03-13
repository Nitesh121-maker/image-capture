import pandas as pd
import numpy as np

# Create a DataFrame with random data
data = pd.DataFrame(np.random.randn(1000000, 10), columns=[f'Column_{i}' for i in range(10)])

# Save the DataFrame to an XLSX file
data.to_excel('sample_data_one.xlsx', index=False)

print("Trade data saved to trade_data.xlsx")