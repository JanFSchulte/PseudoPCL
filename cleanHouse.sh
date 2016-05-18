RUNNUM="$1"
cd Results$RUNNUM/MinBias_2016
rm milleBinary_*
cd ../
rm -r MinBias_2016_*
cd ../
mkdir -p ~/public/pp3.8T_PCL_Alignment
mv Results$RUNNUM ~/public/pp3.8T_PCL_Alignment
cp printTwiki.py ~/public/pp3.8T_PCL_Alignment
echo "DONE!"
