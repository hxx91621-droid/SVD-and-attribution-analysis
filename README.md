SVD and Attribution Analysis
** 
This part of the code is used to implement SVD computation and the corresponding attribution analysis. The relevant data references are as follows:

📊 Data Sources
1. Crop Data
Considering potential inconsistencies among classification products, both maize and winter wheat maps were derived from a unified crop mapping dataset:
Maize map: https://doi.org/10.1038/s41597-023-02573-6 (Classification accuracy: 79.38%)
Winter wheat map: https://doi.org/10.6084/m9.figshare.12003990 (Classification accuracy: 91.17%)
Crop distribution data spanning 2003-2020 were extracted for the plain and reprojected to a sinusoidal equal-area projection to ensure consistency with the LST dataset.
2. LST Data
Employed a monthly mean LST dataset:
Source: https://zenodo.org/records/6618442
Key features: Global 1 km monthly LST (2003-2020), generated via multi-temporal weighted averaging
Accuracy: Root Mean Square Error (RMSE) = 1.60 K
Monthly LST values were averaged for each year within the study area to form a continuous annual LST record.
3. Attribution Data
3.1 Albedo Data (MCD43A3)
Source: https://ladsweb.modaps.eosdis.nasa.gov
Original specs: 500 m spatial resolution, 16-day composites (WSA/BSA)
Processing: Aggregated to annual means, resampled to 1 km (2×2 block averaging)
3.2 Downward Shortwave Radiation (DSR, GLASS)
Source: https://www.glass.hku.hk
Original specs: 0.05° spatial resolution, daily global coverage
Processing: Mapped 0.05° grids to 5×5 1 km pixels for annual DSR data (2003-2020)
3.3 Latent Heat Flux (LE, MOD16A3GF)
Source: https://lpdaac.usgs.gov
Original specs: 500 m spatial resolution, annual data (2003-2020)
Processing: Extracted 4 MODIS tiles (h26v04, h26v05, h27v04, h27v05), resampled to 1 km (2×2 block averaging)
3.4 Broadband Emissivity (BBE, GLASS)
Source: https://glass.hku.hk
Original specs: 1 km spatial resolution, 8-day temporal resolution
Processing: Aggregated to annual means to characterize yearly surface emissivity
4. Auxiliary Data (Cropland Reference)
Dataset: 30 m China Land Cover Dataset (CLCD)
Source: https://zenodo.org/records/12779975
Development: Derived from Landsat observations on Google Earth Engine (overall accuracy: 80%)
Purpose: Minimize the influence of non-crop areas on temperature effect estimates

