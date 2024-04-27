import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
def load_data(filepath):
    df = pd.read_excel(filepath)
    # Make sure 'Rating' column is in numeric format, e.g., as "5.0"
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    return df.dropna(subset=['Rating'])  # Drop rows where Rating could not be turned into a number

# Load both datasets
df_iphone = load_data('output_iphone.xlsx')
df_samsung = load_data('output_samsung.xlsx')

# Calculate average and standard deviation for both sets
avg_rating_iphone = df_iphone['Rating'].mean()
std_rating_iphone = df_iphone['Rating'].std()
avg_rating_samsung = df_samsung['Rating'].mean()
std_rating_samsung = df_samsung['Rating'].std()

# Create a DataFrame for the plot
df_plot = pd.DataFrame({
    'Product': ['iPhone 15', 'Samsung S24'],
    'Average Rating': [avg_rating_iphone, avg_rating_samsung],
    'Standard Deviation': [std_rating_iphone, std_rating_samsung]
})

# Set up the seaborn plot
sns.set_style('whitegrid')

# Create a barplot
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='Product', y='Average Rating', yerr=df_plot['Standard Deviation'], data=df_plot, capsize=.1)
plt.title('Average Rating Comparison with Standard Deviation')
plt.ylabel('Average Rating')
plt.xlabel('Product')

# Display the plot
plt.show()
