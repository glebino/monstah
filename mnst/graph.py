import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import xlrd

graph = pd.read_excel("./output/monthly_statistics.xlsx")
sns.load_dataset("titanic")
g = sns.factorplot(x="Visits", col="Client", data
=graph, kind="bar", palette="muted", legend=False)

#plt.show()
plt.savefig('test2.png')