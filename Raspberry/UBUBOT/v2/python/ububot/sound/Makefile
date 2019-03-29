
all: clean enable disable siren symph9 pokemon portal

enable:
	gcc -o enable.s src/enable.c -lwiringPi -D
disable:
	gcc -o disable.s src/disable.c -lwiringPi -D
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
portal:
	gcc -o portal.s src/portal.c -lwiringPi -lpthread
clean:
	rm -f *.s