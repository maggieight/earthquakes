from datetime import date
import matplotlib.pyplot as plt
import earthquakes
import matplotlib.ticker as ticker


def get_data():
    return earthquakes.get_data()


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year
    return year


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    magnitudes_per_year = {}
    for earthquake in earthquakes:
        year = get_year(earthquake)
        mag = get_magnitude(earthquake)
        if year not in magnitudes_per_year:
            magnitudes_per_year[year] = []
        magnitudes_per_year[year].append(mag)
    return magnitudes_per_year


def plot_average_magnitude_per_year(earthquakes):
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    average_magnitudes = {year: sum(mags) / len(mags) for year, mags in magnitudes_per_year.items()}
    plt.bar(average_magnitudes.keys(), average_magnitudes.values())
    plt.xlabel("Year")
    plt.ylabel("Average Magnitude")
    plt.title("Average Earthquake Magnitude per Year")
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()


def plot_number_per_year(earthquakes):
    counts_per_year = {}
    for earthquake in earthquakes:
        year = get_year(earthquake)
        if year not in counts_per_year:
            counts_per_year[year] = 0
        counts_per_year[year] += 1
    plt.bar(counts_per_year.keys(), counts_per_year.values())
    plt.xlabel("Year")
    plt.ylabel("Number of Earthquakes")
    plt.title("Number of Earthquakes per Year")
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()



# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)