import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sb

class PCA:
    def __init__(self, X):
        self.X = X
        self.Cov = np.cov(self.X, rowvar=False)
        self.eigenvalues, self.eigenvectors = np.linalg.eigh(self.Cov)
        k_desc = [k for k in reversed(np.argsort(self.eigenvalues))]
        self.alpha = self.eigenvalues[k_desc]
        self.a = self.eigenvectors[:, k_desc]
        self.C = self.X @ self.a
        self.Rxc = np.abs(self.a * np.sqrt(self.alpha))
        self.scores = self.C / np.sqrt(self.alpha)
        self.C2 = self.C * self.C
        C2SL = np.sum(self.C2, axis=1)
        self.quality = np.transpose(self.C2.T / C2SL)

    def getAlpha(self):
        return self.alpha
    def getA(self):
        return self.a
    def getPrinComp(self):
        return self.C
    def getFactorLoadings(self):
        return self.Rxc
    def getScores(self):
        return self.scores
    def getQualityOfPoints(self):
        return self.quality
    def getContributions(self):
        return self.C2 / (self.X.shape[0] * self.alpha)
    def getCommonalities(self):
        Rxc2 = np.square(self.Rxc)
        return np.cumsum(a=Rxc2, axis=1)
    def getCumulativeVariance(self):
        return np.cumsum(self.alpha) / np.sum(self.alpha)


# plotting functions
def correlogram(matrix=None, dec=2, title='Correlogram', valmin=-1, valmax=1):
    plt.figure(title, figsize=(18, 12))
    plt.title(title, fontsize=16, color='k', verticalalignment='bottom')
    sb.heatmap(data=np.round(matrix, dec), vmin=valmin, vmax=valmax, cmap='bwr', annot=True)

def principalComponents(eigenvalues=None, XLabel='Principal components', YLabel='Eigenvalues (variance)', title='Explained variance by the principal components'):
    plt.figure(title, figsize=(13, 8))
    plt.title(title, fontsize=14, color='k', verticalalignment='bottom')
    plt.xlabel(XLabel, fontsize=14, color='k', verticalalignment='top')
    plt.ylabel(YLabel, fontsize=14, color='k', verticalalignment='bottom')
    components = ['C'+str(j+1) for j in range(eigenvalues.shape[0])]
    plt.plot(components, eigenvalues, 'bo-')
    plt.axhline(y=1, color='r')


# load dataset
dataset = 'dataIN/EuropeHappiness.csv'
output_dir = './dataOUT/PCA'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

table = pd.read_csv(dataset)

non_numerical_columns = table.select_dtypes(include=['object']).columns
metadata = table[non_numerical_columns]
numerical_data = table.drop(columns=non_numerical_columns)

# scale the dataset
scaler = StandardScaler()
X_scaled = scaler.fit_transform(numerical_data.values)
X_scaled_df = pd.DataFrame(data=X_scaled, index=table.index, columns=numerical_data.columns)

# PCA model
pcaModel = PCA(X_scaled)
alpha = pcaModel.getAlpha()

# creating the graphic of eigenvalues
principalComponents(eigenvalues=alpha)
plt.savefig(os.path.join(output_dir, 'principal_components.png'))

# save the principal components
C = pcaModel.getPrinComp()
nameC = ['C'+str(j+1) for j in range(C.shape[1])]
C_df = pd.DataFrame(data=C, index=table.index, columns=nameC)
C_df.to_csv(os.path.join(output_dir, 'princComp.csv'))

# save factor loadings
factorLoadings = pcaModel.getFactorLoadings()
factorLoadings_df = pd.DataFrame(data=factorLoadings, index=numerical_data.columns, columns=nameC)
factorLoadings_df.to_csv(os.path.join(output_dir, 'factorLoadings.csv'))

# create correlogram
correlogram(matrix=factorLoadings_df, title='The correlation between the initial variables and principal components')
plt.savefig(os.path.join(output_dir, 'factor_loadings.png'))

# save scores
scores = pcaModel.getScores()
scores_df = pd.DataFrame(data=scores, index=table.index, columns=nameC)
scores_df.to_csv(os.path.join(output_dir, 'scores.csv'))

# save quality of points
qualityOfPoints = pcaModel.getQualityOfPoints()
qualityOfPoints_df = pd.DataFrame(data=qualityOfPoints, index=table.index, columns=nameC)
qualityOfPoints_df.to_csv(os.path.join(output_dir, 'quality.csv'))

# save commonalities
common = pcaModel.getCommonalities()
common_df = pd.DataFrame(data=common, index=numerical_data.columns, columns=nameC)
common_df.to_csv(os.path.join(output_dir, 'commonalities.csv'))

plt.show()
