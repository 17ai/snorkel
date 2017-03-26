README (for Babble Labble project)
Written: 3/25/17

Overview:
The workhorse object of the Babble Labble project is a CDRModel from model.py. It accepts a configuration dictionary from model_config.py which provides all the settings it needs. The actual semantic parsing occurs in the generate_lfs method. This method creates a SemanticParser object.

Test results are summarized in LF_stats.gdoc
Saved notebooks:
    py - python LFs
    nl - natural language LFs (written by Braden)
    pp - paraphrased LFs
    

KNOWN ISSUES:

1) sqlite vs postgres
We get significantly worse results when using postgres compared to using sqlite. I have no idea why. The workaround has been to simply always use sqlite. In order to not repeat the more expense parse/featurize steps often, I have a database that has already had those operations done that I just copy over at the beginning of each new run (snorkel_good4.db).

2) majority vote vs DP
Currently, using majority vote tends to do better than learning the accuracies of LFs and/or modeling their dependencies (with the default settings). The config argument "display_correlation" results in a plot that shows empirical accuracy vs learned accuracy for LFs--the correlation is currently almost non-existant. Those LFs with higher coverage are further from the mean, but of the few examples we have, they don't necessarily seem more likely to be correct. This should be investigated, confirming that the generative model and dependency selector are converging, and seeing if a parameter search can improve them. I did almost no parameter tuning with them, so it very well may be a simple fix.

3) high baseline
Because of the class balance (approx. 40/60), random does quite well, and the naive baseline is quite high. We should (a) get more datasets that are larger and have a larger gap between baseline and state of the art, (b) subsample to get a larger class imbalance so that random does poorly, and/or (c) use a different F score that precision is more highly weighted (so they can't just call everything true and call it good).

4) import error 
Importing the PorterStemmer at the top of matchers.py causes an error when parallelism > 1. I don't know why. Workaround: comment it out.


TODOs:

1) Pull in improvements from master
logistic regression may have improved
disc_model.pr_curve(F_dev, L_gold_dev)

2) Use more unlabeled data
See how much of a boost we get simply from using more than the 8k documents we have for training. Braden has more PubMed articles from Jason that should be relatively easy to import.

3) Use the labels we do have
It's possible we could get a small boost by creating an extra LF that simply returns the label assigned by the user and/or sets those marginals to hard +1/-1 values. (It will probably be a relatively low coverage LF, but could nudge a few other LFs in the right direction).

4) More advanced weighting
Potential parses are currently ranked only according to how many words they have absorbed (fewer absorptions = higher rank). We could potentially include other features in this. (Even just which rules the parse uses).

5) Performance boost with LSTM
All tests were done with logistic regression. Moving to the LSTM may improve numbers?

6) Improvements to parser:
- All left/right commands are with respect to an ArgX. To handle "ArgX is left of the word 'foo'", we invert it to "'foo' is right of ArgX", which is fine for simple cases, but is trickier for trickier cases
- within/apart/away ("A and B are within 3 words of each other")
- their/each other ("A and B are next to each other and C is to their left")
- couple/few (set to 2/3, respectively)
- use commas for grouping/avoiding ambiguity? (A and B, or C ~= A, and B or C)
- change left/right arguments to be a dictionary of keyword args (rather than ordered list of regular args)
- word count can be botched by punctuation
- user lists must match verbatim (if dict is 'colors', then 'color words' won't match)
- recognize multiple types of nouns (not just NN)
- "-induced" is parsed as "- induced", which won't match text
- posession ("A's left" -> "left(A)")
- neither/nor

7) System changes:
- Use 'stanza' for python interface to CoreNLP?
- Use Google's Parsey McParseface?

8) Merging to master
When this code is merged to master, a significant acknowledgment should be made to Bill MacCartney, whose SippyCup semantic parser served as the basis for this one.