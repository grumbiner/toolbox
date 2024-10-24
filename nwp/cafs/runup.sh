#!/bin/sh
#SBATCH -J nwp9_cafs
#SBATCH -e nwp9_cafs.err
#SBATCH -o nwp9_cafs.out
#SBATCH -t 7:55:00
#  #SBATCH -t 0:25:00
#SBATCH -q batch
#SBATCH -A marine-cpu
#  #SBATCH -A fv3-cpu
#SBATCH -N 1
#SBATCH --mail-type FAIL
#SBATCH --mail-user USER@system

# Path to cafs output:
export base=/home/Robert.Grumbine/clim_data/cafs/

# This must be more or less exactly this:
source /home/Robert.Grumbine/rgref/env3.12/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/Robert.Grumbine/rgdev/toolbox/nwp
# location of python and support
cd /home/Robert.Grumbine/rgdev/toolbox/nwp/cafs

#These can be anything of convenience
export MPLCONFIGDIR=$HOME/rgexpt/
export OUTDIR=$HOME/rgdev/cafs_nwp

#------------------------------------------------------
tag=`date +"%Y%m%d"`
#debug: 
tag=20241022
#tag=20220501

#reverse -- now to past
end=20220401
#debug: end=20241011

while [ $tag -ge $end ]
do
  echo working on $tag

  yy=`echo $tag | cut -c1-4`
  mm=`echo $tag | cut -c5-6`
  dd=`echo $tag | cut -c7-8`
  if [ ! -f $OUTDIR/${yy}/out.$tag -o ! -f $OUTDIR/${yy}/nwp_${tag}_240.png \
         -o ! -f $OUTDIR/${yy}/path_${tag}_240.kml ] ; then
    time python3 new_cafs.py $yy $mm $dd > $OUTDIR/${yy}/out.$tag
  fi
  if [ -f nwp_${tag}_240.png ] ; then
    mv nwp_${tag}_*.png $OUTDIR/${yy}
  fi  
  if [ -f path_${tag}_240.kml ] ; then
    mv path_${tag}_*.kml $OUTDIR/${yy}
  fi  

  tag=`expr $tag - 1`
  tag=`$HOME/bin/dtgfix3 $tag`
done
