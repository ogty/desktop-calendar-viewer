pip3 install -r $HOME/desktop-calendar-viewer/requirements.txt

for i in {1..31}; do
    ic make google-calendar-$i https://ssl.gstatic.com/calendar/images/dynamiclogo_2020q4/calendar_${i}_2x.png
done
