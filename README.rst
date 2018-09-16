
#######################################
 Spam Classification on Enron Data Set
#######################################

**************
 Introduction
**************

Email spam classfication on the "Enron-Spam in pre-processed form" data set
using Naive Bayes.


*********
 Results
*********

.. list-table::
   :widths: auto
   :header-rows: 1

   * - Test Data Set
     - Result
   * - enron1
     - 94.18%
   * - enron2
     - 92.86%
   * - enron3
     - 94.90%
   * - enron4
     - 93.86%
   * - enron5
     - 97.23%
   * - enron6
     - 97.73%

Runtime: ~14 seconds (train and test)

See :ref:`analysis` for detailed analysis.


**********
 Contents
**********

.. toctree::
   :maxdepth: 1

   analysis/README


*******
 Usage
*******

Data Set
========

.. code-block:: bash
   :caption: Expected directory listing after downloading Enron Data Set.

   $ tree -l -L 2 dat/
   dat/
   ├── english.stop.txt
   └── enron -> ../../../dat/enron/
       ├── enron1
       ├── enron1.tar.gz
       ├── enron2
       ├── enron2.tar.gz
       ├── enron3
       ├── enron3.tar.gz
       ├── enron4
       ├── enron4.tar.gz
       ├── enron5
       ├── enron5.tar.gz
       ├── enron6
       └── enron6.tar.gz

Download the "Enron-Spam in pre-processed form" data set from `this website
<http://www2.aueb.gr/users/ion/data/enron-spam/>`__ and place it in
:file:`dat/enron/` directory.

Basic Usage
===========

.. code-block:: bash
   :caption: Train, test and calculate accuracy.

   $ python --version
   Python 2.7.12

   $ cd code/
   $ python main.py > predict-ds6.txt

   $ bash get_accuracy.sh predict-ds6.txt
   97.73%

Debugging
=========

The :code:`debug` global variable (in :file:`main.py`) allows configuring the
execution.

.. code-block:: py
   :caption: Setting the :code:`debug` variable to print the learned model.

   debug = ["print_model", "run_train_only"]

For example, if you want to see the model that was learned, set it as shown
above.

.. code-block:: bash
   :caption: Printing the learned model.

   $ python main.py > predict-ds6.txt

   $ head predict-ds6.txt
   NaiveBayesClassifier    DocFreq spam    ham
   fawn    6       6.0     2.22044604925e-16
           18      38.0    2.22044604925e-16
   percopo 3       2.22044604925e-16       3.0
   catechols       2       2.0     2.22044604925e-16
   mdbm    1       1.0     2.22044604925e-16
   bloqueos        4       4.0     2.22044604925e-16
   240061  4       2.22044604925e-16       7.0
   sowell  2       2.22044604925e-16       2.0
   017201846       2       2.0     2.22044604925e-16

(As the learning time is small, we do not support pickle-ing the model.)

Please see :code:`main.py` for other possible values.

Model Interpretability
======================

.. code-block:: bash
   :caption: Run model and determine misclassifications.

   $ python main.py > predict-ds6.txt

   $ grep False predict-ds6.txt | awk 'function abs(x) { return x < 0 ? 
   -x : x } { print(abs($4-$5), $0) }' | sort -k1,1 -n | head                          
   0.0404643 False spam    ham     -23.4744411393  -23.5149054246  ../dat/enron/enron6/ham/4839.2001-10-25.lokay.ham.txt
   0.293468 False  ham     spam    -37.1120550078  -36.8185866744  ../dat/enron/enron6/spam/2692.2005-01-13.BG.spam.txt
   0.300347 False  spam    ham     -29.8652542377  -30.1656009106  ../dat/enron/enron6/ham/3769.2001-06-14.lokay.ham.txt
   0.425152 False  ham     spam    -0.928149293364 -0.502997327745 ../dat/enron/enron6/spam/0442.2004-09-02.BG.spam.txt
   0.425152 False  ham     spam    -0.928149293364 -0.502997327745 ../dat/enron/enron6/spam/5910.2005-07-23.BG.spam.txt
   0.749669 False  spam    ham     -61.5928200042  -62.3424894688  ../dat/enron/enron6/ham/3859.2001-06-27.lokay.ham.txt
   0.788438 False  ham     spam    -23.0850307794  -22.2965924716  ../dat/enron/enron6/spam/3158.2005-02-01.BG.spam.txt
   0.869716 False  spam    ham     -69.4085459143  -70.2782619644  ../dat/enron/enron6/ham/4959.2001-11-09.lokay.ham.txt
   1.01452 False   ham     spam    -40.9774586044  -39.9629392579  ../dat/enron/enron6/spam/0872.2004-10-02.BG.spam.txt
   1.11811 False   ham     spam    -359.693306199  -358.575199471  ../dat/enron/enron6/spam/5177.2005-06-08.BG.spam.txt

Run model and determine misclassifications as shown above.

.. code-block:: py
   :caption: Set :code:`debug` to :code:`"run_print_freqs"` to enable model
             interpretability.

   debug = ["run_print_freqs"]

Set :code:`debug` to :code:`"run_print_freqs"` to enable model
interpretability as shown above.

As an example, let's consider :file:`enron6/spam/0872.2004-10-02.BG.spam.txt`.

.. code-block:: bash
   :caption: word_diff for misclassified
             :file:`enron6/spam/0872.2004-10-02.BG.spam.txt`

   1.01452 False   ham     spam    -40.9774586044  -39.9629392579  ../dat/enron/enron6/spam/0872.2004-10-02.BG.spam.txt

Although it is "spam," it is misclassified as "ham" by a small word_diff of
1.01452.

.. code-block:: bash
   :caption: Sample run to demonstrate model interpretability.

   $ python main.py ../dat/enron/enron6/spam/0872.2004-10-02.BG.spam.txt
    
   Token   DocFreq LogProbSpam     LogProbHam      word_diff
   subject 7345    -6.99428150365  -5.44600027609  1.54828122756
   640     18      -11.5912935019  -12.9972747206  1.40598121863
   ram     106     -9.73890941089  -10.5843415704  0.845432159512
   doubts  50      -11.7248248946  -10.4323253631  1.29249953146

Running model interpretability, we see that the word "subject" contributed a
word_diff of 1.55 towards "ham".  This boosted the sum of log probabilities
for "ham," resulting in misclassification of this email.

As "subject" is present in every email (in the header line), it might make
sense to filter it out.  This could be done by using TF-IDF.  Better still, we could shunt it out by adding it to our list of stop words thereby saving some processing.


*********
 Sources
*********

- The problem statement was provided as an exercise as part of a talk on
  "Text Classification using Naive Bayes Algorithm," by Yash Gandhi held
  at PubMatic.

- We used the "Enron-Spam in pre-processed form" data set from
  `this website <http://www2.aueb.gr/users/ion/data/enron-spam/>`__

- The Stop Words :file:`dat/english.stop.txt` were obtained from
  `GitHub cs109/2015
  <https://github.com/cs109/2015/blob/master/Lectures/Lecture15b/sparklect/english.stop.txt>`__
  and modified as required.


********************
 Indices and tables
********************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

