
all: clean enable disable reset siren symph9 pokemon portal bits

enable:
	gcc -o enable.s src/enable.c -lwiringPi
disable:
	gcc -o disable.s src/disable.c -lwiringPi
reset:
	gcc -o reset.s src/reset.c -lwiringPi
siren:
	gcc -o siren.s src/siren.c -lwiringPi -lpthread -lm
symph9:
	gcc -o symph9.s src/symph9.c -lwiringPi -lpthread
pokemon:
	gcc -o pokemon_b_w_rb.s src/pokemon.c -lwiringPi -lpthread -D SONG=1
	gcc -o pokemon_b_w_rs.s src/pokemon.c -lwiringPi -lpthread -D SONG=2
	gcc -o pokemon_b_w_bw.s src/pokemon.c -lwiringPi -lpthread -D SONG=3
	gcc -o pokemon_b_t_rb.s src/pokemon.c -lwiringPi -lpthread -D SONG=4
	gcc -o pokemon_b_t_rs.s src/pokemon.c -lwiringPi -lpthread -D SONG=5
	gcc -o pokemon_v_rb.s src/pokemon.c -lwiringPi -lpthread -D SONG=6
portal:
	gcc -o portal.s src/portal.c -lwiringPi -lpthread
bits:
	gcc -o xp_on.s src/bits.c -lwiringPi -lpthread -D SONG=1
	gcc -o xp_off.s src/bits.c -lwiringPi -lpthread -D SONG=2
clean:
	rm -f *.s