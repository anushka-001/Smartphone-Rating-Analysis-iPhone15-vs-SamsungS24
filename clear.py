import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Ensure seaborn is set up for nicer plots
sns.set(style="whitegrid")

def load_data(file_path, product_name):
    # Load the data, assuming ratings are stored in a column named 'Rating'
    df = pd.read_excel(file_path)
    # Convert the ratings to numeric values, assuming they're in a format like '5 out of 5 stars'
    df['Rating'] = df['Rating'].str.extract(r'(\d+(?:\.\d+)?)')[0].astype(float)
    # Add a column to label the product
    df['Product'] = product_name
    return df

# Load and clean the data for both products
df_iphone = load_data('output_iphone.xlsx', 'iPhone 15')
df_samsung = load_data('output_samsung.xlsx', 'Samsung S24')

# Combine the DataFrames for plotting
df_combined = pd.concat([df_iphone, df_samsung])

# Create a more informative plot, such as a violin plot
plt.figure(figsize=(10, 6))
sns.violinplot(x='Product', y='Rating', data=df_combined, palette="muted", split=True, inner="quart", linewidth=1.5)
sns.swarmplot(x='Product', y='Rating', data=df_combined, color='k', alpha=0.6)  # Adds individual points on top

plt.title('Rating Distribution: iPhone 15 vs Samsung S24')
plt.ylabel('Rating')
plt.xlabel('Product')
plt.show()
