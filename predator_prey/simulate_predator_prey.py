from argparse import ArgumentParser
import numpy as np
import random
import time


def sim():
    """
    predator(pumas) and prey(hares) simulator to predict their density.
    """
    par = ArgumentParser()
    par.add_argument("-r", "--birth-hares", type=float, default=0.08, help="Birth rate of hares")
    par.add_argument("-a", "--death-hares", type=float, default=0.04, help="Rate at which pumas eat hares")
    par.add_argument("-k", "--diffusion-hares", type=float, default=0.2, help="Diffusion rate of hares")
    par.add_argument("-b", "--birth-pumas", type=float, default=0.02, help="Birth rate of pumas")
    par.add_argument("-m", "--death-pumas", type=float, default=0.06, help="Rate at which pumas starve")
    par.add_argument("-diffusion_pumas", "--diffusion-pumas", type=float, default=0.2, help="Diffusion rate of pumas")
    par.add_argument("-dt", "--delta-t", type=float, default=0.4, help="Time step size")
    par.add_argument("-t", "--time_step", type=int, default=10, help="Number of time steps at which to output files")
    par.add_argument("-d", "--duration", type=int, default=500, help="Time to run the simulation (in timesteps)")
    par.add_argument("-f","--landscape-file",type=str,required=True,help="Input landscape file")
    par.add_argument("-hs", "--hare-seed", type=int, default=1, help="Random seed for initialising hare densities")
    par.add_argument("-ps", "--puma-seed", type=int, default=1, help="Random seed for initialising puma densities")
    args = par.parse_args()
    birthrate_of_hares = args.birth_hares
    deathrate_of_hares = args.death_hares
    diffusion_hares = args.diffusion_hares
    birthrate_of_pumas = args.birth_pumas
    deathrate_of_pumas = args.death_pumas
    diffusion_pumas = args.diffusion_pumas
    delta_time = args.delta_t
    timestep = args.time_step
    duration = args.duration
    landscape_file=args.landscape_file
    # landscape_file = "map.dat"

    hare_seed = args.hare_seed
    puma_seed = args.puma_seed
    # Initialise landscape and neighbors
    landscape, number_of_lands, height, width = get_landscape(landscape_file)
    neighbors = get_neighbors(height, width, landscape)
    # Initialise original density for hares and pumas
    hares_old_density = seed(landscape, height, width, hare_seed)
    pumas_old_density = seed(landscape, height, width, puma_seed)

    # Initialise new density and color array for hares and pumas
    hares_new_density = hares_old_density.copy()
    pumas_new_density = pumas_old_density.copy()
    hares_color_array = np.zeros((height, width), int)
    pumas_color_array = np.zeros((height, width), int)

    with open("averages.csv", "w") as f:
        hdr = "Timestep,Time,Hares,Pumas\n"
        f.write(hdr)
    # Main for loop to print out average density for both pumas and hares, write csv file and ppm files
    total_timesteps = int(duration / delta_time)
    for i in range(0, total_timesteps):# Loop time points

        if not i % timestep:# Print out in every time step(10,20,30...)
            average_hares, average_pumas, max_hares, max_pumas = calculate_max_average(i, hares_old_density,
                                                                                       pumas_old_density,
                                                                                       number_of_lands, delta_time)

            with open("averages.csv".format(i), "a") as f:# Write csv file
                f.write("{},{},{},{}\n".format(i, i * delta_time, average_hares, average_pumas))
            for x in range(1, height + 1):
                for y in range(1, width + 1):
                    # Calculate the colors and write to ppm files
                    if landscape[x, y]:
                        if max_hares != 0:
                            hares_color = (hares_old_density[x, y] / max_hares) * 255
                        else:
                            hares_color = 0
                        if max_pumas != 0:
                            pumas_color = (pumas_old_density[x, y] / max_pumas) * 255
                        else:
                            pumas_color = 0
                        hares_color_array[x - 1, y - 1] = hares_color
                        pumas_color_array[x - 1, y - 1] = pumas_color
            with open("map_{:04d}.ppm".format(i), "w") as f:
                hdr = "P3\n{} {}\n{}\n".format(width, x, 255)
                f.write(hdr)
                for x in range(0, height):
                    for y in range(0, width):
                        if landscape[x + 1, y + 1]:
                            f.write("{} {} {}\n".format(hares_color_array[x, y], pumas_color_array[x, y], 0))
                        else:
                            f.write("{} {} {}\n".format(0, 0, 255))
        for x in range(1, height + 1):
            for y in range(1, width + 1):
                if landscape[x, y]:
                    # Calculate density for hares and pumas in next time point
                    hares_new_density = calculate_hares(hares_old_density, pumas_old_density, hares_new_density, x, y,
                                                        delta_time, birthrate_of_hares, deathrate_of_hares,
                                                        diffusion_hares, neighbors)
                    pumas_new_density = calculate_pumas(hares_old_density, pumas_old_density, pumas_new_density, x, y,
                                                        delta_time, birthrate_of_pumas, deathrate_of_pumas,
                                                        diffusion_pumas, neighbors)
        # Swap arrays for next iteration.
        hares_old_density, hares_new_density = swap(hares_old_density, hares_new_density)
        pumas_old_density, pumas_new_density = swap(pumas_old_density, pumas_new_density)


