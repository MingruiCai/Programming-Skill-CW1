# MSc Programming Skills Python predator-prey simulation

## Requirements

* Python 3.x
* [numpy(https://numpy.org/)

### DICE

`python3` is available on DICE. In the following instructions, use the command `python3` instead of the command `python`.

### Cirrus

To get Python 3 on Cirrus, run:

```console
$ module load anaconda/python3
```

---

## Usage

To see help:

```console
$ python predator_prey/simulate_predator_prey.py -h
```

To run the simulation:

```console
$ python predator_prey/simulate_predator_prey.py \
    [-r BIRTH_HARES] [-a DEATH_HARES] \
    [-k DIFFUSION_HARES] [-b BIRTH_PUMAS] \
    [-m DEATH_PUMAS] [-l DIFFUSION_PUMAS] \
    [-dt DELTA_T] [-t TIME_STEP] [-d DURATION] \
    -f LANDSCAPE_FILE [-hs HARE_SEED] \
    [-ps PUMA_SEED]
```

(where `\` denotes a line contuation character)

Alternatively, use:

```console
$ python -m predator_prey.simulate_predator_prey.py ...
```

For example, to run using map.dat with default values for the other parameters:

```console
$ python predator_prey/simulate_predator_prey.py -f map.dat
```

### Command-line parameters

| Flag | Parameter | Description | Default Value |
| ---- | --------- |------------ | ------------- |
| -h | --help | Show help message and exit | - |
| -r | --birth-hares | Birth rate of hares | 0.08 |
| -a | --death-hares | Rate at which pumas eat hares | 0.04 | 
| -k | --diffusion-hares | Diffusion rate of hares | 0.2 |
| -b | --birth-pumas | Birth rate of pumas | 0.02 |
| -m | --death-pumas  | Rate at which pumas starve | 0.06 | 
| -l | --diffusion-pumas | Diffusion rate of pumas | 0.2 |
| -dt | --delta-t | Time step size | 0.4 |
| -t | --time_step | Number of time steps at which to output files | 10 |
| -d | --duration  | Time to run the simulation (in timesteps) | 500 |
| -f | --landscape-file | Input landscape file | - |
| -hs | --hare-seed | Random seed for initialising hare densities. If 0 then the density in each square will be 0, else each square's density will be set to a random value | 1 |
| -ps | --puma-seed | Random seed for initialising puma densities. If 0 then the density in each square will be 0, else each square's density will be set to a random value | 1 |
```

### Input files

Map files are expected to be plain-text files of form:

* One line giving Nx, the number of columns, and Ny, the number of rows
* Ny lines, each consisting of a sequence of Nx space-separated ones and zeros (land=1, water=0).

For example:

```
7 7
1 1 1 1 1 1 1
1 1 1 1 1 1 1
1 1 1 1 0 1 1
1 1 1 1 0 0 1
1 1 1 0 0 0 0
1 1 1 0 0 0 0
1 0 0 0 0 0 0
```

### PPM output files

"Plain PPM" image files are output every `TIME_STEP` timesteps.  These files are named `map_<NNNN>.ppm` and are a visualisation of the density of hares and pumas and water-only squares.

These files do not include the halo as the use of a halo is an implementation detail.

These files are plain-text so you can view them as you would any plain-text file e.g.:

```console
$ cat map<NNNN>.pgm
```

PPM files can be viewed graphically using ImageMagick commands as follows.

Cirrus users will need first need to run:

```console
$ module load ImageMagick
```

To view a PPM file, run:

```console
$ display map<NNNN>.pgm
```

To animate a series of PPM files:

```console
$ animate map*.pgm
```

For more information on the PPM file format, run `man ppm` or see [ppm](http://netpbm.sourceforge.net/doc/ppm.html).

### CSV averages output file

A plain-text comma-separated values file, `averages.csv`, has the average density of hares and pumas (across the land-only squares) calculated every `TIME_STEP` timesteps. The file has four columns and a header row:

```csv
Timestep,Time,Hares,Pumas
```

where:

* `Timestep`: timestep from 0 .. `DURATION`.
* `Time`: time in seconds from 0 .. `DELTA_T` * `DURATION`.
* `Hares`: average density of hares.
* `Pumas`: average density of pumas.

This file is plain-text so you can view it as you would any plain-text file e.g.:

```console
$ cat averages.csv
```
