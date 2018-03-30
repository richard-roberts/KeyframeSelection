# Salient Poses - Reference Implementation

![Thumbnail][http://richardroberts.co.nz/images/hosting/salientPosesThumb.png]

This project provides a simple reference implementation of the Salient Poses [Salient Poses](https://github.com/richard-roberts/PhD) algorithm, which I developed during my doctorate study.

Please refer to [The Details](#the-details) for more information on code layout and to [Getting Started](#getting-started) for more information about obtaining and running this implementation. For the more interested, and for other researchers in particular, the [Comparison](#comparison) section may be useful.

Please post any issues in via the [parent repository](https://github.com/richard-roberts/PhD/issues).

The Details
-----------

This project provides a Python-based implementation of all three steps of the Salient Poses algorithm, described [here](https://github.com/richard-roberts/PhD#Details). In particular, the [Error Table](https://github.com/richard-roberts/SalientPosesReference/blob/master/src/analysis/error_table.py) class provides the logic required for the first analysis step, the [Selector](https://github.com/richard-roberts/SalientPosesReference/blob/master/src/selection/selector.py) superclass the logic for the second selection step, and finally the [Interpolator](https://github.com/richard-roberts/SalientPosesReference/blob/master/src/interpolation/interpolator.py) superclass provides the same for the final interpolation step.

#### Why the Abstraction?

I've decided to abstract the behaviour into "Selector" and "Interpolator" superclasses so that I can explore alternative implementations to each step in a plug-and-play behaviour. The concrete subclasses [Salient](https://github.com/richard-roberts/SalientPosesReference/blob/master/src/selection/salient.py) and [OptimizationBasedCurveFitting](https://github.com/richard-roberts/SalientPosesReference/blob/master/src/interpolation/obcf.py) provide the concrete implementation of Salient Poses. Finally, the [Error Table Library](https://github.com/richard-roberts/SalientPosesReference/blob/master/src/analysis/error_table_library.py) provides a mechanism for plugging in different criteria in the first analyses step.


Getting Started
---------------

If you'd like to run the reference implementation, I would recommend first cloning the repository and running the tests (the repository includes a bash script for executing the tests). Alternatively, the `.idea` project file can be opened in the [PyCharm](https://www.jetbrains.com/pycharm/), which includes a testing configuration that can executed interactively.

Please note the other available implementations, [listed here](https://github.com/richard-roberts/PhD#contents).


Contributing
------------

Please refer to the [contributing](https://github.com/richard-roberts/PhD#details) section of the [parent repository](ttps://github.com/richard-roberts/PhD).


Comparison
----------

*Note: this section is a work-in-progress. Please contact me directly for more information regarding comparison.* 

I'm actively developing some Python-based tooling for benchmarking Salient Poses and the other algorithms related to it. The tooling will provide mechanisms that enable automatic:

- benchmarking for each algorithm,
- visualization of how well the keyframes summarize the motion, and
- visualization, in terms of renders, of the poses that correspond to the keyframes of each algorithm.

I will continue to develop further tools as I think of them. Please feel free to make suggestions via the [parent repository's issue tracker](https://github.com/richard-roberts/PhD/issues).

The other keyframe selection algorithms include:

- [Key-posture Extraction Out of Human Motion Data](http://ieeexplore.ieee.org/document/1020399?reload=true), a greedy algorithm for keyframe selection designed by Lim and Thalmann, 2001.
    + The implementation is [here](https://github.com/richard-roberts/SalientPosesReference/blob/master/src/selection/greedy.py)

And the other interpolation algorithms include:

- [An algorithm for automatically fitting digitized curves](http://www.gameenginegems.net/gemsdb/article.php?id=780), an algorithm for fitting chains of two-dimensional cubic Bézier curves to sampled data.
    + The **partial** implementation is [here](https://github.com/richard-roberts/SalientPosesReference/blob/master/src/interpolation/schneider.py).
    + The original implementation is hosted [here](http://www.realtimerendering.com/resources/GraphicsGems/). 

