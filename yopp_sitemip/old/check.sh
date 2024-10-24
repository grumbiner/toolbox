#!/bin/sh --login
#SBATCH -J yopp201
#SBATCH -e yopp201.err
#SBATCH -o yopp201.out
#SBATCH -t 7:55:00
#  #SBATCH -t 0:29:00
#SBATCH -q batch
#SBATCH -A marine-cpu
#  #SBATCH -A fv3-cpu
#SBATCH -N 1
#SBATCH --mail-type FAIL
#SBATCH --mail-user USER@system

#-------------------------- Reference -------------------------------
#Arctic SOP1:
start=20180201
end=20180331

#Arctic SOP2:
start=20180701
end=20180930

#Antarctic SOP1:
start=20181116
end=20190215

#Mosaic:
start=20191001
end=20201012

#Antarctic SOP2:
start=20220415
end=20220831

#-------------------------- END Reference -------------------------------
module load hpss/hpss
module load hpc/1.2.0 intel/2022.1.2 hpc-intel/2022.1.2
module load impi/2022.1.2 hpc-impi/2022.1.2
module load hdf5/1.10.6 wgrib2/2.0.8 netcdf/4.7.0
. python_load
module list

export YDIR=$HOME/rgdev/toolbox/yopp_sitemip
export PYTHONPATH=$PYTHONPATH:$YDIR
export pid=$$
mkdir $HOME/scratch/yopp.$pid
cd $HOME/scratch/yopp.$pid
ln -s $YDIR/gpfs .
cp -p $YDIR/*.py .
cp -p $YDIR/*.csv .

#Arctic SOP1:
start=20180201
end=20180331

tag=$start

export YOPP_base=$HOME/clim_data/yopp

while [ $tag -le $end ]
do
  #######
  # do the extraction to .nc:

  for cyc in 00 06 12 18 
  do
    export YOPP_archive_dir=$YOPP_base/$cyc

    if [ ! -f $YOPP_archive_dir/ncep_gfs_sflux.$tag$cyc.tgz ] ; then
      echo missing ncep_gfs_sflux.$tag$cyc.tgz
    fi

    if [ ! -f $YOPP_archive_dir/ncep_gfs_pgrb.$tag$cyc.tgz ] ; then
      echo missing ncep_gfs_pgrb.$tag$cyc.tgz
    fi

    if [ ! -f $YOPP_archive_dir/ncep_gfs_pgrb_surf.$tag$cyc.tgz ] ; then
      echo missing ncep_gfs_pgrb_surf.$tag$cyc.tgz
    fi

  done

  tag=`expr $tag + 1`
  tag=`$HOME/bin/dtgfix3 $tag`
done
