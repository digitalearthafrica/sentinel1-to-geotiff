#!/usr/bin/env bash
# find /g/data/dz56/ga/ ga_s1a_c_ard/1-0-0/Copernicus_Backscatter/Sentinel-1/C-SAR/GRD/2017/2017-12 -name '*.yaml' | xargs -n 1 -P 8 echo
find /g/data/dz56/ga/ga_s1a_c_ard/1-0-0/Copernicus_Backscatter_repro/Sentinel-1/C-SAR/GRD/2017/* -name '*.data' > work_list-all.txt
time cat work_list-all.txt|  xargs -n 1 -P 8 ./s1cog.py



# aws s3 cp Gamma0_VH.tif s3://test-odc-conf/Copernicus_Backscatter_repro_cog/Sentinel-1/C-SAR/GRD/2017/2017-09/40S145E-45S150E/S1A_IW_GRDH_1SDV_20170917T191718_20170917T191743_018419_01F035_5AF6.data/