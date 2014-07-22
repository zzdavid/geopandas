from __future__ import absolute_import

import os
import shutil
import tempfile
import unittest

import matplotlib
matplotlib.use('Agg', warn=False)
from matplotlib.pyplot import Artist, savefig, clf
from matplotlib.testing.noseclasses import ImageComparisonFailure
from matplotlib.testing.compare import compare_images
from shapely.geometry import Polygon, LineString, Point, MultiPolygon, MultiLineString
from six.moves import xrange

from geopandas import GeoSeries, GeoDataFrame


# If set to True, generate images rather than perform tests (all tests will pass!)
GENERATE_BASELINE = False

BASELINE_DIR = os.path.join(os.path.dirname(__file__), 'baseline_images', 'test_plotting')


class PlotTests(unittest.TestCase):
    
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        return

    def tearDown(self):
        shutil.rmtree(self.tempdir)
        return

    def _compare_images(self, ax, filename, tol=10):
        """ Helper method to do the comparisons """
        assert isinstance(ax, Artist)
        if GENERATE_BASELINE:
            savefig(os.path.join(BASELINE_DIR, filename))
        savefig(os.path.join(self.tempdir, filename))
        err = compare_images(os.path.join(BASELINE_DIR, filename),
                             os.path.join(self.tempdir, filename),
                             tol, in_decorator=True)
        if err:
            raise ImageComparisonFailure('images not close: %(actual)s '
                                         'vs. %(expected)s '
                                         '(RMS %(rms).3f)' % err)

    def test_poly_plot(self):
        """ Test plotting a simple series of polygons """
        clf()
        filename = 'poly_plot.png'
        t1 = Polygon([(0, 0), (1, 0), (1, 1)])
        t2 = Polygon([(1, 0), (2, 0), (2, 1)])
        polys = GeoSeries([t1, t2])
        ax = polys.plot()
        self._compare_images(ax=ax, filename=filename)

    def test_multipoly_plot(self):
        """ Test plotting a simple series of multipolygons """
        clf()
        filename = 'multipoly_plot.png'
        t1 = Polygon([(0, 0), (1, 0), (1, 1)])
        t2 = Polygon([(1, 0), (2, 0), (2, 1)])
        t3 = Polygon([(2, 0), (3, 0), (3, 1)], [[(2.2, 0.1), (2.8, 0.1), (2.8, 0.7)]])
        t12 = MultiPolygon([t1, t2, t3])
        mpolys = GeoSeries([t12])
        ax = mpolys.plot()
        self._compare_images(ax=ax, filename=filename)

    def test_point_plot(self):
        """ Test plotting a simple series of points """
        clf()
        filename = 'points_plot.png'
        N = 10
        points = GeoSeries(Point(i, i) for i in xrange(N))
        ax = points.plot()
        self._compare_images(ax=ax, filename=filename)

    def test_line_plot(self):
        """ Test plotting a simple series of lines """
        clf()
        filename = 'lines_plot.png'
        N = 10
        lines = GeoSeries([LineString([(0, i), (9, i)]) for i in xrange(N)])
        ax = lines.plot()
        self._compare_images(ax=ax, filename=filename)

    def test_multiline_plot(self):
        """ Test plotting a multilinestring """
        clf()
        filename = 'multilines_plot.png'
        N = 10
        mlines = GeoSeries(MultiLineString(
            [LineString([(0, i), (9, i)]) for i in xrange(N)]))
        ax = mlines.plot()
        self._compare_images(ax=ax, filename=filename)

    def test_dataframe_plot(self):
        """ Test plotting a geodataframe"""
        clf()
        df = GeoDataFrame([
            {'geometry': Polygon([(0, 0), (1, 0), (1, 1)]), 'value1': 1, 'cat1': 'low'},
            {'geometry': Polygon([(1, 0), (2, 0), (2, 1)]), 'value1': 2, 'cat1': 'med'},
            {'geometry': Polygon([(2, 0), (3, 0), (3, 1)]), 'value1': 3, 'cat1': 'high'},
            {'geometry': Polygon([(0, 1), (1, 1), (1, 2)]), 'value1': 4, 'cat1': 'low'},
            {'geometry': Polygon([(1, 1), (2, 1), (2, 2)]), 'value1': 5, 'cat1': 'med'},
            {'geometry': Polygon([(2, 1), (3, 1), (3, 2)]), 'value1': 6, 'cat1': 'high'},
            {'geometry': Polygon([(0, 2), (1, 2), (1, 3)]), 'value1': 7, 'cat1': 'low'},
            {'geometry': Polygon([(1, 2), (2, 2), (2, 3)]), 'value1': 8, 'cat1': 'med'},
            {'geometry': Polygon([(2, 2), (3, 2), (3, 3)]), 'value1': 9, 'cat1': 'high'},
        ])

        filename = 'poly_df_plot.png'
        ax = df.plot(column='value1', scheme='QUANTILES', k=3, colormap='OrRd')
        self._compare_images(ax=ax, filename=filename)

        filename = 'poly_df_category_plot.png'
        ax = df.plot(column='cat1', legend=True, categorical=True, alpha=1.0)
        self._compare_images(ax=ax, filename=filename)

if __name__ == '__main__':
    unittest.main()
