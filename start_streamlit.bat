
echo off
echo "Please ensure that you have created an conda environment named empathtech in order to start streamlit. Else expect errors"
echo "Activate empathtech env"
call activate empathtech

call streamlit run Main.py