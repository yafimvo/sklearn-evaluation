CHANGELOG
=========

0.8.4dev
--------
* New ``plot.ROC`` api added
* Adds ``plot.ROC.__add__`` for generating overlapping curves
* ``plot.ROC`` can be serialized/unserialized with ``.dump``/ ``.from_dump``

0.8.3 (2022-12-02)
------------------
* Adds ``plot.silhoutte_analysis``
* Adds clustering user guide
* Adds ``plot.target_analysis``
* Adds bulk insert to ``SQliteTracker`` via ``.insert_many``
* ``SQliteTracker.{get_parameters_keys, get_sample_query}`` support extracting keys from nested JSON objects

0.8.2 (2022-11-24)
------------------
* ``plot.ConfusionMatrix`` and ``plot.ClassifictionReport`` can be serialized/unserialized with ``.dump``/ ``.from_dump``
* Adds ``Experiment`` class to easily create new experiments from ``SQLiteTracker`` using ``.new_experiment()``
* Adds ``Experiment.log_classification_report``
* Adds ``Experiment.log_confusion_matrix``
* Adds ``Experiment.log_figure``
* Adds ``Experiment.log``
* Adds ``Experiment.log_dict``
* Adds ``SQLiteTracker.get``
* Adds docstring examples to ``SQLiteTracker`` and ``Experiment``
* Updates ``SQliteTracker`` tutorial
* Fixes error when querying experiments using ``SQliteTracker`` whose UUID was all numbers (e.g., ``"1234"``)

0.8.1 (2022-11-16)
------------------
* Adds ``plot.residuals`` and ``plot.prediction_error`` for evaluating regression models

0.8 (2022-11-15)
----------------
* ``SQliteTracker.get_sample_query`` generates a query compatible with older SQLite versions that do not support the ``->`` operator
* ``SQliteTracker`` creates shorter experiment IDs
* Fixes whitespace in generated HTML when generating tab views and in ``SQLTracker`` results when ``as_frame=False``


0.7.9 (2022-11-14)
------------------
* Adds ``as_frame`` argument to ``SQLiteTracker``
* Adds ``SQLiteTracker.upsert``
* Allow overwriting records in ``SQLiteTracker.update`` with ``allow_overwrite=True``
* Adds ``SQliteTracker.get_sample_query``
* Adds ``SQliteTracker.get_parameters_keys``

0.7.8 (2022-11-05)
------------------
* Adds ``plot.scores_distribution``
* Adds ``plot.classification_report``
* Fixes ``plot.calibration_curve`` error that scaled probabilities before plotting

0.7.7 (2022-11-01)
------------------
* ``plot.calibration_curve`` allows plotting curves with different sample sizes

0.7.6 (2022-11-01)
------------------
* Adds ``plot.calibration_curve``

0.7.5 (2022-10-28)
------------------
* Renames ``cluster_ranges`` to ``n_clusters`` in ``plot.elbow_curve``
* Adds ``plot.elbow_curve_from_results``

0.7.4 (2022-10-27)
------------------
* Adds ``plot.elbow_curve``

0.7.3 (2022-10-26)
------------------
* Updates telemetry

0.7.2 (2022-09-15)
------------------
* Adds `plot.ConfusionMatrix`

0.7.1 (2022-08-30)
------------------
* Updates telemetry key

0.7 (2022-08-15)
----------------
* ``NotebookDatabase``:  makes ``path`` the primary key
* ``NotebookDatabase``: ``.index()`` uses path to see if the notebook has been indexed
* ``NotebookDatabase``: adds ``update`` to ``.index()``

0.6.1 (2022-08-13)
------------------
* Adds anonymous telemetry

0.6 (2022-08-11)
----------------
* Query notebooks with SQL using ``NotebookDatabase``
* Stripping output string in ``NotebookIntrospector``
* Ignoring standard error output in ``NotebookIntrospector``

0.5.9 (2022-07-04)
------------------
* Adds ``sort`` argument to ``plot.grid_search`` (#45)

0.5.8 (2022-04-16)
------------------
* Fixes an error in ``plot.grid_search`` when parameters grid has a single parameter

0.5.7 (2021-10-17)
------------------
* Adds ``NotebookIntrospector.get_injected_parameters``

0.5.6 (2021-06-26)
------------------
* Fixes error that caused grid search plot to fail when a parameter had a ``None`` value (#40)

0.5.5 (2021-03-28)
------------------
* Adds missing dependency (``IPython``), required by ``NotebookIntrospector``

0.5.4 (2020-12-28)
-------------------
* ``NotebookCollection`` displays output using HTML and tabs
* Adds links to try out the examples in binder


0.5.3 (2020-12-15)
-------------------
* ``DataSelector`` copies input steps to prevent mutating input params
* Simplifies ``NotebookInstrospector`` API and adds first implementation of ``NotebookCollection``


0.5.2 (2020-10-02)
------------------
* Adds SQLiteTracker for tracking ML experiments using a SQlite backend
* Adds NotebookIntrospector [Experimental]
* Migrates tests to ``nox``
* Adds DataSelector
* Enables testing with Python 3.8


0.5.1 (2020-09-18)
-------------------
* Drops support for Python 3.5
* Documentation migrated to Read the Docs
