# Visualizing the Bias-Variance Tradeoff

This is a repo for the script I wrote to visualize the bias-variance tradeoff, featured in [Machine Learning at Berkley's blog](ml.berkeley.edu/blog). 

It fits a locally weighted linear regression model to noisy sine wave data. By using the smoothing kernel as a proxy for complexity, we see that complex models tend to overfit and less complex models tend to underfit. We can also see from the training and test error that there is a sweet spot that gives us the best possible model.

`lwlr-visualize.py` is the script that I actually ended up using. Running it will generate pngs of the graphs of the prediction, along with jpegs of graphs of the errors for different weighting neighborhoods. Before running, make sure to create directories called `errors/` and `figures/`.

`index.html` is a quick webpage I threw together to test the animation. The one on the website works a bit differntly (cause we don't exactly want to deal with 200 pngs).
