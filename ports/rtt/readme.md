python make_root_pointers.py ../ports/rtt/boards/genhdr/qstr.i.last > ../ports/rtt/boards/genhdr/root_pointers.h
python makeversionhdr.py ../ports/rtt/boards/genhdr/mpversion.h 
python ../py/makeqstrdefs.py split qstr ../ports/rtt/boards/genhdr/qstr.i.last ../ports/rtt/boards/genhdr/qstr _ 
python ../py/makeqstrdefs.py cat qstr _ ../ports/rtt/boards/genhdr/qstr ../ports/rtt/boards/genhdr/qstrdefs.collected.h

cat ../py/qstrdefs.h qstrdefsport.h ../ports/rtt/boards/genhdr/qstrdefs.collected.h | sed 's/^Q(.*)/"&"/' | gcc -E -I. -Ibuild -I.. -I../ports/rtt/boards -Wall -Werror -Wextra -Wno-unused-parameter -Wpointer-arith -std=gnu99 -Os -fdata-sections -ffunction-sections -fno-asynchronous-unwind-tables - | sed 's/^\"\(Q(.*)\)\"/\1/' > ../ports/rtt/boards/genhdr/qstrdefs.preprocessed.h

python ../py/makeqstrdata.py ../ports/rtt/boards/genhdr/qstrdefs.preprocessed.h > ../ports/rtt/boards/genhdr/qstrdefs.generated.h

python makemoduledefs.py ../ports/rtt/boards/genhdr/qstr.i.last > ../ports/rtt/boards/genhdr/moduledefs.h

#touch ../ports/rtt/boards/genhdr/qstr.split


