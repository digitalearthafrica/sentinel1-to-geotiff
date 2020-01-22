#!/usr/bin/env python3

import subprocess
from os.path import join, isdir
from os import makedirs
import sys
import time
import yaml
import os


def cmdrun(cmd):
    print(cmd)
    push = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    if not push.returncode == 0:
        raise RuntimeError(cmd)
    return push


split_dir = 'Copernicus_Backscatter_repro'
split_tag = '_cog'
img_files_base = ['Gamma0_VV', 'Gamma0_VH']


def cog_img(in_path, out_path):
    """
    Given a path to an image file cog it and save the output file.
    Note: a .img file also needs a .hdr file!
    :param in_path: The image file.
    :param out_path: The output file.
    :return:
    """
    """
    This is an example of the bash I'm implimenting
    gdal_translate Gamma0_VH.img Gamma0_VH_V4.tif 
        -co TILED=YES -co COMPRESS=DEFLATE
    gdaladdo -r average Gamma0_VH_V4.tif 2 4 8 16 32
    gdal_translate Gamma0_VH_V4.tif Gamma0_VH_V4_cog.tif
        -co TILED=YES -co COMPRESS=DEFLATE -co COPY_SRC_OVERVIEWS=YES
        -co BLOCKXSIZE=512 -co BLOCKYSIZE=512
        --config GDAL_TIFF_OVR_BLOCKSIZE 512
    rm  Gamma0_VH_V4.tif
    """
    tmp_path = out_path + '.tmp'
    cmd = 'gdal_translate ' + in_path + ' ' + tmp_path
    cmd += ' -co TILED=YES -co COMPRESS=DEFLATE'
    cmdrun(cmd)

    cmd = 'gdaladdo -r average ' + tmp_path + ' 2 4 8 16 32'
    cmdrun(cmd)

    cmd = 'gdal_translate ' + tmp_path + ' ' + out_path
    cmd += ' -co TILED=YES -co COMPRESS=DEFLATE '
    cmd += '-co COPY_SRC_OVERVIEWS=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 '
    cmd += '--config GDAL_TIFF_OVR_BLOCKSIZE 512'
    cmdrun(cmd)

    cmdrun('rm ' + tmp_path)


def create_data_dir_yaml(in_path):
    """
    given a location of a .data dir
    copy the dir over to a new dir,
      with backscatter_repro> backscatter_repro_cog

    copy and update the scene .yaml at the same level over,

    COG the two .img files;
    Gamma0_VH.img
    Gamma0_VV.img

    """

    start_time = time.time()

    new_dir = split_dir + split_tag
    out_path = in_path.replace(split_dir, new_dir)
    assert new_dir in out_path
    print (out_path)

    # create_data_dir
    if not isdir(out_path):
        makedirs(out_path)

    # update the yaml file and move it over
    assert in_path[-5:] == '.data'
    src = in_path[:-5] + '.yaml'
    dst = out_path[:-5] + '.yaml'
    update_yaml(src, dst)

    # COG the files
    for img_file_base in img_files_base:
        cog_in_path = join(in_path, img_file_base + '.img')
        cog_out_path = join(out_path, img_file_base + '.tif')
        cog_img(cog_in_path, cog_out_path)

    delta = time.time() - start_time
    print("--- %s.2f seconds ---" % delta)


def update_yaml(in_yaml_path, out_yaml_path):
    """
    Modify the yaml file to take into account the COGing and
    the different file location.

    :param in_yaml_path:
    :param out_yaml_path:
    :return:
    """
    with open(in_yaml_path) as f:
        yamdoc = yaml.load(f)

    yamdoc['format']['name'] = 'GeoTiff'

    # fix the band paths, from absolute to relative
    for band in ['vh', 'vv']:
        ab_vh = yamdoc['image']['bands'][band]['path']
        ab_list = ab_vh.split(os.sep)
        rel = join('.', ab_list[-2], ab_list[-1])

        # Fix the file type
        if rel[-3:] == 'img':
            rel = rel[:-3] + 'tif'
        yamdoc['image']['bands'][band]['path'] = rel

    with open(out_yaml_path, "w") as f:
        yaml.dump(yamdoc, f, default_flow_style=False)


if __name__ == '__main__':
    create_data_dir_yaml(sys.argv[1])