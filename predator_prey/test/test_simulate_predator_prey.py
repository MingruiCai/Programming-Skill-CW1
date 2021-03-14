import predator_prey.simulate_predator_prey as simulate
import unittest
import numpy as np
import random


class simTestCase(unittest.TestCase):

    def test_numberOflands(self):
        """Check number of lands
        """
        size = 200
        self.assertEquals(size, simulate.get_landscape("map.dat")[1], msg="number of lands returned was unexpected")

    def test_landscape(self):
        """ Check the landscape array
        """
        test_landscape = np.zeros((22, 12), int)
        for row in range(1, 21):
            test_landscape[row] = [0] + [1 for i in range(10)] + [0]
        ifequal = (test_landscape == simulate.get_landscape("map.dat")[0]).all()
        self.assertEquals(ifequal, True, msg="landscape returned was unexpected")

    def test_neighbors(self):
        """ Check the neighbors array
        """
        test_neighbors = np.zeros((22, 12), int)
        for row in range(1, 21):
            if row == 1 or row == 20: test_neighbors[row] = [0, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 0]
            if row > 1 and row < 20: test_neighbors[row] = [0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 0]
        ifequal = (test_neighbors == simulate.get_neighbors(20, 10, simulate.get_landscape("map.dat")[0])).all()
        self.assertEquals(ifequal, True, msg="neighbors returned was unexpected")

    def test_seed(self):
        """Check the original value of density(the initial density)
        """
        landscape = simulate.get_landscape("map.dat")[0]
        test_old_density = landscape.astype(float).copy()
        random.seed(1)
        for x in range(1, 21):
            for y in range(1, 11):
                if landscape[x, y]:
                    test_old_density[x, y] = random.uniform(0, 5.0)
                else:
                    test_old_density[x, y] = 0
        ifequal = (test_old_density == simulate.seed(simulate.get_landscape("map.dat")[0], 20, 10, 1)).all()
        self.assertEquals(ifequal, True, msg="seeds returned was unexpected")

    def test_max_hares(self):
        """Check the maximum of hares when time==0
        """
        landscape = simulate.get_landscape("map.dat")[0]
        hares_old_density = simulate.seed(landscape, 20, 10, 1)
        pumas_old_density = simulate.seed(landscape, 20, 10, 1)
        number_of_lands = simulate.get_landscape("map.dat")[1]
        test_max_hares = simulate.calculate_max_average(0, hares_old_density, pumas_old_density, number_of_lands, 0.4)[
            2]
        self.assertEquals(test_max_hares, 4.962717060880325, msg="maximum of hares was unexpected")

    def test_max_pumas(self):
        """Check the maximum of pumas when time==0
        """
        landscape = simulate.get_landscape("map.dat")[0]
        hares_old_density = simulate.seed(landscape, 20, 10, 1)
        pumas_old_density = simulate.seed(landscape, 20, 10, 1)
        number_of_lands = simulate.get_landscape("map.dat")[1]
        test_max_pumas = simulate.calculate_max_average(0, hares_old_density, pumas_old_density, number_of_lands, 0.4)[
            3]
        self.assertEquals(test_max_pumas, 4.962717060880325, msg="maximum of pumas was unexpected")

    def test_average_hares(self):
        """Check the average of hares when time==0
        """
        landscape = simulate.get_landscape("map.dat")[0]
        hares_old_density = simulate.seed(landscape, 20, 10, 1)
        pumas_old_density = simulate.seed(landscape, 20, 10, 1)
        number_of_lands = simulate.get_landscape("map.dat")[1]
        test_average_hares = \
            simulate.calculate_max_average(0, hares_old_density, pumas_old_density, number_of_lands, 0.4)[
                0]
        self.assertEquals(test_average_hares, 2.4268595788671457, msg="average of hares was unexpected")

    def test_average_pumas(self):
        """Check the average of pumas when time==0
        """
        landscape = simulate.get_landscape("map.dat")[0]
        hares_old_density = simulate.seed(landscape, 20, 10, 1)
        pumas_old_density = simulate.seed(landscape, 20, 10, 1)
        number_of_lands = simulate.get_landscape("map.dat")[1]
        test_average_pumas = \
            simulate.calculate_max_average(0, hares_old_density, pumas_old_density, number_of_lands, 0.4)[
                1]
        self.assertEquals(test_average_pumas, 2.4268595788671457, msg="average of pumas was unexpected")

    def test_calculate_hares(self):
        """Check new hares density value in point[1][1] in hares density array when time==0
        """
        landscape = simulate.get_landscape("map.dat")[0]
        hares_old_density = simulate.seed(landscape, 20, 10, 1)
        pumas_old_density = simulate.seed(landscape, 20, 10, 1)
        hares_new_density = hares_old_density.copy()
        test_hares_new_density = simulate.calculate_hares(hares_old_density, pumas_old_density, hares_new_density, 1, 1,
                                                          0.4, 0.08,
                                                          0.04, 0.2, simulate.get_neighbors(20, 10, landscape))
        self.assertEquals(test_hares_new_density[1][1], 1.2518861406345514,
                          msg="hares new density returned was unexpected")

    def test_calculate_pumas(self):
        """Check new pumas density value in point[1][1] in hares density array when time==0
        """
        landscape = simulate.get_landscape("map.dat")[0]
        hares_old_density = simulate.seed(landscape, 20, 10, 1)
        pumas_old_density = simulate.seed(landscape, 20, 10, 1)
        pumas_new_density = pumas_old_density.copy()
        test_pumas_new_density = simulate.calculate_pumas(hares_old_density, pumas_old_density, pumas_new_density, 1, 1,
                                                          0.4, 0.02, 0.06,
                                                          0.2, simulate.get_neighbors(20, 10, landscape))
        self.assertEquals(test_pumas_new_density[1][1], 1.2250964023406175,
                          msg="pumas new density returned was unexpected")


if __name__ == '__main__':
    unittest.main(verbosity=2)
