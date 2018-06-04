import numpy as np


class Curve(object):
    matrix = np.matrix([[-1.0,  3.0, -3.0,  1.0],
                        [ 3.0, -6.0,  3.0,  0.0],
                        [-3.0,  3.0,  0.0,  0.0],
                        [ 1.0,  0.0,  0.0,  0.0]])

    @staticmethod
    def coefficient_a(u):
        return np.power(1 - u, 3)

    @staticmethod
    def coefficient_b(u):
        return 3 * np.power(1 - u, 2) * u

    @staticmethod
    def coefficient_c(u):
        return 3 * (1 - u) * np.power(u, 2)

    @staticmethod
    def coefficient_d(u):
        return np.power(u, 3)

    @staticmethod
    def uniform_sample_set(n):
        return [i / (n - 1) for i in range(n)]

    @staticmethod
    def multiply_by_coefficient_matrix(vs):
        us = np.array([[v] for v in vs])

        def cubed():
            return us * us * us

        def squared():
            return us * us

        return np.hstack([cubed(), squared(), us, np.ones((len(vs), 1))]) * Curve.matrix

    def __init__(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.C = None

    def __str__(self):
        a = "A:(%2.2f, %2.2f)" % (self.a[0], self.a[1])
        b = "B:(%2.2f, %2.2f)" % (self.b[0], self.b[1])
        c = "C:(%2.2f, %2.2f)" % (self.c[0], self.c[1])
        d = "D:(%2.2f, %2.2f)" % (self.d[0], self.d[1])
        return "Curve[%s, %s, %s, %s]" % (a, b, c, d)

    def number_of_frames_covered(self):
        return int(round(self.d[0] - self.a[0] + 1))

    def set_b(self, x, y):
        self.b = np.array([x, y])

    def set_c(self, x, y):
        self.c = np.array([x, y])

    def get_a(self):
        return self.a[0], self.a[1]

    def get_b(self):
        return self.b[0], self.b[1]

    def get_c(self):
        return self.c[0], self.c[1]

    def get_d(self):
        return self.d[0], self.d[1]

    def get_coordinates(self):
        return [self.get_a(), self.get_b(), self.get_c(), self.get_d()]

    def update(self):
        self.C = np.matrix(np.vstack((self.a, self.b,
                                      self.c, self.d)))

    def sample_at(self, us):
        samples = Curve.multiply_by_coefficient_matrix(us) * self.C

        points = []
        for i in range(samples.shape[0]):
            s = samples[i, :]
            point = np.array(s.tolist()[0])
            points.append(point)

        return points

    def sample_uniform(self, n: int):
        return self.sample_at(Curve.uniform_sample_set(n))

    def parameter_nearest_to_point(self, point, resolution):
        us = [i / (resolution - 1) for i in range(resolution)]
        U = Curve.multiply_by_coefficient_matrix(us)

        interps = U * self.C
        distances = np.array(interps - point)
        i = np.argmin((distances * distances).sum(1))
        u = i / (resolution - 1)
        return u

    def parameters_nearest_to_points(self, points, resolution):
        return [self.parameter_nearest_to_point(p, resolution) for p in points]

    def point_nearest_to_point(self, point, resolution):
        u = self.parameter_nearest_to_point(point, resolution)
        return self.sample_at([u])[0]

    def fit_to_points(self, points, t0, t1, us):
        self.a = points[0]
        self.d = points[-1]

        U = Curve.multiply_by_coefficient_matrix(us)
        c0 = np.array(U[:, 0])
        c1 = np.array(U[:, 1])
        c2 = np.array(U[:, 2])
        c3 = np.array(U[:, 3])

        # Setup matrix A
        p11 = np.sum(c1 ** 2)
        np.dot(t0, t1)
        p12 = np.dot(t0, t1) * np.sum(9 * c0 * c3)
        p21 = p12
        p22 = np.sum(c2 ** 2)
        A = np.matrix([[p11, p12], [p21, p22]])

        # Setup column b
        points_ab = [np.dot(t0, p) * u for (p, u) in zip(points, c1)]
        points_cd = [np.dot(t1, p) * u for (p, u) in zip(points, c2)]
        b1 = (np.sum(points_ab)
              - np.dot(t0, self.a) * np.sum(c1 * (c0 + c1))
              - np.dot(t0, self.d) * np.sum(c1 * (c2 + c3)))
        b2 = (np.sum(points_cd)
              - np.dot(t1, self.a) * np.sum(c2 * (c0 + c1))
              - np.dot(t1, self.d) * np.sum(c2 * (c2 + c3)))
        b = np.matrix([[b1], [b2]])

        # Solve for weights
        x = np.linalg.lstsq(A, b)
        x1 = x[0].item(0)
        x2 = x[0].item(1)

        # Set shape of curve to new points
        self.b = self.a + t0 * x1
        self.c = self.d + t1 * x2
        self.update()

    def fit_to_points_free(self, points, us):
        self.a = points[0]
        self.d = points[-1]
        n_dims = len(points[0])

        C14 = np.matrix([ points[0], points[-1] ])
        anim = np.matrix(points)

        R = []
        for u in us:
            r_ = np.matrix([pow(u, 3), pow(u, 2), pow(u, 1), pow(u, 0)])
            r = r_ * Curve.matrix
            R.append(r)

        R = np.matrix(np.array(R))
        R23 = R[:, [1,2]]
        R14 = R[:, [0,3]]
        b = anim - R14 * C14
        
        c23,_resid,_rank,_s = np.linalg.lstsq(R23, b, rcond=None)
        self.b = [c23.item(0, i) for i in range(n_dims)]
        self.c = [c23.item(1, i) for i in range(n_dims)]
        self.update()

    @staticmethod
    def create_from_points(a, b, c, d):
        curve = Curve()
        curve.a = a
        curve.b = b
        curve.c = c
        curve.d = d
        curve.update()
        return curve

    @staticmethod
    def create_by_linear_interpolation(a, d):
        curve = Curve()
        curve.a = a
        curve.d = d
        curve.b = a.interpolate_by(d, 0.33)
        curve.c = a.interpolate_by(d, 0.66)
        curve.update()
        return curve

    @staticmethod
    def create_by_fitting_points(points, t0, t1):
        n = len(points)
        curve = Curve()
        curve.fit_to_points(points, t0, t1, Curve.uniform_sample_set(n))
        return curve

    @staticmethod
    def create_by_fitting_points_free(points):
        n = len(points)
        curve = Curve()
        curve.fit_to_points_free(points, Curve.uniform_sample_set(n))
        return curve