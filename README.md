Predicting Forum Thread Posts
=============================

Use of probabilistic graphical Models to predict forum posts in avsforum.com. Project for CS5340

##Directory structure
1. `working`: Stores working files for use later. e.g.
	* pickled models to be used for evaluation

2. `obj_globals`: global objects to be used for accessing data quickly
	* pickled LDA model. Topics, tokens etc.

3. `reports`: Generated files showing performance of models
	* TSVs
	* CSVs
	* partial .tex files of tables

##Preprocessing
1. `learn_topics` topics learnt from data.
2. `topic_time_dist` generates arrays of time histograms of topics.
	We're looking for time distributions significantly different between topics.
