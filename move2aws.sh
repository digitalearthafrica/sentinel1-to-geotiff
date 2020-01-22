#!/usr/bin/env bash

aws s3 sync /g/data/dz56/ga/ga_s1a_c_ard/1-0-0/Copernicus_Backscatter_repro_cog/ s3://test-odc-conf/Copernicus_Backscatter_repro_cog/
aws s3 cp s1a_gamma0_scene.yaml s3://test-odc-conf/nbar-scenes-tmp-cog/s1a_gamma0_scene.yaml
