# Statistical Sampling Explorer

An interactive web app for teaching how sample size affects statistical significance.

##  What it does

This tool demonstrates a key concept in statistics: **when you sample from the same population, you shouldn't find significant differences between groups** — any difference is just random chance.

The app lets you:
- Draw random samples from a normal distribution (μ=2, σ=1)
- Adjust sample sizes from 2 to 100
- See how means and error bars change in real-time
- Compare groups using three statistical tests

## Statistical Tests

The app compares samples 1-4 against sample 5 using:

| Test | Type | Marker |
|------|------|--------|
| t-test | Parametric | 🟢 Circle |
| Mann-Whitney U | Non-parametric | 🔴 Square |
| Wilcoxon rank-sum | Non-parametric | 🟡 Triangle |

Markers appear when p < 0.05 (significant difference detected).


1. **Small samples = unstable results** — With n=2-5, you'll see lots of variability and false positives
2. **Large samples = reliable results** — With n=50+, means converge to the population mean
3. **Error bars shrink** — SEM decreases as sample size increases (SEM = SD/√n)

## Demo

[View the app](https://chart-sampling.onrender.com)

## Run Locally

```bash
# Clone the repo
git clone https://github.com/kamclar/chart-sampling.git
cd chart-sampling

# Install dependencies
pip install -r requirements.txt

# Run the Bokeh server
bokeh serve app.py

# Open http://localhost:5006/app in your browser
```

## License

MIT
