#This code is used to calculate the attribution analysis section in the article.

import numpy as np
import pandas as pd
from osgeo import gdal
from tqdm import tqdm
from sklearn.decomposition import PCA

gdal.DontUseExceptions()

start_year = 2003
end_year = 2020

for year in range(start_year, end_year):
    next_year = year + 1

    fraction_data = fraction_data
    data = np.load(fraction_data)

    attribution_dataset = gdal.Open( attribution_dataset)
   attribution_array = attribution_dataset.ReadAsArray()
    landuse_tif = CLCD
    landuse_array = np.load(landuse_tif)
    valid_landuse_values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    
    pca_analysis = PCA(n_components=0.99)

    valid_cells = data[0, :, :] <= 0.95
    lat_indices, lon_indices = np.where(valid_cells)

    df = pd.DataFrame({
        'lat_index': lat_indices,
        'lon_index': lon_indices,
        'delta': attribution_array[lat_indices, lon_indices]
    })

    for idx, (lat_index, lon_index) in tqdm(enumerate(zip(lat_indices, lon_indices)), total=len(lat_indices)):
        if (2 <= lat_index <attribution_array.shape[0] - 2) and (2 <= lon_index <attribution_array.shape[1] - 2):
            local_ attribution = attribution_array[lat_index - 2:lat_index + 3, lon_index - 2:lon_index + 3].reshape(25, )
            local_data = data[:, lat_index - 2:lat_index + 3, lon_index - 2:lon_index + 3].reshape(16, 25).T

            local_landuse = landuse_array[:, lat_index - 2:lat_index + 3, lon_index - 2:lon_index + 3]
            mean_landuse_proportions = local_landuse.mean(axis=(1, 2))

            for landuse_type in range(9):
                df.at[idx, f'landuse_{landuse_type+1}_mean'] = mean_landuse_proportions[landuse_type]

            if np.linalg.matrix_rank(local_data) != 0:
                X_centered = local_data - local_data.mean(axis=0)

                U, D, Vt = np.linalg.svd(X_centered, full_matrices=False)
                V_z = Vt.T

                Z = X_centered.dot(V_z)

                Z_augmented = np.hstack((np.ones((Z.shape[0], 1)), Z))
                try:
                    Coefficient = np.linalg.inv(Z_augmented.T.dot(Z_augmented)).dot(Z_augmented.T).dot(local_ attribution)
                except np.linalg.LinAlgError:
                    continue

                for veg_type in range(0, 16):
                    fraction = data[veg_type, lat_index, lon_index]
                    if fraction == 0:
                        df.at[idx, f'{veg_type}E'] = 0
                    else:
                        P_array = np.zeros((25, 16))
                        P_array[12, veg_type] = 1
                        M_array = P_array - local_data.mean(axis=0)
                        Zp = M_array.dot(V_z)
                        Zp_augmented = np.hstack((np.ones((Zp.shape[0], 1)), Zp))
                        Yp = Zp_augmented.dot(Coefficient)
                        df.at[idx, f'{veg_type}E'] = Yp[12]

                    df.at[idx, f'{veg_type}f%'] = fraction

                df.at[idx, 'mean'] = local_ attribution.mean()

    output_file =output
    df.to_excel(output_file, index=False)
