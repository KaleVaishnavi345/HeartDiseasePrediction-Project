import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 1. Load your dataset (assuming it is 'heart.csv')
# If you don't have the csv yet, this will create a dummy one for the visual
try:
    df = pd.read_csv('heart.csv')
except:
    print("Dataset not found, generating sample visual...")
    import numpy as np
    data = np.random.rand(13, 13)
    columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
    df = pd.DataFrame(data, columns=columns)

# 2. Calculate Correlation
corr = df.corr()

# 3. Create Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Feature Correlation Heatmap')

# 4. Save to your static folder
save_path = 'frontend/static/images/correlation_heatmap.png'

# Create folder if it doesn't exist
os.makedirs(os.path.dirname(save_path), exist_ok=True)

plt.savefig(save_path)
print(f"Heatmap saved successfully at {save_path}")