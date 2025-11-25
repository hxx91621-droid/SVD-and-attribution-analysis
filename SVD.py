#This code is used to compute the SVD section in the article.
import numpy as np
import pandas as pd
from osgeo import gdal
from tqdm import tqdm
from sklearn.decomposition import PCA

gdal.DontUseExceptions()

fraction_data = yearly crop data
data = np.load(fraction_data)
LST_dataset = gdal.Open(yearly LST data)
LST_array = LST_dataset.ReadAsArray()

pca_analysis = PCA(n_components=0.99)

valid_cells = data[0, :, :] <= 0.9
lat_indices, lon_indices = np.where(valid_cells)

df = pd.DataFrame({
    'lat_index': lat_indices,
    'lon_index': lon_indices,
    'LST_value': LST_array[lat_indices, lon_indices]
})

for idx, (lat_index, lon_index) in tqdm(enumerate(zip(lat_indices, lon_indices)), total=len(lat_indices)):
    if (2 <= lat_index < LST_array.shape[0] - 2) and (2 <= lon_index < LST_array.shape[1] - 2):
        local_LST = LST_array[lat_index - 2:lat_index + 3, lon_index - 2:lon_index + 3].reshape(25, )
        local_data = data[:, lat_index - 2:lat_index + 3, lon_index - 2:lon_index + 3].reshape(16, 25).T

        if np.linalg.matrix_rank(local_data) != 0:
            normalized_data = local_data - local_data.mean(axis=0)
            Z_array = pca_analysis.fit_transform(normalized_data)
            try:
                Coefficient = np.linalg.inv(Z_array.T @ Z_array) @ Z_array.T @ local_LST
                
                P_array_open = np.zeros((25, 16))
                P_array_open[12:, 0] = 1
                Zp_array_open = pca_analysis.transform(P_array_open - local_data.mean(axis=0))
                Yp_array_open = Zp_array_open @ Coefficient

                for veg_type in range(0, 16):
                    P_array_veg = np.zeros((25, 16))
                    P_array_veg[12:, veg_type] = 1
                    Zp_array_veg = pca_analysis.transform(P_array_veg - local_data.mean(axis=0))
                    Yp_array_veg = Zp_array_veg @ Coefficient

                    temp_diff = Yp_array_veg[24] - Yp_array_open[24]
                    df.at[idx, f'{veg_type}E'] = temp_diff
                    df.at[idx, f'{veg_type}f%'] = data[veg_type, lat_index, lon_index]
            except np.linalg.LinAlgError:
                df.at[idx, f'{veg_type}E'] = 0

output_file = output data
df.to_csv(output_file, index=False)