def get_landscape(landscape_file):
    """Initialise landscape by loading "map.dat".
    :parameter landscape_file: data file name
    :returns: landscape array, number of lands, height of map, width of map
    """
    with open(landscape_file, "r") as f:
        width, height = [int(i) for i in f.readline().split(" ")]
        print("Width: {} Height: {}".format(width, height))
        width_halo = width + 2  # Width including halo
        height_halo = height + 2  # Height including halo
        landscape = np.zeros((height_halo, width_halo), int)
        row = 1
        for line in f.readlines():
            values = line.split(" ")
            # Read landscape into array,padding with halo values.
            landscape[row] = [0] + [int(i) for i in values] + [0]
            row += 1

    number_of_lands = np.count_nonzero(landscape)
    print("Number of land-only squares: {}".format(number_of_lands))
    return landscape, number_of_lands, height, width


def seed(landscape, height, width, seed):
    """Generate initial density of hares and pumas by using random seed.
    :parameter landscape: landscape numpy array
    :type landscape: numpy array
    :parameter height: height of the array loading from "map.dat"
    :type height: int
    :parameter width: width of the array loading from "map.dat"
    :type width: int
    :parameter seed: seed for calling random.seed() function
    :type seed: int
    :return: initial density for pumas or hares
    :rtype: numpy array
    """
    old_density = landscape.astype(float).copy()
    random.seed(seed)
    for x in range(1, height + 1):
        for y in range(1, width + 1):
            if seed == 0:
                old_density[x, y] = 0
            else:
                if landscape[x, y]:
                    old_density[x, y] = random.uniform(0, 5.0)
                else:
                    old_density[x, y] = 0

    return old_density


def get_neighbors(height, width, landscape):
    """Calculate the number of neighbours for each land square and generate a neighbors numpy array
    :parameter height: height of map
    :type height: int
    :parameter width: width of map
    :type width: int
    :parameter landscape: landscape numpy array
    :type landscape: numpy array
    :return: neighbors numpy array
    :rtype: numpy array
    """
    # Pre-calculate number of land neighbours of each land square.
    neighbors = np.zeros((height + 2, width + 2), int)
    for x in range(1, height + 1):
        for y in range(1, width + 1):
            neighbors[x, y] = landscape[x - 1, y] \
                              + landscape[x + 1, y] \
                              + landscape[x, y - 1] \
                              + landscape[x, y + 1]
    return neighbors


def calculate_max_average(i, hares_old_density, pumas_old_density, number_of_lands, delta_time):
    """Calculate maximum and average of old hares and pumas density
    :param i: time point
    :param hares_old_density: hares density in current time point
    :param pumas_old_density: pumas density in current time point
    :param number_of_lands: number of lands in landscape
    :param delta_time: changing time
    :returns: average of hares, average of pumas, maximum of hares, maximum of pumas
    """
    max_hares = np.max(hares_old_density)
    max_pumas = np.max(pumas_old_density)
    if number_of_lands != 0:
        average_hares = np.sum(hares_old_density) / number_of_lands
        average_pumas = np.sum(pumas_old_density) / number_of_lands
    else:
        average_hares = 0
        average_pumas = 0
    print("Averages. Timestep: {} Time (s): {} Hares: {} Pumas: {}".format(i, i * delta_time, average_hares,
                                                                           average_pumas))
    return average_hares, average_pumas, max_hares, max_pumas


def calculate_hares(hares_old_density, pumas_old_density, hares_new_density, x, y, delta_time, birthrate_of_hares,
                    deathrate_of_hares, diffusion_hares, neighbors):
    """Calculate new hares density for next time point by implementing the formula
    :param hares_old_density: hares density in current time point
    :param pumas_old_density: pumas density in current time point
    :param hares_new_density: hares density for next time point
    :param x: height position in array
    :param y: width position in array
    :param delta_time: changing time
    :param birthrate_of_hares: birth rate of hares
    :param deathrate_of_hares: death rate of hares
    :param diffusion_hares: diffusion rate of hares
    :param neighbors: neighbors array
    :return: hares density in next time point
    """
    hares_new_density[x, y] = hares_old_density[x, y] + delta_time * ((birthrate_of_hares * hares_old_density[x, y]) - (
            deathrate_of_hares * hares_old_density[x, y] * pumas_old_density[x, y]) + diffusion_hares * (
                                                                              (hares_old_density[x - 1, y] +
                                                                               hares_old_density[x + 1, y] +
                                                                               hares_old_density[x, y - 1] +
                                                                               hares_old_density[x, y + 1]) - (
                                                                                      neighbors[x, y] *
                                                                                      hares_old_density[x, y])))
    if hares_new_density[x, y] < 0:
        hares_new_density[x, y] = 0
    return hares_new_density


def calculate_pumas(hares_old_density, pumas_old_density, pumas_new_density, x, y, delta_time, birthrate_of_pumas,
                    deathrate_of_pumas, diffusion_pumas, neighbors):
    """Calculate new pumas density for next time point by implementing the formula
    The parameters and return are similar to those in the above function
    """
    pumas_new_density[x, y] = pumas_old_density[x, y] + delta_time * (
            (birthrate_of_pumas * hares_old_density[x, y] * pumas_old_density[x, y]) - (
            deathrate_of_pumas * pumas_old_density[x, y]) + diffusion_pumas * (
                    (pumas_old_density[x - 1, y] + pumas_old_density[x + 1, y] + pumas_old_density[x, y - 1] +
                     pumas_old_density[x, y + 1]) - (neighbors[x, y] * pumas_old_density[x, y])))
    if pumas_new_density[x, y] < 0:
        pumas_new_density[x, y] = 0
    return pumas_new_density


def swap(a, b):
    """Swap current density and future density
    :param a: current density
    :param b: future density
    :returns: current density for next time point, old density for current time point
    """
    tmp = a
    a = b
    b = tmp
    return a, b


if __name__ == "__main__":
    sim()
